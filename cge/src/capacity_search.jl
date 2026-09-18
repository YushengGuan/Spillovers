function run_capacity_search()
    root=joinpath(runtime,"equilibria_final",grid)
    initialparams=copy(m.nlp_model.parameters);initialx=copy(cache.x)
    trials=DataFrame()
    searchfile=joinpath(root,"capacity_price_search.csv")
    isfile(searchfile) && append!(trials,CSV.read(searchfile,DataFrame);cols=:union)
    function evaluate(price;final=false)
        rid=final ? "C" : "trial_"*replace(string(round(price,digits=9)),'.'=>'p')
        global output_dir=joinpath(root,rid);mkpath(output_dir)
        global stop_year=final ? 2050 : 2030
        ENV["LEGACY_EXTRA_CARBON_PRICE"]=string(price)
        cache.x.=initialx;restore_parameters(initialparams)
        for df in [diagnostics,macrodata,powerdata,accounting,cost_mapping,calibration,carbon_trials,carbon_matches,transitions];empty!(df);end
        run_experiment()
        d=CSV.read(joinpath(output_dir,"power.csv"),DataFrame)
        cap=sum(d[(d.year.==2030).&(d.technology.∈Ref([EcType[i] for i in CalibrationRE])),:capacity_proxy_GW])
        if !final
            push!(trials,(run_id=rid,additional_price_2024USD_t=price,capacity_GW=cap,gap_GW=cap-11000.);cols=:union)
            CSV.write(searchfile,trials)
        end
        println("PRICE_TRIAL_ACCEPTED ",price," CAPACITY ",cap);flush(stdout)
        (price=price,cap=cap,gap=cap-11000.)
    end
    b=CSV.read(joinpath(root,"B","power.csv"),DataFrame)
    lowcap=sum(b[(b.year.==2030).&(b.technology.∈Ref([EcType[i] for i in CalibrationRE])),:capacity_proxy_GW])
    low=(price=0.,cap=lowcap,gap=lowcap-11000.)
    if nrow(trials)==0 || !any(trials.additional_price_2024USD_t.==0.) # initialized below for first search
        push!(trials,(run_id="B",additional_price_2024USD_t=0.,capacity_GW=lowcap,gap_GW=low.gap);cols=:union)
    end
    CSV.write(searchfile,trials)
    chosen=low;status="no_increase_needed"
    if low.gap<-.05
        high=evaluate(5.)
        while high.gap<0 && high.price<4096;high=evaluate(2high.price);end
        high.gap>=0 || error("No nonnegative capacity price bracket")
        chosen=high;status="matched"
        for iter in 1:35
            abs(chosen.gap)<.05 && break
            x=clamp(low.price+(high.price-low.price)*(-low.gap)/(high.gap-low.gap),low.price+.05*(high.price-low.price),high.price-.05*(high.price-low.price))
            z=evaluate(x);chosen=z
            if z.gap<0;low=z;else;high=z;end
        end
        abs(chosen.gap)<.05 || error("Capacity matching failed")
    end
    evaluate(chosen.price;final=true)
    CSV.write(joinpath(root,"capacity_policy_selected.csv"),DataFrame(additional_price_2024USD_t=[chosen.price],target_GW=[11000.],capacity_GW=[chosen.cap],gap_GW=[chosen.gap],status=[status]))
end
