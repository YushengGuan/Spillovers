#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables
#---     May, 2023

@variables m begin
    # -- initialize the energy
    eint[j = EnergySec, i = Sectors_Non_Elec, rr = Regions], (start=eint0[j, i, rr])
    eint_elec[j = EnergySec, i = ElecType, rr = Regions], (start=eint_elec0[j, i, rr])
    eh[j = EnergySec, rr = Regions], (start=eh0[j, rr])
    emis_int[j in FossilSec, i in Sectors_Non_Elec, rr in Regions], (start=emis_int0[j, i, rr])
    emis_elec[j in FossilSec, i in ElecType, rr in Regions], (start=emis_elec0[j, i, rr])
    emis_h[j in FossilSec, rr in Regions], (start=emis_h0[j, rr])
    temit[rr in Regions], (start=temit0[rr])
    gemit, (start=gemit0)
end