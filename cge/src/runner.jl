# Approved three-scenario experiment in the actual repaired GRID/GHEER core.
using JuMP, PATHSolver, Complementarity, CSV, DataFrames, Serialization, SHA, Statistics
length(ARGS)>=3 || error("runner.jl RUNTIME GRID SCENARIO [END_YEAR]")
runtime=abspath(ARGS[1]);grid=ARGS[2];scenario=ARGS[3]
stop_year=length(ARGS)>=4 ? parse(Int,ARGS[4]) : (grid=="annual_2030" ? 2030 : 2050)
model_dir=joinpath(runtime,"model","jl_r18s15");input_dir=joinpath(runtime,"inputs")
output_dir=joinpath(runtime,"equilibria_final",grid,get(ENV,"LEGACY_RUN_ID",scenario));mkpath(output_dir)
license=get(ENV,"PATH_LICENSE_STRING","")
if scenario != "CHECK"
    isempty(license) && error("Set PATH_LICENSE_STRING in your environment before solving. No license key is distributed with this repository.")
    PATHSolver.c_api_License_SetString(license)
end
cd(model_dir)
rNum=18;sNum=15;yrgap=grid=="annual_2030" ? 1 : 5
tfp_flag="GDP";cp_flag="Tax";rr_farm=0.;rr_int=0.;rr_h=0.;rand_flag=0
Years=grid=="annual_2030" ? collect(2017:2030) : [2017;collect(2020:5:2050)]
NumYears=length(Years)
for f in ["sam/sam_set_r18s15.jl","ene/ene_set.jl","elec/elec_set.jl","elas/elas_cal_0.jl",
 "sam/sam_read.jl","sam/sam_cal_new.jl","ene/ene_read.jl","ene/ene_cal.jl",
 "elec/elec_read.jl","elec/elec_cal_share.jl","dyn/dyn_cal.jl","policy/policy_cal.jl"]
    println("LOAD ",f);flush(stdout);include(joinpath(model_dir,f))
end
const CalibrationRE=[SolarPV,Wind,Hydro,findfirst(==("Biomass"),EcType)]
const reference_physical=CSV.read(joinpath(input_dir,"physical_benchmark.csv"),DataFrame)
const physical_rows=Dict((String(x.region),String(x.technology))=>x for x in eachrow(reference_physical))
const generation_to_capacity=zeros(NumElec,NumRegion)
for i in GenType,r in Regions
    obs=physical_rows[(Region[r],EcType[i])]
    factor=gen_elec0[i,r]>0 && obs.generation_TWh>0 ? obs.generation_TWh/gen_elec0[i,r] :
      median([physical_rows[(Region[q],EcType[i])].generation_TWh/gen_elec0[i,q] for q in Regions if gen_elec0[i,q]>0 && physical_rows[(Region[q],EcType[i])].generation_TWh>0])
    generation_to_capacity[i,r]=factor/(8.76*obs.capacity_factor)
end
m=MCPModel()
for f in ["sam/init_production_new_elec.jl","sam/init_income.jl","sam/init_demand.jl","sam/init_trade.jl",
 "sam/init_save.jl","sam/init_macro.jl","ene/init_ene.jl","elec/init_elec.jl","policy/init_policy.jl",
 "running/exg_param_tfp_share.jl","sam/init_investment_closure.jl",
 "sam/eq_production_s22_elec.jl","sam/eq_demand.jl","sam/eq_income_elec.jl","sam/eq_save.jl",
 "sam/eq_trade.jl","sam/eq_macro_tfp_new.jl","ene/eq_ene.jl","elec/eq_elec.jl","policy/eq_policy.jl"]
    println("BUILD ",f);flush(stdout);include(joinpath(model_dir,f))
end
eq_investment_closure();eq_production();eq_income();eq_demand();eq_save();eq_trade()
eq_macro("TFP");eq_ene();eq_elec();eq_policy("Tax");eq_calibration_switches()
include(joinpath(@__DIR__,"cached_path_solver.jl"))
include(joinpath(@__DIR__,"experiment.jl"))
if scenario=="CHECK"
    println("MODEL_BUILD_CHECK_PASS variables=", JuMP.num_variables(m))
elseif scenario=="C"
    include(joinpath(@__DIR__,"capacity_search.jl"));run_capacity_search()
elseif scenario=="EXPORT"
    include(joinpath(@__DIR__,"export.jl"));export_states()
else
    run_experiment()
end
