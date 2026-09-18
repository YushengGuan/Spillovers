#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: calibration of the energy and emissions
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# calibration on the energy
# --------------------------------------------------------------------------------------------------
eint0 = Veint0
eh0 = Veh0

enefac_int = eint0 ./ qint0
enefac_h = eh0 ./ consh0

eimrr0 = Veimrr0
enefac_imrr = eimrr0 ./ imrr0

# # --------------------------------------------------------------------------------------------------
# # calibration on the energy-related emissions factor
# # --------------------------------------------------------------------------------------------------
emis_int0 = Vemis_int0
emis_h0 = Vemis_h0

emisfac_int = emis_int0 ./ qint0
emisfac_h = emis_h0 ./ consh0
temit0 = sum(emis_int0, dims=(1, 2))[1, 1, :] .+ sum(emis_h0, dims=1)[1, :]
gemit0 = sum(temit0, dims=1)[1]