#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables
#---     May, 2023

@variables m begin
    # -- initialize the technological effciency
    lambdak[i = Sectors, rr = Regions], (start=1)
    lambdal[i = Sectors, rr = Regions], (start=1)
    # lambdalnd[i = AgriSec, rr = Regions], (start=1)
    # lambdans[i = NatSec, rr = Regions], (start=1)
    tfp[rr = Regions], (start=1)
    ngdp[rr = Regions], (start = gdp0[rr])
    rgdp[rr = Regions], (start = gdp0[rr])
    pgdp[rr = Regions], (start = 1)
    # -- initialize the price of factors
    pk[rr = Regions], (start=pk0[rr])
    pl[rr = Regions], (start=pl0[rr])
    plnd[rr = Regions], (start=plnd0[rr]) # using uniform price for test
    pns[i = NatSec, rr = Regions], (start=pns0[i, rr])
end