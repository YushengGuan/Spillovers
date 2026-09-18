#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables
#---     May, 2023

@variables m begin
    # -- initialize the price
    # pfob[j = Goods, r = Regions, rr = Regions], (start=pfob0[j, r, rr])
    # pcif[j = Goods, r = Regions, rr = Regions], (start=pcif0[j, r, rr])
    pm[j = Goods, rr = Regions], (start=pm0[j, rr])
    pdm[j = Goods, rr = Regions], (start=pdm0[j, rr])
    pa[j = Goods, rr = Regions], (start=pa0[j, rr])
    pe[j = Goods, r = Regions], (start=pe0[j, r])

    # -- initialize the trade
    tdd[j = Goods, rr = Regions], (start=tdd0[j, rr])
    imrr[j = Goods, r = Regions, rr = Regions], (start=imrr0[j, r, rr])
    imt[j = Goods, rr = Regions], (start=imt0[j, rr])
    dmd[j = Goods, rr = Regions], (start=dmd0[j, rr])
    ext[j = Goods, r = Regions], (start=ext0[j, r])
    dms[j = Goods, r = Regions], (start=dmd0[j, r])
    qs[j = Goods, r = Regions], (start=qs0[j, r])

    # -- initialize the trade margin
    qtrs[r = Regions], (start=qtrs0[r])
    ptrst, (start = ptrst0)
    trst, (start=trst0)
end