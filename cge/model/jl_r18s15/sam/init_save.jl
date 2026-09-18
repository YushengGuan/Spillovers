#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables of income block
#---     May, 2023

@variables m begin
    # -- initialize the saving
    savh[rr = Regions], (start=savh0[rr])
    savg[rr = Regions], (start=savg0[rr])
    save[rr = Regions], (start=save0[rr])
    savtrs[rr = Regions], (start=savtrs0[rr])
    savk[rr = Regions], (start=savk0[rr])
end