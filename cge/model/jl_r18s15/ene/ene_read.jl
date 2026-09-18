#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: read data of the energy and emissions
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# Read on the energy
# --------------------------------------------------------------------------------------------------
# -- Intermediate inputs of energy e to sector i in region r
Veintddir = joinpath(pwd(), "../input/ene/eintd.csv")
Veintddata = CSV.read(Veintddir, DataFrames.DataFrame, header=1, skipto=2)
Veintddata = Matrix(Veintddata)[1:end, 3:2+NumRegion] # million toe
Veintfdir = joinpath(pwd(), "../input/ene/eintf.csv")
Veintfdata = CSV.read(Veintfdir, DataFrames.DataFrame, header=1, skipto=2)
Veintfdata = Matrix(Veintfdata)[1:end, 3:2+NumRegion] # million toe
Veintdata = Veintddata .+ Veintfdata

Veint0 = zeros(Float64, NumGood, NumSector, NumRegion)

for j in EnergyType, i in Sectors, r in Regions
    rowNum = (j - 1) * NumSector + i
    Veint0[EnergySec[j], i, r] = Veintdata[rowNum, r] 
end

# -- Household consumption of energy e in region r
Vehddir = joinpath(pwd(), "../input/ene/ehd.csv")
Vehddata = CSV.read(Vehddir, DataFrames.DataFrame, header=1, skipto=2)
Vehddata = Matrix(Vehddata)[1:end, 2:1+NumRegion] # million toe
Vehfdir = joinpath(pwd(), "../input/ene/ehf.csv")
Vehfdata = CSV.read(Vehfdir, DataFrames.DataFrame, header=1, skipto=2)
Vehfdata = Matrix(Vehfdata)[1:end, 2:1+NumRegion] # million toe
Vehdata = Vehddata .+ Vehfdata

Veh0 = zeros(Float64, NumGood, NumRegion)
for j in EnergyType
    Veh0[EnergySec[j], :] = Vehdata[j, :]
end

# -- international trade of energy e from r to rr
Veimrrdir = joinpath(pwd(), "../input/ene/eimrr.csv")
Veimrrdata = CSV.read(Veimrrdir, DataFrames.DataFrame, header=1, skipto=2)
Veimrrdata = Matrix(Veimrrdata)[1:end, 3:2+NumRegion] # million toe

Veimrr0 = zeros(Float64, NumGood, NumRegion, NumRegion)
for j in EnergyType, r in Regions, rr in Regions
    rowNum = (j - 1) * NumRegion + r
    Veimrr0[EnergySec[j], r, rr] = Veimrrdata[rowNum, rr]
end

# --------------------------------------------------------------------------------------------------
# Read on the energy-related CO2 emissions
# --------------------------------------------------------------------------------------------------
# -- CO2 emissions from intermediate inputs of energy e to sector i in region r
Vemis_intddir = joinpath(pwd(), "../input/ene/emis_intd.csv")
Vemis_intddata = CSV.read(Vemis_intddir, DataFrames.DataFrame, header=1, skipto=2)
Vemis_intddata = Matrix(Vemis_intddata)[1:end, 3:2+NumRegion] # million toe
Vemis_intfdir = joinpath(pwd(), "../input/ene/emis_intf.csv")
Vemis_intfdata = CSV.read(Vemis_intfdir, DataFrames.DataFrame, header=1, skipto=2)
Vemis_intfdata = Matrix(Vemis_intfdata)[1:end, 3:2+NumRegion] # million toe
Vemis_intdata = Vemis_intddata .+ Vemis_intfdata
Vemis_int0 = zeros(Float64, NumGood, NumSector, NumRegion)
for j in FossilType, i in Sectors, r in Regions
    rowNum = (j - 1) * NumSector + i
    Vemis_int0[FossilSec[j], i, r] = Vemis_intdata[rowNum, r] 
end

# -- Household consumption of energy e in region r
Vemis_hddir = joinpath(pwd(), "../input/ene/emis_hd.csv")
Vemis_hddata = CSV.read(Vemis_hddir, DataFrames.DataFrame, header=1, skipto=2)
Vemis_hddata = Matrix(Vemis_hddata)[1:end, 2:1+NumRegion] # million t
Vemis_hfdir = joinpath(pwd(), "../input/ene/emis_hf.csv")
Vemis_hfdata = CSV.read(Vemis_hfdir, DataFrames.DataFrame, header=1, skipto=2)
Vemis_hfdata = Matrix(Vemis_hfdata)[1:end, 2:1+NumRegion] # million t
Vemis_hdata = Vemis_hddata .+ Vemis_hfdata
Vemis_hdata = replace(Vemis_hdata, missing=>0)

Vemis_h0 = zeros(Float64, NumGood, NumRegion)
for j in FossilType
    Vemis_h0[FossilSec[j], :] = Vemis_hdata[j, :]
end
