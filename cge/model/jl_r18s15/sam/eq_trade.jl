#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_trade()
    # relationship between production and supply when considering the transport demand of international trade
    @mapping(m, eq_prod_trans[r in Regions], qs[TransSec, r] - (prod[TransSec, r] - qtrs[r]))
    @complementarity(m, eq_prod_trans, prod[TransSec, Regions])

    @mapping(m, eq_prod_oth[j in NonTransSec, r in Regions], qs[j, r] - prod[j, r])
    @complementarity(m, eq_prod_oth, prod[NonTransSec, Regions])

    # CET-1 Structure
    @mapping(m, eq_dms[j in Goods, r in Regions], dms[j, r] * pdm[j, r] ^ sigmae[j, r] - adms[j, r] * qs[j, r] * pp[j, r] ^ sigmae[j, r])
    @complementarity(m, eq_dms, dms)

    @mapping(m, eq_ext[j in Goods, r in Regions], ext[j, r] * pe[j, r] ^ sigmae[j, r] - aext[j, r] * qs[j, r] * pp[j, r] ^ sigmae[j, r])
    @complementarity(m, eq_ext, ext)

    @mapping(m, eq_qs[j in Goods, r in Regions], aext[j, r] * pe[j, r] ^ (1 - sigmae[j, r]) + adms[j, r] * pdm[j, r] ^ (1 - sigmae[j, r]) - pp[j, r] ^ (1 - sigmae[j, r]))
    @complementarity(m, eq_qs, qs)

    @mapping(m, eq_pe[j in Goods, r in Regions], ext[j, r] - sum(imrr[j, r, rr] for rr in Regions))
    @complementarity(m, eq_pe, pe)

    # @mapping(m, eq_pfob[j in Goods, r in Regions, rr in Regions], pfob[j, r, rr] - (1 + ter[j, r, rr]) * pe[j, r])
    # @complementarity(m, eq_pfob, pfob)

    # @mapping(m, eq_pcif[j in Goods, r in Regions, rr in Regions], pcif[j, r, rr] - (pfob[j, r, rr] + qtmg0[j, r, rr] * ptrst))
    # @complementarity(m, eq_pcif, pcif)

    # CES level 1
    @mapping(m, eq_tdd[j in Goods, rr in Regions], tdd[j, rr] - sum(qint[j, i, rr] for i in Sectors) - consh[j, rr] - consg[j, rr] - inv[j, rr])
    @complementarity(m, eq_tdd, tdd)
    
    @mapping(m, eq_pdm[j in Goods, rr in Regions], dms[j, rr] - dmd[j, rr])
    @complementarity(m, eq_pdm, pdm)

    @mapping(m, eq_imt[j in Goods, rr in Regions], imt[j, rr] * pm[j, rr] ^ sigmam[j, rr] - aimt[j, rr] * tdd[j, rr] * pa[j, rr] ^ sigmam[j, rr])
    @complementarity(m, eq_imt, imt)

    @mapping(m, eq_dmd[j in Goods, rr in Regions], dmd[j, rr] * pdm[j, rr] ^ sigmam[j, rr] - admd[j, rr] * tdd[j, rr] * pa[j, rr] ^ sigmam[j, rr])
    @complementarity(m, eq_dmd, dmd)

    @mapping(m, eq_pa[j in Goods, rr in Regions], pa[j, rr] ^ (1 - sigmam[j, rr]) - aimt[j, rr] * pm[j, rr] ^ (1 - sigmam[j, rr]) - admd[j, rr]* pdm[j, rr] ^ (1-sigmam[j, rr]))
    @complementarity(m, eq_pa, pa)

    # CES level 2
    @mapping(m, eq_imrr[j in Goods, r in Regions, rr in Regions], imrr[j, r, rr] * (((1 + ter[j, r, rr]) * pe[j, r] + qtmg0[j, r, rr] * ptrst) * (1 + tmr[j, r, rr])) ^ sigmarr[j, rr] - aimrr[j, r, rr] * imt[j, rr] * pm[j, rr] ^ sigmarr[j, rr])
    @complementarity(m, eq_imrr, imrr)

    @mapping(m, eq_pm[j in Goods, rr in Regions], pm[j, rr] ^ (1-sigmarr[j, rr]) - sum(aimrr[j, r, rr] * (((1 + ter[j, r, rr]) * pe[j, r] + qtmg0[j, r, rr] * ptrst) * (1 + tmr[j, r, rr])) ^ (1-sigmarr[j, rr]) for r in Regions))
    @complementarity(m, eq_pm, pm)

    # international trade transport margins
    @mapping(m, eq_qtrs[rr in Regions], qtrs[rr] * pp[TransSec, rr] ^ sigmatrs - atrs[rr] * trst * ptrst ^ sigmatrs)
    @complementarity(m, eq_qtrs, qtrs)

    @mapping(m, eq_ptrst, ptrst ^ (1 - sigmatrs) - sum(atrs[rr] * pp[TransSec, rr] ^ (1 - sigmatrs) for rr in Regions))
    @complementarity(m, eq_ptrst, ptrst)

    @mapping(m, eq_trst, trst - sum(sum(sum(imrr[j, r, rr] * qtmg0[j, r, rr] for j in Goods) for r in Regions) for rr in Regions))
    @complementarity(m, eq_trst, trst)
end