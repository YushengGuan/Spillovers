#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_save()
    # saving of foreigners
    @mapping(m, eq_save[r in Regions], save[r] + sum(sum((1 + ter[j, r, rr]) * pe[j, r] * imrr[j, r, rr] - (1 + ter[j, rr, r]) * pe[j, rr] * imrr[j, rr, r] for rr in Regions) for j in Sectors))
    @complementarity(m, eq_save, save)

    @mapping(m, eq_savk[r in Regions], savk[r] - aksav[r] * sav_dn[r] * tkinc[r])
    @complementarity(m, eq_savk, savk)

    @mapping(m, eq_savh[r in Regions], savh[r] - asavh[r] * sav_dn[r] * inch[r])
    @complementarity(m, eq_savh, savh)

    @mapping(m, eq_savg[r in Regions], savg[r] - asavg[r] * sav_dn[r] * incg[r])
    @complementarity(m, eq_savg, savg)
    
    @mapping(m, eq_savtrs[r in Regions], savtrs[r] + pp[TransSec, r] * qtrs[r] - sum(sum(imrr[j, rr, r] * qtmg0[j, rr, r] * ptrst for j in Goods) for rr in Regions))
    @complementarity(m, eq_savtrs, savtrs)

    # balance of saving and investment
    @mapping(m, eq_is[r in Regions], savh[r] + savg[r] + savk[r] + er0[r] * save[r] + savtrs[r] + walras[r] - tinv[r] * ptinv_idx[r])
    @complementarity(m, eq_is, walras)
end