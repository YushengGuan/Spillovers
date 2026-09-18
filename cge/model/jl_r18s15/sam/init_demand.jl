#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables of final demand
#---     May, 2023

@variables m begin
    # -- initialize the demand
    consh[j = Goods, rr = Regions], (start=consh0[j, rr])
    consg[j = Goods, rr = Regions], (start=consg0[j, rr])
    inv[j = Goods, rr = Regions], (start=inv0[j, rr])
    tinv[rr = Regions], (start=tinv0[rr])
    walras[rr = Regions], (start=0)
end