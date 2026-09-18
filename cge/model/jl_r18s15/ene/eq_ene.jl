#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_ene()
    # energy demand of all agents
    @mapping(m, eq_eint[j in EnergySec, i in Sectors_Non_Elec, r in Regions], eint[j, i, r] - enefac_int[j, i, r] * qint[j, i, r])
    @complementarity(m, eq_eint, eint)

    @mapping(m, eq_eint_elec[j in EnergySec, i in ElecType, r in Regions], eint_elec[j, i, r] - enefac_elec[j, i, r] * qint_elec[j, i, r])
    @complementarity(m, eq_eint_elec, eint_elec)

    @mapping(m, eq_eh[j in EnergySec, r in Regions], eh[j, r] - enefac_h[j, r] * consh[j, r])
    @complementarity(m, eq_eh, eh)

    # energy-related CO2 emissions of all agents
    @mapping(m, eq_emis_int[j in FossilSec, i in Sectors_Non_Elec, r in Regions], emis_int[j, i, r] - emisfac_int[j, i, r] * qint[j, i, r])
    @complementarity(m, eq_emis_int, emis_int)

    @mapping(m, eq_emis_elec[j in FossilSec, i in ElecType, r in Regions], emis_elec[j, i, r] - emisfac_elec[j, i, r] * qint_elec[j, i, r])
    @complementarity(m, eq_emis_elec, emis_elec)

    @mapping(m, eq_emis_h[j in FossilSec, r in Regions], emis_h[j, r] - emisfac_h[j, r] * consh[j, r])
    @complementarity(m, eq_emis_h, emis_h)

    # total emissions
    @mapping(m, eq_temit[rr in Regions], temit[rr] - sum(sum(emis_int[j, i, rr] for j in FossilSec) for i in Sectors_Non_Elec) - sum(sum(emis_elec[j, i, rr] for j in FossilSec) for i in ElecType) - sum(emis_h[j, rr] for j in FossilSec))
    @complementarity(m, eq_temit, temit)

    @mapping(m, eq_gemit, gemit - sum(temit[rr] for rr in Regions))
    @complementarity(m, eq_gemit, gemit)
end