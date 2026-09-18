#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: calibration of the core model
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# Elasticities
# --------------------------------------------------------------------------------------------------

sigmarr = zeros(Float64, NumGood, NumRegion) .+ 2 # elasticity of imported goods from different regions
sigmam = zeros(Float64, NumGood, NumRegion) .+ 2 # elasticity between domestically produced and imported goods
sigmae = zeros(Float64, NumGood, NumRegion) .- 3 # elasticity between domestically produced and exported goods, usualy -3
sigmav = zeros(Float64, NumRegion) .+ 2 # elasticity between investment goods
sigmaene = zeros(Float64, NumSector, NumRegion) .+ 2 # elasticity between electricity and fossil fuel
sigmafe = zeros(Float64, NumSector, NumRegion) .+ 2 # elasticity among fossil fuels
sigmavae = zeros(Float64, NumSector, NumRegion) .+ 0.3 # elasticity among KEL and land/natural resources
sigmakel = zeros(Float64, NumSector, NumRegion) .+ 0.8 # elasticity among factors and energy
sigmakl = zeros(Float64, NumSector, NumRegion) .+ 0.6 # elasticity among capital and labor
sigmava = zeros(Float64, NumSector, NumRegion) .+ 0.6 # elasticity among capital and labor
sigmap = zeros(Float64, NumSector, NumRegion) # top-nested elasticity
sigmatrs = 4 # elasticity of international trade transport supplier among differetn countries
sigmalu = zeros(Float64, NumSector, NumRegion) .+ 2
# sigmaaez = zeros(Float64, NumAEZ, NumRegion) .- 2

sigmaene_elec = zeros(Float64, NumElec, NumRegion) .+ 0.2 # elasticity between electricity and fossil fuel
sigmavae_elec = zeros(Float64, NumElec, NumRegion) .+ 0.3 # elasticity among KEL and land/natural resources
sigmakel_elec = zeros(Float64, NumElec, NumRegion) .+ 0.5 # elasticity among factors and energy
sigmakl_elec = zeros(Float64, NumElec, NumRegion) .+ 0.6 # elasticity among capital and labor
sigmava_elec = zeros(Float64, NumElec, NumRegion) .+ 0.6 # elasticity among capital and labor
sigmap_elec = zeros(Float64, NumElec, NumRegion) # top-nested elasticity
sigmaelec = zeros(Float64, NumRegion) .+ 2 # elasticity among different electricity technologies, usually 4
# household income elasticity
etahdir = joinpath(pwd(), "../input/elas/etah_s" * string(sNum) * ".csv")
etahdata = CSV.read(etahdir, DataFrames.DataFrame, header=1, skipto=2)
etah = Matrix(etahdata)[1:NumSector, 2]

# household price elasticity of food
gammahdir = joinpath(pwd(), "../input/elas/gammahr" * string(rNum) * "s" * string(sNum) * ".csv")
gammahdata = CSV.read(gammahdir, DataFrames.DataFrame, header=1, skipto=2)
gammah = Matrix(gammahdata)[1:NumSector, 2:1+NumRegion]

# frish parameter
frishdir = joinpath(pwd(), "../input/elas/frish_par.csv")
frishdata = CSV.read(frishdir, DataFrames.DataFrame, header=1, skipto=2)
frish = Matrix(frishdata)[1:NumRegion, 4]