#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: seting on the basic SAM structure of GRID Model
#---     May, 2023


# --------------------------------------------------------------------------------------------------
# Define the sets of core SAM as name/abbr
# --------------------------------------------------------------------------------------------------
Region = [
    "Australia_Oceania",  
    "China",
    "Japan",
    "South Korea",
    "Rest of World",
    "Southeast Asia",
    "Central, Western and South Asia",
    "India",
    "Canada",
    "United States",
    "Rest of America",
    "Brazil",
    "EU, UK and EFTA",
    "Eastern Europe",
    "Russia",
    "North Africa",
    "Sub Saharan",
    "South Africa"
]

Sector = [
    "Rice",
    "Crops nec",
    "Bovine cattle, sheep and goats, horses",
    "Animal products nec",
    "Forestry",
    "Coal",
    "Oil",
    "Gas",
    "Mine",
    "Manufac",
    "Petro",
    "Power",
    "WatWaste",
    "OthServ",
    "Transport",
]

Good = Sector

EneSec = [ # energy sector
    "Coal",
    "Oil",
    "Gas",
    "Petro",
    "Power"
    ]

PowSec = [
    "Power"
]

FslSec = [
    "Coal",
    "Oil",
    "Gas",
    "Petro",
    ]

AgrSec = [
    "Rice",
    "Crops nec",
    "Bovine cattle, sheep and goats, horses",
    "Animal products nec",
    "Forestry",
]

CrpSec = [
    "Rice",
    "Crops nec"
]

MtSec = [
    "Bovine cattle, sheep and goats, horses",
    "Animal products nec",
]

NtSec = [
    # "Forestry",
    # "Fishing",
    "Coal",
    "Oil",
    "Gas",
    "Mine",
]

TrsSec = [
    "Transport"
]

Institution = [
    "Private Households",
    "Government",
    "Investment"
]

Factor = [
    "UnSkLab",
    "SkLab",
    "Capital",
    "Land",
    "NatRes"
]

NumRegion = length(Region)
NumSector = length(Sector)
NumGood = length(Good)

NumInstitution = length(Institution)
NumFactor = length(Factor)
NumFossil = length(FslSec)

# --------------------------------------------------------------------------------------------------
# Define the sets of core SAM as serial number
# --------------------------------------------------------------------------------------------------
Regions = collect(1:1:NumRegion)
RegionTest = Regions
Sectors = collect(1:1:NumSector)
Goods = collect(1:1:NumGood)
Institutions = collect(1:1:NumInstitution)
Factors = collect(1:1:NumFactor)
EnergySec = findall(x -> x in EneSec, Sector)
PowerSec = findall(x -> x in PowSec, Sector)[1]
FossilSec = findall(x -> x in FslSec, Sector)
TransSec = findall(x -> x in TrsSec, Sector)[1]
NonTransSec = setdiff(Sectors, TransSec)
IntSec = setdiff(Sectors, EnergySec)
AgriSec = findall(x -> x in AgrSec, Sector)
CropsSec = findall(x -> x in CrpSec, Sector)
MeatSec = findall(x -> x in MtSec, Sector)
NatSec = findall(x -> x in NtSec, Sector)
FrsSec = findall(x -> x == "Forestry", Sector)[1]
OtherSec = setdiff(Sectors, [AgriSec; NatSec])
OtherSec_Non_Elec = setdiff(Sectors, [AgriSec; NatSec; PowerSec])
Sectors_Non_Elec = setdiff(Sectors, PowerSec)
Sectors_Non_Ene = setdiff(Sectors, EnergySec)