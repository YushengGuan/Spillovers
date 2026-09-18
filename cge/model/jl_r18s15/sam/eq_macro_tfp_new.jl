#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_macro(dyn_flag = "TFP")
    if dyn_flag == "TFP"
        # dynamic Process
        @mapping(m, eq_tfp_exg[rr in Regions], calibrate_gdp*(rgdp[rr]/rgdp_exg[rr]-1)+(1-calibrate_gdp)*(tfp[rr]-tfp_exg[rr]))
        @complementarity(m, eq_tfp_exg, tfp)
        
    elseif dyn_flag == "GDP"
        @mapping(m, eq_tfp_exg[rr in Regions], rgdp[rr] - rgdp_exg[rr])
        @complementarity(m, eq_tfp_exg, tfp)
    end

    @mapping(m, eq_lambdal[i in Sectors, rr in Regions], lambdal[i, rr] - tfp[rr])
    @complementarity(m, eq_lambdal, lambdal)

    @mapping(m, eq_lambdak[i in Sectors, rr in Regions], lambdak[i, rr] - tfp[rr])
    @complementarity(m, eq_lambdak, lambdak)
    
    @mapping(m, eq_lambdal_elec[i in OHElecType, rr in Regions], lambdal_elec[i, rr] - tfp[rr])
    @complementarity(m, eq_lambdal_elec, lambdal_elec[OHElecType, Regions])

    @mapping(m, eq_lambdak_elec[i in OHElecType, rr in Regions], lambdak_elec[i, rr] - tfp[rr])
    @complementarity(m, eq_lambdak_elec, lambdak_elec[OHElecType, Regions])

    @mapping(m, eq_lambdal_elecF[i in FsElecType, rr in Regions], lambdal_elec[i, rr] - tfp[rr])
    @complementarity(m, eq_lambdal_elecF, lambdal_elec[FsElecType, Regions])

    @mapping(m, eq_lambdak_elecF[i in FsElecType, rr in Regions], lambdak_elec[i, rr] - tfp[rr])
    @complementarity(m, eq_lambdak_elecF, lambdak_elec[FsElecType, Regions])

    @mapping(m, eq_lambdal_solar[i in [SolarPV], rr in Regions], lambdal_elec[i, rr] - tfp_solar_exg[rr])
    @complementarity(m, eq_lambdal_solar, lambdal_elec[[SolarPV], Regions])

    @mapping(m, eq_lambdak_solar[i in [SolarPV], rr in Regions], lambdak_elec[i, rr] - tfp_solar_exg[rr])
    @complementarity(m, eq_lambdak_solar, lambdak_elec[[SolarPV], Regions])

    @mapping(m, eq_lambdal_wind[i in [Wind], rr in Regions], lambdal_elec[i, rr] - tfp_wind_exg[rr])
    @complementarity(m, eq_lambdal_wind, lambdal_elec[[Wind], Regions])

    @mapping(m, eq_lambdak_wind[i in [Wind], rr in Regions], lambdak_elec[i, rr] - tfp_wind_exg[rr])
    @complementarity(m, eq_lambdak_wind, lambdak_elec[[Wind], Regions])

    @mapping(m, eq_lambdal_hydro[i in [Hydro], rr in Regions], lambdal_elec[i, rr] - ((tfp[rr]-1)*0.2+1))
    @complementarity(m, eq_lambdal_hydro, lambdal_elec[[Hydro], Regions])

    @mapping(m, eq_lambdak_hydro[i in [Hydro], rr in Regions], lambdak_elec[i, rr] - ((tfp[rr]-1)*0.2+1))
    @complementarity(m, eq_lambdak_hydro, lambdak_elec[[Hydro], Regions])

    # @mapping(m, eq_lambdalnd[i in AgriSec, rr in Regions], lambdalnd[i, rr] - tfp[rr])
    # @complementarity(m, eq_lambdalnd, lambdalnd)

    # @mapping(m, eq_lambdans[i in NatSec, rr in Regions], lambdak[i, rr] - tfp[rr])
    # @complementarity(m, eq_lambdans, lambdans)

    # Price of Production factors
    @mapping(m, eq_pk[r in Regions], caps[r] - sum(k[i, r] for i in Sectors))
    @complementarity(m, eq_pk, pk)

    @mapping(m, eq_pl[r in Regions], labs[r] - sum(l[i, r] for i in Sectors))
    @complementarity(m, eq_pl, pl)

    @mapping(m, eq_plnd[r in Regions], lands[r] - sum(lnd[i, r] for i in AgriSec))
    @complementarity(m, eq_plnd, plnd)

    @mapping(m, eq_pns[i in NatSec, r in Regions], natres[i, r] - ns[i, r])
    @complementarity(m, eq_pns, pns)

    # macro variables
    @mapping(m, eq_ngdp[rr in Regions], sum((consh[j, rr] + consg[j, rr] + inv[j, rr]) * pa[j, rr] + sum(imrr[j, rr, r] * (1 + ter[j, rr, r]) * pe[j, rr] for r in Regions) - sum(imrr[j, r, rr] * ((1 + ter[j, r, rr]) * pe[j, r] + qtmg0[j, r, rr] * ptrst) for r in Regions) for j in Goods) + pp[TransSec, rr] * qtrs[rr] - ngdp[rr])
    @complementarity(m, eq_ngdp, ngdp)

    @mapping(m, eq_rgdp[rr in Regions], sum((consh[j, rr] + consg[j, rr] + inv[j, rr]) * pa0[j, rr] + sum(imrr[j, rr, r] * pfob0[j, rr, r] for r in Regions) - sum(imrr[j, r, rr] * pcif0[j, r, rr] for r in Regions) for j in Goods) + pp0[TransSec, rr] * qtrs[rr] - rgdp[rr])
    @complementarity(m, eq_rgdp, rgdp)

    @mapping(m, eq_pgdp[rr in Regions], pgdp[rr] * rgdp[rr] - ngdp[rr])
    @complementarity(m, eq_pgdp, pgdp)
end