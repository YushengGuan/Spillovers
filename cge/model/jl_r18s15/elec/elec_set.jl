#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: seting on the energy and emissions
#---     May, 2023


# --------------------------------------------------------------------------------------------------
# Define the sets of electricity subsectors as name/abbr
# --------------------------------------------------------------------------------------------------
EcType = [
    "TnD",
    "Coal_Power",
    "Oil_Power",
    "Gas_Power",
    "Nuclear",
    "Hydro",
    "Wind",
    "Solar",
    "Biomass"
]

TdType = [
    "TnD"
]

GnType = setdiff(EcType, TdType)

FsEcType = [
    "Coal_Power",
    "Oil_Power",
    "Gas_Power",
]

BeEcType = [
    "Biomass"
]


ReEcType = [
    "Wind",
    "Solar"
]

CCSEcType = [FsEcType; BeEcType]

ElecType = collect(1:1:length(EcType))
TnDType = collect(1:1:length(TdType))[1]
GenType = setdiff(ElecType, TnDType)
SolarPV = findall(x -> x in ["Solar"], EcType)[1]
Wind = findall(x -> x in ["Wind"], EcType)[1]
Hydro = findall(x -> x in ["Hydro"], EcType)[1]
ElecType_Non_WS = setdiff(ElecType, [SolarPV, Wind])

# CCS related type
FsElecType = findall(x -> x in FsEcType, EcType)
BeElecType = findall(x -> x in BeEcType, EcType)
CCSElecType = findall(x -> x in CCSEcType, EcType)
OthElecType = setdiff(ElecType, CCSElecType)
ReElecType = findall(x -> x in ReEcType, EcType)
OReElecType = setdiff(ElecType, ReElecType)
OElecType = setdiff(OReElecType, FsElecType)
OReGenType = setdiff(GenType, ReElecType)
OHElecType = setdiff(OElecType, [Hydro])

NumElec = length(ElecType)