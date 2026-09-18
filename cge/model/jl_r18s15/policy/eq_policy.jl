#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_policy(cp_flag)
    # carbon pricing and revenue
    if cp_flag == "Tax"
        @mapping(m, eq_pco2[rr in Regions], pco2[rr] - pco2_exg[rr])
        @complementarity(m, eq_pco2, pco2)
        
    elseif cp_flag == "Cap"
        @mapping(m, eq_pco2[rr in Regions], cap_exg[rr] - temit[rr])
        @complementarity(m, eq_pco2, pco2)

    elseif cp_flag == "Cap_g"
        @mapping(m, eq_pco2_g, cap_g_exg - sum(temit[rr] for rr in Regions))
        @complementarity(m, eq_pco2_g, pco2_g)

        @mapping(m, eq_pco2[rr in Regions], pco2[rr] - pco2_g)
        @complementarity(m, eq_pco2, pco2)
    end

    @mapping(m, eq_etax[j in FossilSec, i in Sectors_Non_Elec, rr in Regions], etax[j, i, rr] - emisfac_int[j, i, rr] * pco2[rr])
    @complementarity(m, eq_etax, etax)

    @mapping(m, eq_etax_elec[j in EnergySec, i in ElecType, rr in Regions], etax_elec[j, i, rr] - emisfac_elec[j, i, rr] * pco2[rr])
    @complementarity(m, eq_etax_elec, etax_elec)

    @mapping(m, eq_etax_h[j in Goods, rr in Regions], etax_h[j, rr] - emisfac_h[j, rr] * pco2[rr])
    @complementarity(m, eq_etax_h, etax_h)
    
    # @mapping(m, eq_etax_nco2eq_prod[i in Sectors, rr in Regions], etax_nco2eq_prod[i, rr])
    # @complementarity(m, eq_etax_nco2eq_prod, etax_nco2eq_prod)

    @mapping(m, eq_emisrev[rr in Regions], emisrev[rr] - (sum(sum(etax[j, i, rr] * qint[j, i, rr] for j in FossilSec) for i in Sectors_Non_Elec) + sum(sum(etax_elec[j, i, rr] * qint_elec[j, i, rr] for j in FossilSec) for i in ElecType) + sum(etax_h[j, rr] * consh[j, rr] for j in FossilSec)))
    @complementarity(m, eq_emisrev, emisrev)
end