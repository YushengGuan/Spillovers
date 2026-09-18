# Reuse GHEER's exact Complementarity mappings and the actual PATH solver.
# Unlike the upstream wrapper, build the AD evaluator and sparse Jacobian
# pattern once per model. No economics, equation, tolerance or bound is changed.
using SparseArrays
const CachedMOI=JuMP.MOI

mutable struct CachedPATHModel{E}
    model::JuMP.Model
    data::Vector
    evaluator::E
    lower::Vector{Float64}
    upper::Vector{Float64}
    var_names::Vector{String}
    eq_names::Vector{String}
    jacobian::SparseMatrixCSC{Float64,Int}
    jac_values::Vector{Float64}
    jac_positions::Vector{Int}
    x::Vector{Float64}
    f::Vector{Float64}
end

function CachedPATHModel(model)
    rows=sort(Complementarity.get_MCP_data(model),by=x->x.raw_idx)
    n=length(rows)
    [x.raw_idx for x in rows]==collect(1:n) || error("Noncontiguous GHEER MCP variable indexes")
    isempty(model.nlp_model.constraints) || error("Construct cached evaluator before adding other NL constraints")
    @NLconstraint(model,[i=1:n],rows[i].F==0)
    d=JuMP.NLPEvaluator(model)
    CachedMOI.initialize(d,[:Jac])
    pattern=CachedMOI.jacobian_structure(d)
    J=sparse(first.(pattern),last.(pattern),ones(length(pattern)),n,n)
    positions=Dict((J.rowval[k],col)=>k for col in 1:n for k in J.colptr[col]:J.colptr[col+1]-1)
    slots=[positions[p] for p in pattern]
    x=[Float64(JuMP.start_value(row.var)) for row in rows]
    return CachedPATHModel(model,rows,d,[row.lb for row in rows],[row.ub for row in rows],
        [row.var_name for row in rows],[row.F_name for row in rows],J,zeros(length(pattern)),slots,x,zeros(n))
end

function solve_cached!(cache::CachedPATHModel; output="no",tolerance=1e-8,time_limit=6000,reinitialize=false,equilibrate_rows=false)
    Base.Experimental.@force_compile
    # NLparameter values change between years/scenarios. ReverseAD may reuse
    # its last_x cache at the warm start, so invalidate it once per solve.
    # For the pinned ReverseAD backend, the source checks only last_x before
    # reading the shared model parameter table. Invalidate that cache without
    # rebuilding the expression graph. Other backends use the public fallback.
    backend=hasproperty(cache.evaluator,:backend) ? cache.evaluator.backend : nothing
    if !reinitialize && backend!==nothing && hasproperty(backend,:last_x)
        fill!(backend.last_x,NaN)
    else
        CachedMOI.initialize(cache.evaluator,[:Jac])
    end
    n=length(cache.data);J=cache.jacobian
    row_scale=ones(n)
    if equilibrate_rows
        # Positive row multipliers preserve the exact MCP solution set. Only
        # amplify weakly scaled equations; never downweight account identities.
        CachedMOI.eval_constraint_jacobian(cache.evaluator,cache.jac_values,cache.x)
        fill!(J.nzval,0)
        for h in eachindex(cache.jac_values);J.nzval[cache.jac_positions[h]]+=cache.jac_values[h];end
        magnitude=abs.(J)*max.(abs.(cache.x),1e-6)
        row_scale.=clamp.(1.0./max.(magnitude,1e-12),1.0,1e8)
        println("Positive equation row scaling: min=",minimum(row_scale)," max=",maximum(row_scale));flush(stdout)
    end
    function f_callback(n_arg::Cint,z::Vector{Cdouble},f::Vector{Cdouble})
        Base.Experimental.@force_compile
        CachedMOI.eval_constraint(cache.evaluator,f,z)
        f .*= row_scale
        return Cint(0)
    end
    function j_callback(n_arg::Cint,nnz_arg::Cint,z::Vector{Cdouble},col_start::Vector{Cint},col_len::Vector{Cint},row::Vector{Cint},values::Vector{Cdouble})
        Base.Experimental.@force_compile
        CachedMOI.eval_constraint_jacobian(cache.evaluator,cache.jac_values,z)
        fill!(J.nzval,0)
        for h in eachindex(cache.jac_values)
            J.nzval[cache.jac_positions[h]]+=cache.jac_values[h]
        end
        for col in 1:n
            col_start[col]=J.colptr[col];col_len[col]=J.colptr[col+1]-J.colptr[col]
        end
        for k in eachindex(J.nzval)
            row[k]=J.rowval[k];values[k]=J.nzval[k]*row_scale[J.rowval[k]]
        end
        return Cint(0)
    end
    t=time()
    status,z,info=PATHSolver.solve_mcp(f_callback,j_callback,cache.lower,cache.upper,cache.x;
        nnz=nnz(J),variable_names=cache.var_names,constraint_names=cache.eq_names,
        convergence_tolerance=tolerance,output=output,time_limit=time_limit)
    z===nothing && error("PATH returned no solution: $status")
    cache.x.=z
    for (i,row) in enumerate(cache.data)
        Complementarity.set_result_value(row,z[i])
        JuMP.set_start_value(row.var,z[i])
    end
    CachedMOI.eval_constraint(cache.evaluator,cache.f,z)
    residual=maximum(abs.(z.-clamp.(z.-cache.f,cache.lower,cache.upper)))
    return (status=Complementarity.return_type[Int(status)],max_natural_residual=residual,elapsed=time()-t,info=info)
end
