# Numerical calibration, exact fixed-price cost inversion, scenario recursion and reporting.
const physical=CSV.read(joinpath(input_dir,"physical_benchmark.csv"),DataFrame)
const targets=CSV.read(joinpath(input_dir,"power_targets.csv"),DataFrame)
const paths=CSV.read(joinpath(input_dir,"dynamic_paths.csv"),DataFrame)
const ratios=CSV.read(joinpath(input_dir,"regional_tfp_paths.csv"),DataFrame)
const phy=Dict((String(x.region),String(x.technology))=>x for x in eachrow(physical))
const target=Dict((String(x.region),String(x.technology),Int(x.year))=>x for x in eachrow(targets))
const dyn=Dict((String(x.region),Int(x.year))=>x for x in eachrow(paths))
const ratio_map=Dict((String(x.region),String(x.technology),Int(x.year))=>Float64(x.tfp_multiplier) for x in eachrow(ratios))
const deflator=parse(Float64,get(ENV,"CGE_DEFLATOR","1.279736455613577"))
const diagnostics=DataFrame();const macrodata=DataFrame();const powerdata=DataFrame()
const accounting=DataFrame();const cost_mapping=DataFrame();const calibration=DataFrame()
const carbon_trials=DataFrame();const carbon_matches=DataFrame();const transitions=DataFrame()
const cache=CachedPATHModel(m)
rv(v)=cache.x[JuMP.index(v).value]
function generation_factor(i,r)
    gen_elec0[i,r]>0 && Float64(phy[(Region[r],EcType[i])].generation_TWh)>0 && return Float64(phy[(Region[r],EcType[i])].generation_TWh)/gen_elec0[i,r]
    # Only a physical unit conversion for zero-flow cells, never a cost donor.
    median([Float64(phy[(Region[q],EcType[i])].generation_TWh)/gen_elec0[i,q] for q in Regions if gen_elec0[i,q]>0 && Float64(phy[(Region[q],EcType[i])].generation_TWh)>0])
end
generation_twh(i,r)=rv(gen_elec[i,r])*generation_factor(i,r)
capacity_gw(i,r)=generation_twh(i,r)/(8.76*Float64(phy[(Region[r],EcType[i])].capacity_factor))
function persist_tables()
    for (name,df) in [("solve_diagnostics",diagnostics),("macro",macrodata),("power",powerdata),
      ("accounting",accounting),("cost_mapping",cost_mapping),("calibration",calibration),
      ("carbon_trials",carbon_trials),("carbon_matches",carbon_matches),("capital_transitions",transitions)]
        ncol(df)>0 && CSV.write(joinpath(output_dir,name*".csv"),df)
    end
end
function solve_step(stage,y;tol=1e-8,strict=true)
    all(isfinite,m.nlp_model.parameters) || error("Non-finite parameter before $stage")
    valid_start=copy(cache.x)
    println("SOLVE ",grid," ",scenario," ",y," ",stage);flush(stdout)
    sol=solve_cached!(cache;output="no",tolerance=tol,time_limit=strict ? 120 : 20)
    push!(diagnostics,(grid=grid,scenario=scenario,year=y,stage=stage,status=String(sol.status),
        residual=sol.max_natural_residual,seconds=sol.elapsed,requested_tolerance=tol);cols=:union)
    println("RESULT ",sol.status," residual=",sol.max_natural_residual," seconds=",sol.elapsed);flush(stdout)
    if strict && (sol.status!=:Solved || sol.max_natural_residual>1e-8)
        (!all(isfinite,cache.x) || !isfinite(sol.max_natural_residual)) && (cache.x.=valid_start)
        sol=solve_cached!(cache;output="no",tolerance=1e-8,time_limit=600,equilibrate_rows=true)
        push!(diagnostics,(grid=grid,scenario=scenario,year=y,stage=stage*"_scaled_polish",status=String(sol.status),
            residual=sol.max_natural_residual,seconds=sol.elapsed,requested_tolerance=1e-8);cols=:union)
        if sol.status!=:Solved && sol.max_natural_residual<=1e-8
            sol=solve_cached!(cache;output="no",tolerance=1e-8,time_limit=600)
            push!(diagnostics,(grid=grid,scenario=scenario,year=y,stage=stage*"_certify",status=String(sol.status),
                residual=sol.max_natural_residual,seconds=sol.elapsed,requested_tolerance=1e-8);cols=:union)
        end
    end
    CSV.write(joinpath(output_dir,"solve_diagnostics.csv"),diagnostics)
    strict && (sol.status!=:Solved || sol.max_natural_residual>1e-8) && error("Unacceptable MCP solve $stage $y")
    sol
end
function restore_parameters(values)
    all(isfinite,values) || error("Non-finite continuation parameters")
    for k in eachindex(values);set_value(JuMP.NonlinearParameter(m,k),values[k]);end
end
function continuation(old,target_params,y,stage;n=4)
    f=0.;step=1/n
    while f<1-1e-12
        next=min(1.,f+step);start=copy(cache.x)
        restore_parameters((1-next).*old.+next.*target_params)
        sol=solve_step(stage*"_"*string(round(next,digits=6)),y;strict=false)
        if sol.status==:Solved && sol.max_natural_residual<=1e-8
            f=next;step=min(1/n,step*1.5)
            if scenario=="A"
                CSV.write(joinpath(output_dir,"last_calibration_iterate.csv"),DataFrame(variable=cache.var_names,value=cache.x))
            end
        else
            residual=abs.(cache.x.-clamp.(cache.x.-cache.f,cache.lower,cache.upper))
            for k in sortperm(residual,rev=true)[1:8]
                println("FAILED_EQUATION ",cache.eq_names[k]," paired ",cache.var_names[k]," residual=",residual[k])
            end
            cache.x.=start;step/=2
            step>=1/4096 || error("Continuation cannot progress beyond $f in $stage $y")
            println("BISECT_CONTINUATION ",stage," ",y," accepted_fraction=",f," step=",step);flush(stdout)
        end
    end
end
function read_tfp(tech,y)
    key=tech=="solar" ? "pv" : "wind"
    [Float64(only(eachrow(ratios[(ratios.technology.==key).&(ratios.year.==y).&(ratios.region.==Region[r]),:])).baseline_tfp) for r in Regions]
end
function set_environment(y,stock)
    ts=read_tfp("solar",y);tw=read_tfp("wind",y)
    for r in Regions
        d=dyn[(Region[r],y)];d0=dyn[(Region[r],2017)]
        set_value(caps[r],stock[r]*.08)
        set_value(labs[r],sum(l0[:,r])*d.population_multiplier)
        set_value(lands[r],sum(lnd0[:,r]))
        for j in NatSec;set_value(natres[j,r],ns0[j,r]);end
        set_value(foreign_saving_target[r],save0[r]*d.GDP_target/gdp0[r])
        set_value(rgdp_exg[r],d.GDP_target)
        # The original Chinese saving-rate adjustment uses a growth-rate ratio.
        gr0=dyn[(Region[r],2018)].GDP_target/d0.GDP_target-1
        prev=max(2017,y-1);gr=d.GDP_target/dyn[(Region[r],prev)].GDP_target-1
        set_value(sav_dn[r],r==2 && y>2017 ? .5+.5*gr/gr0 : 1.)
        for j in Sectors;set_value(lambdae[j,r],1.015^(y-2017));end
        t=findfirst(==(y),Years);set_value(pco2_exg[r],pco2_exg_dyn[r,t])
        set_value(tfp_solar_exg[r],ts[r]);set_value(tfp_wind_exg[r],tw[r])
        if scenario=="A" && y<=2024
            for i in CalibrationRE
                desired=Float64(target[(Region[r],EcType[i],y)].target_generation_TWh)
                factor=generation_factor(i,r)
                set_value(generation_target[i,r],desired/factor)
                set_value(generation_scale[i,r],max(desired/factor,1e-4))
            end
        end
    end
    if scenario=="A" && y<=2030
        set_value(global_capacity_target,sum(Float64(target[(Region[r],EcType[i],y)].target_capacity_GW) for i in CalibrationRE,r in Regions))
        if y>2024
            # Future regional pathways set composition weights, not 72 hard
            # capacity constraints. The approved global trajectory is binding.
            for r in Regions
                proposed=copy(agen_elec0[:,r])
                for i in CalibrationRE
                    desired=Float64(target[(Region[r],EcType[i],y)].target_generation_TWh)/generation_factor(i,r)
                    proposed[i]=desired*pgent_elec0[i,r]^sigmaelec[r]/(totgen_elec0[r]*ptotgen_elec0[r]^sigmaelec[r])
                end
                normalizer=sum(proposed[i]*pgent_elec0[i,r]^(1-sigmaelec[r]) for i in ElecType)/ptotgen_elec0[r]^(1-sigmaelec[r])
                for i in ElecType;set_value(agen_reference[i,r],proposed[i]/normalizer);end
            end
        end
    end
end
function ces(a,x,b,z,s)
    if abs(s-1)<1e-10
        return exp((a*log(x)+b*log(z))/max(a+b,1e-30))
    end
    (a*x^(1-s)+b*z^(1-s))^(1/(1-s))
end
function fixed_cost(i,r,ak,al,pkv,plv,pene,pint,le)
    pva=ces(ak_elec[i,r],pkv*(1+trk_elec[i,r])/ak,al_elec[i,r],plv*(1+trl_elec[i,r])/al,sigmava_elec[i,r])
    pvae=ces(ava_elec[i,r],pva,aene_elec[i,r],pene/le,sigmavae_elec[i,r])
    ces(avae_elec[i,r],pvae,aint_elec[i,r],pint,sigmap_elec[i,r])*(1+trpd_elec[i,r])
end
function map_costs(y)
    result=ones(2,NumRegion)
    for r in Regions,(h,i) in enumerate([SolarPV,Wind])
        tech=h==1 ? "pv" : "wind"
        mult=ratio_map[(Region[r],tech,y)]
        result[h,r]=mult
        push!(cost_mapping,(year=y,region=Region[r],technology=tech,tfp_multiplier=mult,
            baseline_tfp=rv(lambdak_elec[i,r]),counterfactual_tfp=rv(lambdak_elec[i,r])*mult);cols=:union)
    end
    result
end
function accounts!(y)
    maxgap=0.
    for r in Regions
        h=sum(rv(consh[j,r])*(rv(pa[j,r])*(1+strh[j,r])+rv(etax_h[j,r])) for j in Goods)-rv(inch[r])+rv(savh[r])
        g=sum(rv(consg[j,r])*rv(pa[j,r])*(1+strg[j,r]) for j in Goods)-rv(incg[r])+rv(savg[r])
        invgap=sum(rv(inv[j,r])*rv(pa[j,r])*(1+strinv[j,r]) for j in Goods)-rv(tinv[r])*rv(ptinv_idx[r])
        kg=value(caps[r])-sum(rv(k[j,r]) for j in Sectors)
        lg=value(labs[r])-sum(rv(l[j,r]) for j in Sectors)
        tax=rv(emisrev[r])-rv(pco2[r])*rv(temit[r])
        vals=[h,g,invgap,kg,lg,tax,rv(walras[r])];maxgap=max(maxgap,maximum(abs.(vals)))
        push!(accounting,(grid=grid,scenario=scenario,year=y,region=Region[r],household=h,
          government=g,investment=invgap,capital=kg,labor=lg,carbon_revenue=tax,walras=rv(walras[r]),
          foreign_saving=rv(save[r]),max_absolute_gap=maximum(abs.(vals)));cols=:union)
    end
    abs(sum(rv.(save)))<1e-5 || error("Global external balance")
    maxgap<1e-5 || error("Budget/factor account gap=$maxgap")
    maxgap
end
function record!(y,price,status)
    for r in Regions
        prices=[rv(pa[j,r])*(1+strh[j,r])+rv(etax_h[j,r]) for j in Goods]
        surplus=[rv(consh[j,r])-minh[j,r] for j in Goods]
        minimum(surplus)>0 || error("Stone-Geary domain")
        lu=sum(muh[j,r]*log(surplus[k]/muh[j,r]) for (k,j) in enumerate(Goods) if muh[j,r]>0)
        lp=sum(muh[j,r]*log(prices[k]) for (k,j) in enumerate(Goods) if muh[j,r]>0)
        exports=sum(rv(imrr[j,r,d])*pfob0[j,r,d] for j in Goods,d in Regions)
        imports=sum(rv(imrr[j,d,r])*pcif0[j,d,r] for j in Goods,d in Regions)
        elecco2=sum(rv(emis_elec[j,i,r]) for j in FossilSec,i in ElecType)
        fossil=sum(rv(eint[j,i,r]) for j in FossilSec,i in Sectors_Non_Elec)+sum(rv(eint_elec[j,i,r]) for j in FossilSec,i in ElecType)+sum(rv(eh[j,r]) for j in FossilSec)
        push!(macrodata,(grid=grid,scenario=scenario,year=y,region=Region[r],real_GDP=rv(rgdp[r]),
          real_consumption=sum(rv(consh[j,r])*pa0[j,r] for j in Goods),real_investment=sum(rv(inv[j,r])*pa0[j,r] for j in Goods),
          nominal_investment=rv(tinv[r])*rv(ptinv_idx[r]),real_exports=exports,real_imports=imports,
          total_CO2=rv(temit[r]),power_CO2=elecco2,fossil_energy_Mtoe=fossil,
          carbon_price_2017USD_t=rv(pco2[r])*1000,carbon_increment_2024USD_t=price,
          carbon_revenue=rv(emisrev[r]),log_utility=lu,log_unit_expenditure=lp,
          generation_TWh=sum(generation_twh(i,r) for i in GenType),
          renewable_generation_TWh=sum(generation_twh(i,r) for i in CalibrationRE),
          renewable_capacity_proxy_GW=sum(capacity_gw(i,r) for i in CalibrationRE),
          electricity_price_index=rv(pp[PowerSec,r])/pp0[PowerSec,r],
          carbon_match_status=status,macro_productivity=rv(tfp[r]));cols=:union)
        for i in GenType
            factor=generation_factor(i,r)
            push!(powerdata,(grid=grid,scenario=scenario,year=y,region=Region[r],technology=EcType[i],
              generation_TWh=generation_twh(i,r),capacity_proxy_GW=capacity_gw(i,r),
              capacity_status="GENERATION_DIVIDED_BY_FIXED_REFERENCE_CF",reference_CF=Float64(phy[(Region[r],EcType[i])].capacity_factor),
              generation_price_2024USD_MWh=rv(pgent_elec[i,r])/factor*1000*deflator,
              capital_efficiency=rv(lambdak_elec[i,r]),labor_efficiency=rv(lambdal_elec[i,r]),
              capital_service_expenditure=rv(k_elec[i,r])*rv(pk[r]),preference=rv(agen_elec[i,r]));cols=:union)
        end
    end
end
function capital_next(y,next_y,stock)
    d=next_y-y;annuity=(1-(1-.05)^d)/.05
    next=[stock[r]*(1-.05)^d+rv(tinv[r])*annuity for r in Regions]
    minimum(next)>0 || error("Nonpositive next capital stock")
    for r in Regions
        push!(transitions,(grid=grid,scenario=scenario,year=y,next_year=next_y,region=Region[r],
          interval_years=d,opening_stock=stock[r],annual_real_investment=rv(tinv[r]),
          survival=(1-.05)^d,investment_annuity=annuity,next_stock=next[r],
          identity_residual=next[r]-stock[r]*(1-.05)^d-rv(tinv[r])*annuity);cols=:union)
    end
    next
end
function carbon_root(y,targetCO2)
    fixedparams=copy(m.nlp_model.parameters);startx=copy(cache.x)
    records=NamedTuple[]
    function evaluate(price)
        restore_parameters(fixedparams)
        for r in Regions;set_value(pco2_exg[r],fixedparams[pco2_exg[r].index]+price/deflator/1000);end
        sol=solve_step("carbon_"*string(price),y)
        co2=sum(rv.(temit));gap=co2-targetCO2
        push!(carbon_trials,(grid=grid,year=y,price_2024USD_t=price,CO2=co2,target_CO2=targetCO2,
          gap_Mt=gap,residual=sol.max_natural_residual,status=String(sol.status));cols=:union)
        rec=(price=price,gap=gap,x=copy(cache.x),params=copy(m.nlp_model.parameters));push!(records,rec)
        CSV.write(joinpath(output_dir,"carbon_trials.csv"),carbon_trials)
        println("CARBON ",y," price=",price," gap=",gap);flush(stdout)
        rec
    end
    ok(e)=abs(e.gap)<=min(1.,.0001*targetCO2)
    zero=evaluate(0.);chosen=zero;status="MATCHED"
    if !ok(zero)
        if zero.gap<0
            status="ZERO_PRICE_ALREADY_BELOW_BASELINE_NO_POSITIVE_COMPENSATION"
        else
            left=zero;right=nothing
            for price in [1.,2.,5.,10.,20.,40.,80.,160.,320.,640.,1280.,2560.,5120.,10240.]
                e=evaluate(price)
                if ok(e);right=e;break;end
                if e.gap<0;right=e;break;end
                left=e
            end
            if right===nothing
                chosen=zero;status="NO_MATCH_ON_NONNEGATIVE_PRICE_GRID"
            else
                chosen=right
                for _ in 1:40
                    ok(chosen) && break
                    chosen=evaluate((left.price+right.price)/2)
                    if chosen.gap>0;left=chosen;else;right=chosen;end
                end
                ok(chosen) || error("Carbon matching tolerance not met")
            end
        end
    end
    cache.x.=chosen.x;restore_parameters(chosen.params)
    solve_step("accepted_carbon",y)
    sorted=sort(records,by=x->x.price);nonmono=any(sorted[k+1].gap>sorted[k].gap+1e-4 for k in 1:length(sorted)-1)
    push!(carbon_matches,(grid=grid,year=y,target_CO2=targetCO2,CO2=sum(rv.(temit)),
      price_2024USD_t=chosen.price,gap_Mt=sum(rv.(temit))-targetCO2,
      relative_gap=(sum(rv.(temit))-targetCO2)/targetCO2,status=status,nonmonotonic_grid=nonmono);cols=:union)
    chosen.price,status
end
function run_experiment()
    println("MCP variables ",length(cache.x));flush(stdout)
    signature=bytes2hex(sha256(join(cache.var_names,"\n")))
    stock=copy(cap_supp[:,1])./.08
    resume_year=2016
    for y in reverse(Years)
        p=joinpath(output_dir,"state_"*string(y)*".jls")
        if isfile(p)
            snap=deserialize(p);snap.signature==signature || error("Variable signature changed")
            cache.x.=snap.x;restore_parameters(snap.parameters);stock=[snap.next_stock[r] for r in Regions];resume_year=y
            for (name,df) in [("solve_diagnostics",diagnostics),("macro",macrodata),("power",powerdata),
              ("accounting",accounting),("cost_mapping",cost_mapping),("calibration",calibration),
              ("carbon_trials",carbon_trials),("carbon_matches",carbon_matches),("capital_transitions",transitions)]
                f=joinpath(output_dir,name*".csv")
                if isfile(f)
                    old=CSV.read(f,DataFrame);filter!(:year=><=(y),old);append!(df,old;cols=:union)
                end
            end
            println("RESUME ",scenario," through ",y);flush(stdout);break
        end
    end
    if resume_year==2016
        initial_parameters=copy(m.nlp_model.parameters)
        set_environment(2017,stock)
        all(isfinite,m.nlp_model.parameters) || error("Initial environment contains non-finite values: $(findall(x->!isfinite(x),m.nlp_model.parameters))")
        restore_parameters(initial_parameters)
        solve_step("unshocked_core",2017)
    end
    for (t,y) in enumerate(Years)
        (y<=resume_year || y>stop_year) && continue
        if scenario=="A"
            # Switch closure at the accepted equilibrium, where the old targets
            # already hold. Then continue economic inputs with closure fixed.
            # Interpolating the closure itself creates a singular final step.
            set_value(calibrate_gdp,1.)
            set_value(calibrate_power,y<=2024 ? 1. : 0.)
            set_value(calibrate_global_capacity,2025<=y<=2030 ? 1. : 0.)
        end
        previous=copy(m.nlp_model.parameters)
        basestate=nothing;mult=ones(2,NumRegion)
        if scenario=="A"
            set_environment(y,stock)
            set_value(calibrate_gdp,1.);set_value(calibrate_power,y<=2024 ? 1. : 0.)
            set_value(calibrate_global_capacity,2025<=y<=2030 ? 1. : 0.)
            if y>2030
                baseline2030=deserialize(joinpath(output_dir,"state_2030.jls"))
                for i in ElecType,r in Regions;set_value(agen_reference[i,r],baseline2030.preference[i,r]);end
                for r in Regions
                    set_value(tfp_solar_exg[r],baseline2030.parameters[tfp_solar_exg[r].index])
                    set_value(tfp_wind_exg[r],baseline2030.parameters[tfp_wind_exg[r].index])
                end
            end
            desired=copy(m.nlp_model.parameters)
            continuation(previous,desired,y,"calibrate";n=y==2017 ? 4 : 4)
            pref=rv.(agen_elec);mtfp=rv.(tfp)
            minimum(pref)>=-1e-8 || error("Negative calibrated source preference")
            for r in Regions
                set_value(tfp_exg[r],mtfp[r])
                set_value(tfp_solar_exg[r],rv(lambdak_elec[SolarPV,r]))
                set_value(tfp_wind_exg[r],rv(lambdak_elec[Wind,r]))
                for i in ElecType;set_value(agen_reference[i,r],pref[i,r]);end
            end
            set_value(calibrate_gdp,0.);set_value(calibrate_power,0.);set_value(calibrate_global_capacity,0.)
            solve_step("baseline_fixed_parameter_replay",y)
            y<=2030 && abs(sum(capacity_gw(i,r) for i in CalibrationRE,r in Regions)-value(global_capacity_target))>1e-3 && error("Global renewable calibration failed")
            for r in Regions
                gdptarget=dyn[(Region[r],y)].GDP_target
                abs(rv(rgdp[r])/gdptarget-1)<1e-7 || error("GDP calibration failed")
                for i in CalibrationRE
                    cap=capacity_gw(i,r)
                    desiredcap=y<=2030 ? Float64(target[(Region[r],EcType[i],y)].target_capacity_GW) : NaN
                    y<=2024 && abs(cap-desiredcap)>1e-3 && error("Historical renewable calibration failed")
                    push!(calibration,(grid=grid,year=y,region=Region[r],technology=EcType[i],
                       GDP=rv(rgdp[r]),GDP_target=gdptarget,capacity_proxy_GW=cap,target_GW=desiredcap,
                       preference=rv(agen_elec[i,r]),macro_tfp=rv(tfp[r]));cols=:union)
                end
            end
            mult=map_costs(y)
        else
            basepath=joinpath(runtime,"equilibria_final",grid,"A","state_"*string(y)*".jls")
            isfile(basepath) || error("Missing completed A for $y")
            basestate=deserialize(basepath);restore_parameters(basestate.parameters)
            # Same baseline coefficients, but own inherited stocks and the same direct cost shock.
            for r in Regions
                set_value(caps[r],stock[r]*.08)
                set_value(tfp_solar_exg[r],value(tfp_solar_exg[r])*basestate.tfp_multiplier[1,r])
                set_value(tfp_wind_exg[r],value(tfp_wind_exg[r])*basestate.tfp_multiplier[2,r])
            end
            if scenario=="C"
                extra=parse(Float64,get(ENV,"LEGACY_EXTRA_CARBON_PRICE","0"))
                for r in Regions;set_value(pco2_exg[r],value(pco2_exg[r])+extra/deflator/1000);end
            end
            desired=copy(m.nlp_model.parameters)
            # Initialize from the same node's baseline equilibrium, then apply own stocks and shocks.
            cache.x.=basestate.x
            continuation(basestate.parameters,desired,y,"scenario";n=4)
            mult=basestate.tfp_multiplier
        end
        price=0.;matchstatus="NOT_APPLICABLE"
        if scenario=="C"
            price=parse(Float64,get(ENV,"LEGACY_EXTRA_CARBON_PRICE","0"))
            matchstatus="UNIFORM_CAPACITY_MATCHING_INCREMENT"
        end
        accounts!(y);record!(y,price,matchstatus)
        nextstock=t<NumYears ? capital_next(y,Years[t+1],stock) : copy(stock)
        persist_tables()
        snapshot=(signature=signature,year=y,scenario=scenario,x=copy(cache.x),parameters=copy(m.nlp_model.parameters),
          opening_stock=copy(stock),next_stock=nextstock,tfp_multiplier=mult,preference=rv.(agen_elec),
          global_co2=sum(rv.(temit)),carbon_increment=price,carbon_match_status=matchstatus)
        serialize(joinpath(output_dir,"state_"*string(y)*".jls"),snapshot)
        CSV.write(joinpath(output_dir,"completion.csv"),DataFrame(grid=[grid],scenario=[scenario],last_year=[y],complete=[y==Years[end]],
          MCP_residual=[diagnostics.residual[end]],global_CO2=[sum(rv.(temit))],
          global_RE_capacity_proxy_GW=[sum(capacity_gw(i,r) for i in CalibrationRE,r in Regions)]))
        stock=nextstock
        println("ACCEPTED ",grid," ",scenario," ",y);flush(stdout)
    end
end
