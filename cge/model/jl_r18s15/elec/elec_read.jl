#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: read data of the energy and emissions
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# Read on the power sector
# --------------------------------------------------------------------------------------------------
# -- Intermediate inputs
Vqint_elecddir = joinpath(pwd(), "../input/elec/elecd.csv")
Vqint_elecddata = CSV.read(Vqint_elecddir, DataFrames.DataFrame, header=1, skipto=3)
Vqint_elecddata = Matrix(Vqint_elecddata)[1:end, 2:end]  ./ 1000 .+ 0.000001 # billion
Vqint_elecfdir = joinpath(pwd(), "../input/elec/elecf.csv")
Vqint_elecfdata = CSV.read(Vqint_elecfdir, DataFrames.DataFrame, header=1, skipto=3)
Vqint_elecfdata = Matrix(Vqint_elecfdata)[1:end, 2:end]  ./ 1000 .+ 0.000001 # billion
Vqint_elecdata = Vqint_elecddata .+ Vqint_elecfdata
Vqint_elec0 = zeros(Float64, NumGood, NumElec, NumRegion)
for j in Goods, i in ElecType, r in Regions
    colNum = (r - 1) * NumElec + i
    Vqint_elec0[j, i, r] = Vqint_elecdata[j, colNum] 
end
Vqint_elec0[FossilSec, :, 1]
# -- Value added of power sector
Vvaelec0 = zeros(Float64, NumFactor, NumElec, NumRegion) 
Vvaelecdir = joinpath(pwd(), "../input/elec/vaelec.csv")
Vvaelecdata = CSV.read(Vvaelecdir, DataFrames.DataFrame, header=[1,2], skipto=3)
Vvaelecdata = Matrix(Vvaelecdata)[1:end, 2:end] ./ 1000 .+ 0.000001 # billion
for v in Factors, i in ElecType, r in Regions
    colNum = (r - 1) * NumElec + i
    Vvaelec0[v, i, r] = Vvaelecdata[v, colNum] 
end
Vvaelec0

# -- production tax of power sector
prodtax_elecdir = joinpath(pwd(), "../input/elec/prodtax_elec.csv")
prodtax_elecdata = CSV.read(prodtax_elecdir, DataFrames.DataFrame, header=1, skipto=2)
prodtax_elec0 = Matrix(prodtax_elecdata)[1:end, 2:end] ./ 1000 .+ 0.000001# billion

# -- value added tax of power sector
vatax_elec0 = zeros(Float64, NumFactor, NumElec, NumRegion) 
vatax_elecdir = joinpath(pwd(), "../input/elec/vatax_elec.csv")
vatax_elecdata = CSV.read(vatax_elecdir, DataFrames.DataFrame, header=[1,2], skipto=3)
vatax_elecdata = Matrix(vatax_elecdata)[1:end, 2:end] ./ 1000 .+ 0.000001# billion
for v in Factors, i in ElecType, r in Regions
    colNum = (r - 1) * NumElec + i
    vatax_elec0[v, i, r] = vatax_elecdata[v, colNum] 
end

# -- power generation share of power sector
Vgendir = joinpath(pwd(), "../input/elec/gen.csv")
Vgendata = CSV.read(Vgendir, DataFrames.DataFrame, header=1, skipto=2)
Vgen0 = Matrix(Vgendata)[1:end, 2:end] .+ 0.000001# million toe

Vgen_psydir = joinpath(pwd(), "../input/elec/gen_elec_psy_2017.csv")
Vgen_psydata = CSV.read(Vgen_psydir, DataFrames.DataFrame, header=1, skipto=2)
Vgen_psy0 = Matrix(Vgen_psydata)[1:end, 2:end] ./ 1000 .+ 0.000001# 1000 TWh
Vgen_psy0

Vgen_psy16dir = joinpath(pwd(), "../input/elec/gen_elec_psy_2016.csv")
Vgen_psy16data = CSV.read(Vgen_psy16dir, DataFrames.DataFrame, header=1, skipto=2)
Vgen_psy16 = Matrix(Vgen_psy16data)[1:end, 2:end] ./ 1000 .+ 0.000001# TWh

Vgen_psy20dir = joinpath(pwd(), "../input/elec/gen_elec_psy_2020.csv")
Vgen_psy20data = CSV.read(Vgen_psy20dir, DataFrames.DataFrame, header=1, skipto=2)
Vgen_psy20 = Matrix(Vgen_psy20data)[1:end, 2:end] ./ 1000 .+ 0.000001# TWh

Vgen_diffdir = joinpath(pwd(), "../input/elec/gen_elec_diff_data.csv")
Vgen_diffdata = CSV.read(Vgen_diffdir, DataFrames.DataFrame, header=1, skipto=2)
timehis = collect(1978:1:2017)
timehiss = collect(1:1:length(timehis))
Vgen_diff0 = zeros(Float64, length(timehiss), NumRegion, NumElec)
for t in timehiss[13:end]
    for r in Regions
        for i in ElecType
            rownum = (t - 13) * NumRegion + r
            Vgen_diff0[t, r, i] = max(0, Vgen_diffdata[rownum, 2+i]) # TWh
        end
    end
end
Vgen_diff0[1:13, :, :] .= Vgen_diff0[[13], :, :] / 13

# tfp_solardir = joinpath(pwd(), "../input/elec/" * scn_name * "_solar" * ".csv")
# tfp_solardata = CSV.read(tfp_solardir, DataFrames.DataFrame, header=1, skipto=2)
# tfp_solardata_exg = tfp_solardata[1:14, 2:19]
# println("tfp_solardata:")
# println(tfp_solardata_exg)
# tfp_winddir = joinpath(pwd(), "../input/elec/" * scn_name * "_wind" * ".csv")
# tfp_winddata = CSV.read(tfp_winddir, DataFrames.DataFrame, header=1, skipto=2)
# tfp_winddata_exg = tfp_winddata[1:14, 2:19]
# println("tfp_winddata:")
# println(tfp_winddata_exg)
