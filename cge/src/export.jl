function export_states()
    energy=DataFrame();sectors=DataFrame();extras=DataFrame();audits=DataFrame()
    root=joinpath(runtime,"equilibria_final",grid)
    for sid in ["A","B","C"],y in Years
        state=deserialize(joinpath(root,sid,"state_"*string(y)*".jls"))
        cache.x.=state.x;restore_parameters(state.parameters)
        for r in Regions
            p=[rv(pa[j,r])*(1+strh[j,r])+rv(etax_h[j,r]) for j in Goods]
            lp=sum(muh[j,r]*log(p[k]) for (k,j) in enumerate(Goods) if muh[j,r]>0)
            ex=sum(rv(imrr[j,r,d])*(1+ter[j,r,d])*rv(pe[j,r]) for j in Goods,d in Regions)
            im=sum(rv(imrr[j,d,r])*((1+ter[j,d,r])*rv(pe[j,d])+qtmg0[j,d,r]*rv(ptrst)) for j in Goods,d in Regions)
            push!(extras,(scenario=sid,year=y,region=Region[r],wage=rv(pl[r]),household_price_index=exp(lp),government_income=rv(incg[r]),exports_FOB=ex,imports_CIF=im,foreign_saving=rv(save[r]),capital_return=rv(pk[r]));cols=:union)
            push!(audits,(scenario=sid,year=y,region=Region[r],pv_tfp=value(tfp_solar_exg[r]),wind_tfp=value(tfp_wind_exg[r]),macro_tfp=value(tfp_exg[r]),calibrate_gdp=value(calibrate_gdp),calibrate_power=value(calibrate_power),calibrate_capacity=value(calibrate_global_capacity));cols=:union)
            for j in Sectors
                push!(sectors,(scenario=sid,year=y,region=Region[r],sector=Sector[j],real_output=rv(prod[j,r])*pp0[j,r],labor_demand=rv(l[j,r]),capital_demand=rv(k[j,r]));cols=:union)
            end
            for (k,j) in enumerate(EnergySec)
                hh=rv(eh[j,r]);ind=sum(rv(eint[j,i,r]) for i in setdiff(Sectors_Non_Elec,EnergySec))
                push!(energy,(scenario=sid,year=y,region=Region[r],fuel=EneType[k],household_Mtoe=hh,nonenergy_industries_Mtoe=ind,energy_industries_Mtoe=sum(rv(eint[j,i,r]) for i in intersect(Sectors_Non_Elec,EnergySec)),power_sector_Mtoe=sum(rv(eint_elec[j,i,r]) for i in ElecType),modeled_final_demand_Mtoe=hh+ind);cols=:union)
            end
        end
    end
    for (name,df) in [("energy_balances",energy),("sector",sectors),("macro_extras",extras),("input_audit",audits)]
        CSV.write(joinpath(root,name*".csv"),df)
    end
    export_detailed_diagnostics()
    println("EXPORTED_ALL_EQUILIBRIA")
end

function export_detailed_diagnostics()
    diagnostic_root=joinpath(runtime,"equilibria_final",grid)
rows=DataFrame();powerrows=DataFrame();checks=DataFrame()
for sid in ["A","B","C"], y in [2030,2050]
    state=deserialize(joinpath(runtime,"equilibria_final",grid,sid,"state_"*string(y)*".jls"))
    cache.x.=state.x;restore_parameters(state.parameters)
    for r in Regions
        subtotal=0.
        for i in Sectors_Non_Elec
            v=sum(rv(emis_int[j,i,r]) for j in FossilSec)
            push!(rows,(scenario=sid,year=y,region=Region[r],sector=Sector[i],CO2_Mt=v))
            subtotal+=v
        end
        pe=sum(rv(emis_elec[j,i,r]) for j in FossilSec,i in ElecType)
        push!(rows,(scenario=sid,year=y,region=Region[r],sector="Power",CO2_Mt=pe))
        hh=sum(rv(emis_h[j,r]) for j in FossilSec)
        push!(rows,(scenario=sid,year=y,region=Region[r],sector="Households",CO2_Mt=hh))
        gap=subtotal+pe+hh-rv(temit[r])
        abs(gap)<1e-6 || error("Emission identity failed")
        push!(checks,(scenario=sid,year=y,region=Region[r],total_CO2_Mt=rv(temit[r]),power_CO2_Mt=pe,identity_gap=gap))
        for i in ElecType
            push!(powerrows,(scenario=sid,year=y,region=Region[r],technology=EcType[i],CO2_Mt=sum(rv(emis_elec[j,i,r]) for j in FossilSec)))
        end
    end
    println("READ_STATE ",sid," ",y);flush(stdout)
end
CSV.write(joinpath(diagnostic_root,"sector_emissions.csv"),rows)
CSV.write(joinpath(diagnostic_root,"power_emissions.csv"),powerrows)
CSV.write(joinpath(diagnostic_root,"emissions_checks.csv"),checks)
println("EXPORTED ",nrow(rows)," sector rows; ",nrow(powerrows)," technology rows; identities pass")

consumption=DataFrame();incomes=DataFrame()
for sid in ["A","B","C"], y in [2030,2050]
    state=deserialize(joinpath(runtime,"equilibria_final",grid,sid,"state_"*string(y)*".jls"))
    cache.x.=state.x;restore_parameters(state.parameters)
    for r in Regions
        expend=0.
        for j in Goods
            cp=rv(pa[j,r])*(1+strh[j,r])+rv(etax_h[j,r])
            q=rv(consh[j,r]);expend+=q*cp
            push!(consumption,(scenario=sid,year=y,region=Region[r],good=Good[j],quantity=q,consumer_price=cp,expenditure_2024USD_bn=q*cp*deflator,real_consumption_2024USD_bn=q*pa0[j,r]*deflator))
        end
        gap=expend-(rv(inch[r])-rv(savh[r]))
        abs(gap)<1e-6 || error("Household expenditure identity failed")
        push!(incomes,(scenario=sid,year=y,region=Region[r],household_income=rv(inch[r])*deflator,household_savings=rv(savh[r])*deflator,labor_income=rv(tlinc[r])*deflator,household_capital_income=akh[r]*rv(tkinc[r])*deflator,land_income=rv(tlndinc[r])*deflator,resource_income=rv(tnsinc[r])*deflator,government_income=rv(incg[r])*deflator,carbon_revenue=rv(emisrev[r])*deflator,expenditure_gap=gap*deflator))
    end
    println("READ_STATE ",sid," ",y);flush(stdout)
end
CSV.write(joinpath(diagnostic_root,"household_consumption.csv"),consumption)
CSV.write(joinpath(diagnostic_root,"household_incomes.csv"),incomes)
println("EXPORTED ",nrow(consumption)," household-good rows; budgets pass")

end
