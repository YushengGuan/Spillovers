#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: read SAM data of the basic GRID model
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# Structure of SAM
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Intermediate inputs and final demand by domestic agents
# --------------------------------------------------------------------------------------------------

# -- Intermediate inputs of imported goods j to sector i in region r
Vqintf0 = zeros(Float64, NumGood, NumSector, NumRegion) 
Vqintfdir = joinpath(pwd(), "../input/sam/qintf.csv")
Vqintfdata = CSV.read(Vqintfdir, DataFrames.DataFrame, header=[1,2], skipto=3)
Vqintfdata = Matrix(Vqintfdata)[1:end, 2:end] ./ 1000 # billion
for j in Goods, i in Sectors, r in Regions
    colNum = (r - 1) * NumSector + i
    Vqintf0[j, i, r] = Vqintfdata[j, colNum] 
end

# -- Intermediate inputs of domestically produced goods j to sector i in region r
Vqintd0 = zeros(Float64, NumGood, NumSector, NumRegion) 
Vqintddir = joinpath(pwd(), "../input/sam/qintd.csv")
Vqintddata = CSV.read(Vqintddir, DataFrames.DataFrame, header=[1,2], skipto=3)
Vqintddata = Matrix(Vqintddata)[1:end, 2:end] ./ 1000 # billion
for j in Goods, i in Sectors, r in Regions
    colNum = (r - 1) * NumSector + i
    Vqintd0[j, i, r] = Vqintddata[j, colNum] 
end

# -- Intermediate inputs of goods j to sector i in region r
Vqint0 = Vqintd0 .+ Vqintf0

# -- Final demand of imported goods j to agents a in region r
Vqfdfdir = joinpath(pwd(), "../input/sam/qfdf.csv")  # Q final demand foreign
Vqfdfdata = CSV.read(Vqfdfdir, DataFrames.DataFrame, header=[1,2], skipto=3)
Vqfdfdata = Matrix(Vqfdfdata)[1:end, 2:end] ./ 1000 # billion

Vconshf0 = zeros(Float64, NumGood, NumRegion) # demand of imported goods from private household
Vconsgf0 = zeros(Float64, NumGood, NumRegion) # demand of imported goods from government
Vinvf0 = zeros(Float64, NumGood, NumRegion) # invest of imported goods

for j in Goods, rr in Regions
    Vconshf0[j, rr] = Vqfdfdata[j, (rr - 1) * 3 + 1]
    Vconsgf0[j, rr] = Vqfdfdata[j, (rr - 1) * 3 + 2]
    Vinvf0[j, rr] = Vqfdfdata[j, (rr - 1) * 3 + 3]
end

# -- Final demand of domestically produced goods j to agents a in region r
Vqfdddir = joinpath(pwd(), "../input/sam/qfdd.csv")
Vqfdddata = CSV.read(Vqfdddir, DataFrames.DataFrame, header=[1,2], skipto=3)
Vqfdddata = Matrix(Vqfdddata)[1:end, 2:end] ./ 1000 # billion

Vconshd0 = zeros(Float64, NumGood, NumRegion) # demand of domestically produced goods from private household
Vconsgd0 = zeros(Float64, NumGood, NumRegion) # demand of domestically produced goods from government
Vinvd0 = zeros(Float64, NumGood, NumRegion) # investment of domestically produced goods

for j in Goods, rr in Regions
    Vconshd0[j, rr] = Vqfdddata[j, (rr - 1) * 3 + 1]
    Vconsgd0[j, rr] = Vqfdddata[j, (rr - 1) * 3 + 2]
    Vinvd0[j, rr] = Vqfdddata[j, (rr - 1) * 3 + 3]
end

# -- Final demand of goods j to agents a in region r
Vconsh0 = Vconshd0 .+ Vconshf0 # household
Vconsg0 = Vconsgd0 .+ Vconsgf0 # government
Vinv0 = Vinvd0 .+ Vinvf0 # investment

# --------------------------------------------------------------------------------------------------
# Incomes of production factors and production/saled taxes
# --------------------------------------------------------------------------------------------------

# -- Income of Production Factors
Vvam0 = zeros(Float64, NumFactor, NumSector, NumRegion) 
Vvamdir = joinpath(pwd(), "../input/sam/vam.csv")
Vvamdata = CSV.read(Vvamdir, DataFrames.DataFrame, header=[1,2], skipto=3)
Vvamdata = Matrix(Vvamdata)[1:length(Factors), 2:(1+ NumSector * NumRegion)] ./ 1000 # billion
for v in Factors, i in Sectors, r in Regions
    colNum = (r - 1) * NumSector + i
    Vvam0[v, i, r] = Vvamdata[v, colNum] 
end

Vvam0[4, FrsSec, :] .= Vvam0[5, FrsSec, :]
Vvam0[5, FrsSec, :] .= 0

Vvam0[4, MeatSec, :] .= Vvam0[5, MeatSec, :] .+ Vvam0[4, MeatSec, :]
Vvam0[5, MeatSec, :] .= 0

# -- Production tax on sector i in region r
prodtax0 = zeros(Float64, NumSector, NumRegion) 
prodtaxdir = joinpath(pwd(), "../input/sam/prodtax.csv")
prodtaxdata = CSV.read(prodtaxdir, DataFrames.DataFrame, header=1, skipto=2)
prodtax0 = Matrix(prodtaxdata)[1:end, 2:1+NumRegion] ./ 1000 # billion

# -- Factor tax on sector i in region r
vatax0 = zeros(Float64, NumFactor, NumSector, NumRegion) 
vataxdir = joinpath(pwd(), "../input/sam/vatax.csv")
vataxdata = CSV.read(vataxdir, DataFrames.DataFrame, header=[1,2], skipto=3)
vataxdata = Matrix(vataxdata)[1:end, 2:1+NumSector * NumRegion] ./ 1000 # billion
for v in Factors, i in Sectors, r in Regions
    colNum = (r - 1) * NumSector + i
    vatax0[v, i, r] = vataxdata[v, colNum] 
end

vatax0[4, FrsSec, :] .= vatax0[5, FrsSec, :]
vatax0[5, FrsSec, :] .= 0
vatax0[4, MeatSec, :] .= vatax0[5, MeatSec, :] .+ vatax0[4, MeatSec, :]
vatax0[5, MeatSec, :] .= 0

# -- Income tax of different factors on sector i in region r
inctax0 = zeros(Float64, NumFactor, NumSector, NumRegion) 
inctaxdir = joinpath(pwd(), "../input/sam/inctax.csv")
inctaxdata = CSV.read(inctaxdir, DataFrames.DataFrame, header=[1,2], skipto=3)
inctaxdata = Matrix(inctaxdata)[1:end, 2:1+NumSector * NumRegion] ./ 1000 # billion
for v in Factors, i in Sectors, r in Regions
    colNum = (r - 1) * NumSector + i
    inctax0[v, i, r] = inctaxdata[v, colNum] 
end

inctax0[4, FrsSec, :] .= inctax0[5, FrsSec, :]
inctax0[5, FrsSec, :] .= 0
inctax0[4, MeatSec, :] .= inctax0[5, MeatSec, :] .+ inctax0[4, MeatSec, :]
inctax0[5, MeatSec, :] .= 0

# -- Sales taxes on imported goods or services j to different sectors i in region r
sftax_int0 = zeros(Float64, NumGood, NumSector, NumRegion) 
sftax_intdir = joinpath(pwd(), "../input/sam/sftax_int.csv")
sftax_intdata = CSV.read(sftax_intdir, DataFrames.DataFrame, header=[1,2], skipto=3)
sftax_intdata = Matrix(sftax_intdata)[1:end, 2:1+NumSector * NumRegion] ./ 1000 # billion
for j in Goods, i in Sectors, r in Regions
    colNum = (r - 1) * NumSector + i
    sftax_int0[j, i, r] = sftax_intdata[j, colNum] 
end

# -- Sales taxes on domestically produced goods or services j to different sectors i in region r
sdtax_int0 = zeros(Float64, NumGood, NumSector, NumRegion) 
sdtax_intdir = joinpath(pwd(), "../input/sam/sdtax_int.csv")
sdtax_intdata = CSV.read(sdtax_intdir, DataFrames.DataFrame, header=[1,2], skipto=3)
sdtax_intdata = Matrix(sdtax_intdata)[1:end, 2:1+NumSector * NumRegion] ./ 1000 # billion
for j in Goods, i in Sectors, r in Regions
    colNum = (r - 1) * NumSector + i
    sdtax_int0[j, i, r] = sdtax_intdata[j, colNum] 
end

# -- Sales taxes on imported goods or services j to different institutions a in region r
sftax_fd0 = zeros(Float64, NumGood, NumInstitution, NumRegion) 
sftax_fddir = joinpath(pwd(), "../input/sam/sftax_fd.csv")
sftax_fddata = CSV.read(sftax_fddir, DataFrames.DataFrame, header=[1,2], skipto=3)
sftax_fddata = Matrix(sftax_fddata)[1:end, 2:1+length(Institutions) * NumRegion] ./ 1000 # billion
for j in Goods, a in Institutions, r in Regions
    colNum = (r - 1) * NumInstitution + a
    sftax_fd0[j, a, r] = sftax_fddata[j, colNum] 
end

# -- Sales taxes on domestically produced goods or services j to different institutions a in region r
sdtax_fd0 = zeros(Float64, NumGood, NumInstitution, NumRegion) 
sdtax_fddir = joinpath(pwd(), "../input/sam/sdtax_fd.csv")
sdtax_fddata = CSV.read(sdtax_fddir, DataFrames.DataFrame, header=[1,2], skipto=3)
sdtax_fddata = Matrix(sdtax_fddata)[1:end, 2:1+length(Institutions) * NumRegion] ./ 1000 # billion
for j in Goods, a in Institutions, r in Regions
    colNum = (r - 1) * NumInstitution + a
    sdtax_fd0[j, a, r] = sdtax_fddata[j, colNum] 
end

# total saled tax on intermediate goods or final demand
stax_int0 = sdtax_int0 .+ sftax_int0
stax_fd0 = sdtax_fd0 .+ sftax_fd0

# --------------------------------------------------------------------------------------------------
# International Trade Block: volumn, tariff and margin
# --------------------------------------------------------------------------------------------------

# -- Export of commodities from region r to region rr of goods i
Vimrr0 = zeros(Float64, NumGood, NumRegion, NumRegion) 
Vimrrdir = joinpath(pwd(), "../input/sam/imrr.csv")
Vimrrdata = CSV.read(Vimrrdir, DataFrames.DataFrame, header=1, skipto=2)
Vimrrdata = Matrix(Vimrrdata)[1:end, 3:2+NumRegion] ./ 1000 # billion
for i in Goods, r in Regions, rr in Regions
    rowNum = (r - 1) * NumSector + i
    Vimrr0[i, r, rr] = Vimrrdata[rowNum, rr] 
end

# -- Export taxes of goods or services j in region r when exported to rr
te0 = zeros(Float64, NumGood, NumRegion, NumRegion) 
tedir = joinpath(pwd(), "../input/sam/te.csv")
tedata = CSV.read(tedir, DataFrames.DataFrame, header=1, skipto=2)
tedata = Matrix(tedata)[1:end, 3:2+NumRegion] ./ 1000 # billion
for i in Goods, r in Regions, rr in Regions
    rowNum = (r - 1) * NumSector + i
    te0[i, rr, r] = tedata[rowNum, rr] 
end

# -- Import taxes of goods or services j in region rr when imported from r
tm0 = zeros(Float64, NumGood, NumRegion, NumRegion) 
tmdir = joinpath(pwd(), "../input/sam/tm.csv")
tmdata = CSV.read(tmdir, DataFrames.DataFrame, header=1, skipto=2)
tmdata = Matrix(tmdata)[1:end, 3:2+NumRegion] ./ 1000 # billion
for i in Goods, r in Regions, rr in Regions
    rowNum = (r - 1) * NumSector + i
    tm0[i, r, rr] = tmdata[rowNum, rr] 
end

# -- Margin commodities of goods or services j in region rr when imported from r
margin0 = zeros(Float64, NumGood, NumRegion, NumRegion) 
margindir = joinpath(pwd(), "../input/sam/margin.csv")
margindata = CSV.read(margindir, DataFrames.DataFrame, header=1, skipto=2)
margindata = Matrix(margindata)[1:end, 3:2+NumRegion] ./ 1000 # billion
for i in Goods, r in Regions, rr in Regions
    rowNum = (r - 1) * NumSector + i
    margin0[i, r, rr] = margindata[rowNum, rr] 
end

# transport supply of international trade
Vqtrs0 = zeros(Float64, NumRegion)
Vqtrsdir = joinpath(pwd(), "../input/sam/qtrs.csv")
Vqtrsdata = CSV.read(Vqtrsdir, DataFrames.DataFrame, header=1, skipto=2)
Vqtrs0 = Matrix(Vqtrsdata)[1, 3:2+NumRegion] ./ 1000 # billion

# Vsave of foreigners
Vsave0 = zeros(Float64, NumRegion, NumRegion) 
Vsavedir = joinpath(pwd(), "../input/sam/save.csv")
Vsavedata = CSV.read(Vsavedir, DataFrames.DataFrame, header=1, skipto=2)
Vsave0 = Matrix(Vsavedata)[1:end, 2:1+NumRegion] ./ 1000 # billion

# Capital flow
Vcapital = zeros(Float64, 2, NumRegion) 
Vcapitaldir = joinpath(pwd(), "../input/sam/capital.csv")
Vcapitaldata = CSV.read(Vcapitaldir, DataFrames.DataFrame, header=1, skipto=2)
Vcapital0 = Matrix(Vcapitaldata)[1:end, 3:2+NumRegion] ./ 1000 # billion

# --------------------------------------------------------------------------------------------------
# Consistency Check
# --------------------------------------------------------------------------------------------------
# -- check consistency between Vimt0 and Vimrr0
Vimt0 = sum(Vqintf0, dims=2)[:, 1, :] + Vconshf0 + Vconsgf0 + Vinvf0 # demand of imported commodities
Vdmd0 = sum(Vqintd0, dims=2)[:, 1, :] + Vconshd0 + Vconsgd0 + Vinvd0 # demand of domestically produced commodities
Vimrr0 # Vimrr0[i, rext, rimt], import of goods i in region rr from region r, see sam_read.jl
Δimt0 = Vimt0 - sum(Vimrr0 .+ tm0 .+ margin0, dims=2)[:, 1, :]