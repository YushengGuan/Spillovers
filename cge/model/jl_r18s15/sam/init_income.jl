#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables of income block
#---     May, 2023

@variables m begin
    # -- initialize the income
    tlinc[rr = Regions], (start=tlinc0[rr])
    tkinc[rr = Regions], (start=tkinc0[rr])
    tlndinc[rr = Regions], (start=tlndinc0[rr])
    tnsinc[rr = Regions], (start=tnsinc0[rr])
    inch[rr = Regions], (start=inch0[rr])
    incg[rr = Regions], (start=incg0[rr])
    # emisrev[rr = Regions], (start=emisrev0[rr])
end