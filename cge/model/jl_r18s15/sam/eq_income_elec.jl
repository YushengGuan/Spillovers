#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_income()
    # income
    @mapping(m, eq_tlinc[r in Regions], sum((1 - trlinc[i, r]) * l[i, r] * pl[r] for i in Sectors) - tlinc[r])
    @complementarity(m, eq_tlinc, tlinc)

    @mapping(m, eq_tkinc[r in Regions], sum((1 - trkinc[i, r]) * k[i, r] * pk[r] for i in Sectors) - tkinc[r])
    @complementarity(m, eq_tkinc, tkinc)

    @mapping(m, eq_tlndinc[r in Regions], sum((1 - trlndinc[i, r]) * lnd[i, r] * plnd[r] for i in AgriSec) - tlndinc[r])
    @complementarity(m, eq_tlndinc, tlndinc)

    @mapping(m, eq_tnsinc[r in Regions], sum((1 - trnsinc[i, r]) * ns[i, r] * pns[i, r] for i in NatSec) - tnsinc[r])
    @complementarity(m, eq_tnsinc, tnsinc)

    @mapping(m, eq_inch[r in Regions], akh[r] * tkinc[r] + tlndinc[r] + tnsinc[r] + tlinc[r] - inch[r])
    @complementarity(m, eq_inch, inch)

    @mapping(m, eq_incg[r in Regions], 
            sum(trpd[i, r] * pprod[i, r] * prod[i, r] for i in Sectors_Non_Elec) +
            sum(trpd_elec[i, r] * pgen_elec[i, r] * gen_elec[i, r] for i in ElecType) + 
            sum(trk[i, r] * k[i, r] * pk[r] for i in Sectors_Non_Elec) + 
            sum(trk_elec[i, r] * k_elec[i, r] * pk[r] for i in ElecType) + 
            sum(trkinc[i, r] * k[i, r] * pk[r] for i in Sectors) +
            sum(trl[i, r] * l[i, r] * pl[r] for i in Sectors_Non_Elec) + 
            sum(trl_elec[i, r] * l_elec[i, r] * pl[r] for i in ElecType) + 
            sum(trlinc[i, r] * l[i, r] * pl[r] for i in Sectors) +
            sum((trlnd[i, r] + trlndinc[i, r]) * lnd[i, r] * plnd[r] for i in AgriSec) + 
            sum((trns[i, r] + trnsinc[i, r]) * ns[i, r] * pns[i, r] for i in NatSec) + 
            sum(sum(strint[j, i, r] * qint[j, i, r] * pa[j, r] for j in Goods) for i in Sectors_Non_Elec) + 
            sum(sum(strint_elec[j, i, r] * qint_elec[j, i, r] * pa[j, r] for j in Goods) for i in ElecType) + 
            sum(strh[j, r] * consh[j, r] * pa[j, r] for j in Goods) +
            sum(strg[j, r] * consg[j, r] * pa[j, r] for j in Goods) +
            sum(strinv[j, r] * inv[j, r] * pa[j, r] for j in Goods) +
            sum(sum(ter[j, r, rr] * pe[j, r] * imrr[j, r, rr] for rr in Regions) for j in Goods) +
            sum(sum(tmr[j, rr, r] * ((1 + ter[j, rr, r]) * pe[j, rr] + qtmg0[j, rr, r] * ptrst) * imrr[j, rr, r] for rr in Regions) for j in Goods)
            + emisrev[r]
            - incg[r])
    @complementarity(m, eq_incg, incg)
end