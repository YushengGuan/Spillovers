#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: seting on the energy and emissions
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# Define the sets of energy and emissions as name/abbr
# --------------------------------------------------------------------------------------------------
EneType = [
    "Coal",
    "Oil",
    "Gas",
    "Oil_pct",
    "Electricity"
]

FslType = [
    "Coal",
    "Oil",
    "Gas",
    "Oil_pct"
]


EnergyType = collect(1:1:length(EneType))
FossilType = collect(1:1:length(FslType))

