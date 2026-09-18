#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: calibration of the policy variables
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# calibration on the carbon pricing variables
# --------------------------------------------------------------------------------------------------
pco2dir = joinpath(pwd(), "../input/policy/pco2_r" * string(rNum) * ".csv")
pco2data = CSV.read(pco2dir, DataFrames.DataFrame, header=1, skipto=2)
pco2_years = Int.(pco2data[:, 1])
pco2_rows = [begin
    year_pos = findfirst(==(yr), pco2_years)
    if isnothing(year_pos)
        year_pos = findlast(<=(yr), pco2_years)
    end
    if isnothing(year_pos)
        year_pos = 1
    end
    year_pos
end for yr in Years]

if rand_flag == 0
    pco2_exg_dyn = Matrix(pco2data[pco2_rows, 2:1+NumRegion])' ./ 1000
elseif rand_flag == 1
    pco2_exg_dyn = Matrix(pco2data[pco2_rows, 2:1+NumRegion])' .* rand(truncated(Normal(1, 0.7); lower=0.1, upper=1.5))
end
if maximum(Years) > maximum(pco2_years)
    println("pco2 input ends at ", maximum(pco2_years), "; using the latest available carbon price for later years.")
end
# pco2_exg_dyn = zeros(Float64, NumRegion, NumYears)
pco20 = pco2_exg_dyn[:, 1]
if get(ENV, "GRID_VERBOSE_INPUTS", "1") == "1"
    println("pco2_exg_dyn")
    println(pco2_exg_dyn)
end

# cap_red_ratedir = joinpath(pwd(), "../input/policy/emis_agg.csv")
# cap_red_ratedata = CSV.read(cap_red_ratedir, DataFrames.DataFrame, header=1, skipto=2)
# cap_red_rate = Matrix(cap_red_ratedata)[1:NumRegion, 2:1+NumYears]
# --------------------------------------------------------------------------------------------------
# calibration on the technology variables
# --------------------------------------------------------------------------------------------------
emkup_elec_old_dyn = ones(Float64, NumElec, NumYears)
emkup_elec_new_dyn = ones(Float64, NumElec, NumYears)
emkup_elec_old_dyn[SolarPV, :] .= 0.235731 / 0.186277
emkup_elec_new_dyn[SolarPV, :] .= 0.235731 / 0.092
emkup_elec_old_dyn[Wind, 1] = 0.083299 / 0.079321
emkup_elec_new_dyn[Wind, 1] = 0.083299 / 0.064

emkup_ccs_dyn = ones(Float64, NumYears)
# gen_diff_dyn = gen_diff0

# --------------------------------------------------------------------------------------------------
# calibration on the CBAM policy variables
# --------------------------------------------------------------------------------------------------
# cbam_infoDir = joinpath(@__DIR__, "../input/policy/cbam_info.xlsx")
# cbam_info = DataFrame(XLSX.readtable(cbam_infoDir, scn_name))
# sec_carbon_price = Matrix(cbam_info)[1:NumSector, 3:end] 
# sec_cbam = Matrix(cbam_info)[NumSector+1:NumSector+NumSector, 3:end]
# cbam_indirect = Matrix(cbam_info)[NumSector+NumSector+1, 3:end]
# cbam_ratio = Matrix(cbam_info)[NumSector * 2 + 2 : NumSector * 3 + 1, 3 : end]
# rebate_ldcs_ratio = Matrix(cbam_info)[NumSector * 3 + 2 : NumSector * 3 + 1 + NumRegion, 3 : end]
# rebate_sec = Matrix(cbam_info)[NumSector * 3 + 1 + NumRegion + 1 : NumSector * 3 + 1 + NumRegion + NumSector, 3 : end]
# carbonPrice = Matrix(cbam_info)[NumSector * 4 + NumRegion + 2 : NumSector * 4 + NumRegion * 2 + 1, 3:end] ./ 100
# cbam_exempt = Matrix(cbam_info)[NumSector * 4 + NumRegion * 2 + 2 : NumSector * 4 + NumRegion * 3 + 1, 3]

# --------------------------------------------------------------------------------------------------
# calibration on the flw policy variables
# --------------------------------------------------------------------------------------------------
flw_rate_farm_30 = zeros(Float64, NumSector, NumRegion) .+ rr_farm # reduction rate
# flw_rate_proc_30 = zeros(Float64, NumSector, NumRegion) .+ 1
# flw_rate_dist_30 = zeros(Float64, NumSector, NumRegion) .+ 1
# flw_rate_srv_30 = zeros(Float64, NumSector, NumRegion) .+ 1
flw_rate_int_30 = zeros(Float64, NumSector, NumRegion) .+ rr_int
flw_rate_h_30 = zeros(Float64, NumSector, NumRegion) .+ rr_h



# ghgeq_prod0[CH4, :, :] .- fac_ghgeq_prod[CH4, :, :] .* prod0
