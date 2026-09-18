#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_demand()
    # consumption and saving of households
    # @mapping(m, eq_consh[j in Goods, r in Regions], consh[j, r] * (pa[j, r] * (1 + strh[j, r]) + etax_h[j, r]) - thetah[j, r] * (inch[r] - savh[r]))
    # @complementarity(m, eq_consh, consh)

    @mapping(m, eq_consh[j in Sectors, r in Regions], (pa[j, r] * (1 + strh[j, r]) + etax_h[j, r]) * minh[j, r] + muh[j, r] * ((inch[r] - savh[r]) - sum((pa[j, r] * (1 + strh[j, r]) + etax_h[j, r]) * minh[j, r] for j in Goods)) - consh[j, r] * (pa[j, r] * (1 + strh[j, r]) + etax_h[j, r]))
    @complementarity(m, eq_consh, consh)

    # @mapping(m, eq_consh[i in Sectors, r in Regions], parm[i, r] * minh[i, r] / (1 - flw_red[i, r]) + muh[i, r] * (dinch[r] * (1 - asavh[r]) - sum(parm[i, r] * minh[i, r]  / (1 - flw_red[i, r]) for i in Sectors)) - consh[i, r] * parm[i, r] / (1 - flw_red[i, r]))
    # @complementarity(m, eq_consh, consh)

    # consumption and saving of government
    @mapping(m, eq_consg[j in Goods, r in Regions], consg[j, r] * pa[j, r] * (1 + strg[j, r]) - thetag[j, r] * (incg[r] - savg[r]))
    @complementarity(m, eq_consg, consg)

    # investment
    @mapping(m, eq_inv[j in Goods, r in Regions], inv[j, r] * (pa[j, r] * (1 + strinv[j, r])) ^ sigmav[r] - ainv[j, r] * tinv[r] * ptinv_idx[r] ^ sigmav[r])
    @complementarity(m, eq_inv, inv)

    @mapping(m, eq_ptinv[r in Regions], sum(ainv[j, r] * (pa[j, r] * (1 + strinv[j, r])) ^ (1 - sigmav[r]) for j in Goods) - ptinv_idx[r] ^ (1 - sigmav[r]))
    @complementarity(m, eq_ptinv, tinv)
end