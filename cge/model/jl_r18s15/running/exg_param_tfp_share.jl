#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize NLparameters
#---     May, 2023

@NLparameters m begin
    # -- accumulation of different factors
    caps[rr = Regions] == cap_supp[rr, 1]
    labs[rr = Regions] == lab_supp[rr, 1]
    # tarabs[z = AEZsType, rr = Regions] == tarab0[z, rr]
    lands[rr = Regions] == lnd_supp[rr, 1]
    natres[j = NatSec, rr = Regions] == ns_supp[j, rr, 1]
    lambdae[i = Sectors, r = Regions] == 1
    lambdae_elec[i = ElecType, r = Regions] == 1

    # -- calibration on TFP parameters
    tfp_exg[rr = Regions] == 1
    rgdp_exg[rr = Regions] == rgdp_bau_exg[rr, 1]
    tfp_solar_exg[rr = Regions] == 1
    tfp_wind_exg[rr = Regions] == 1

    # -- calibration on electricity share parameter
    agen_reference[i = ElecType, r = Regions] == agen_elec0[i, r]

    # -- carbon pricing policy exogenous variables
    pco2_exg[rr = Regions] == 0
    # cap_exg[rr = Regions] == tghgeq0[CO2, rr]

    # ch4_g_exg == sum(tghgeq0[CH4, rr] for rr in Regions)
    # ch4_exg[rr = Regions] == tghgeq0[CH4, rr]
    # fac_ghgeq_prod[p = GHGType_in_Model, i = Sectors_Non_Elec, rr = Regions] == fac_ghgeq_prod0[p, i, rr]

    # -- food loss and waste related exogenous variables
    # flw_farm_red[i = Sectors, rr = Regions] == flw_farm[i, rr]
    # lambdafd_int[j = IntSec, i = Sectors, rr = Regions] == 1
    # lambdafd_h[j = Goods, rr = Regions] == 1
    sav_dn[rr = Regions] == sav_dyn[rr, 1]
end
@NLparameters m begin
    calibrate_gdp == 0.0
    calibrate_power == 0.0
    calibrate_global_capacity == 0.0
    global_capacity_target == sum(gen_elec0[i,r]*generation_to_capacity[i,r] for i in CalibrationRE,r in Regions)
    generation_target[i=ElecType,r=Regions] == gen_elec0[i,r]
    generation_scale[i=ElecType,r=Regions] == max(gen_elec0[i,r],1e-4)
end
@variables m begin
    agen_elec[i=ElecType,r=Regions], (start=agen_elec0[i,r])
    nonrenewable_preference_scale[r=Regions], (start=1.0)
    global_tfp_factor >= 1e-6, (start=1.0)
end
function eq_calibration_switches()
    @mapping(m, eq_re_calibration[i in CalibrationRE,r in Regions],
      calibrate_power*(gen_elec[i,r]-generation_target[i,r])/generation_scale[i,r]
      +(1-calibrate_power)*(agen_elec[i,r]-agen_reference[i,r]*global_tfp_factor))
    @complementarity(m,eq_re_calibration,agen_elec[CalibrationRE,Regions])
    @mapping(m, eq_other_preferences[i in setdiff(ElecType,CalibrationRE),r in Regions],
       agen_elec[i,r]-agen_reference[i,r]*(1-calibrate_power+calibrate_power*nonrenewable_preference_scale[r]))
    @complementarity(m,eq_other_preferences,agen_elec[setdiff(ElecType,CalibrationRE),Regions])
    @mapping(m, eq_preference_normalization[r in Regions],
       calibrate_power*(sum(agen_elec[i,r]*pgent_elec0[i,r]^(1-sigmaelec[r]) for i in ElecType)/ptotgen_elec0[r]^(1-sigmaelec[r])-1)
       +(1-calibrate_power)*(nonrenewable_preference_scale[r]-1))
    @complementarity(m,eq_preference_normalization,nonrenewable_preference_scale)
    @mapping(m, eq_global_capacity,
      calibrate_global_capacity*(sum(gen_elec[i,r]*generation_to_capacity[i,r] for i in CalibrationRE,r in Regions)/global_capacity_target-1)
      +(1-calibrate_global_capacity)*(global_tfp_factor-1))
    @complementarity(m,eq_global_capacity,global_tfp_factor)
end
