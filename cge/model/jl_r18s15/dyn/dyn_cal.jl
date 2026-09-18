#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: calibration of the dynamic exogenous parameters (not policy varaibles)
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# calibration on the dynamic exogenous parameters
# --------------------------------------------------------------------------------------------------
depr = 0.05 # depreciation rate
ir = 0.03 # interest rate

# -- exogenous investment decision making procedure
kav0 = (sum(k0, dims=1)[1, :] .* pk0 ./ (ptinv0 .* (depr + ir)) .- tinv0) ./ (1 - depr)
deprir = sum(k0, dims=1)[1, :] ./ kav0

# Production factors
lab_supp = zeros(Float64, NumRegion, NumYears)
lab_supp[1:NumRegion, 1] = sum(l0, dims=1)[1, :]
cap_supp = zeros(Float64, NumRegion, NumYears)
cap_supp[1:NumRegion, 1] = sum(k0, dims=1)[1, :]
#  .- sum(k_elec0 .* (1 .- shr_elec_new), dims=1)[1, :]
lnd_supp = zeros(Float64, NumRegion, NumYears)
lnd_supp[1:NumRegion, 1] = sum(lnd0, dims=1)[1, :]
# tarab_supp = zeros(Float64, NumAEZ, NumRegion, NumYears)
# tarab_supp[:, :, 1] = tarab0
ns_supp = zeros(Float64, NumSector, NumRegion, NumYears)
ns_supp[1:NumSector, 1:NumRegion, 1] = ns0
tinv_supp = zeros(Float64, NumRegion, NumYears)
tinv_supp[1:NumRegion, 1] = tinv0

lambdae_supp = ones(Float64, NumSector, NumRegion, NumYears)
lambdaedir = joinpath(pwd(), "../input/dyn/long-term/lambdae_2100.csv")
lambdae_gr = CSV.read(lambdaedir, DataFrames.DataFrame, header=1)[:, 2:end]

# Exogenous variables
rgdp_bau_exg = zeros(Float64, NumRegion, NumYears)
rgdp_bau_exg[1:NumRegion, 1] = gdp0

ks_elec_old_dyn = zeros(Float64, NumElec, NumRegion, NumYears)
# ks_elec_old_dyn[:, :, 1] = k_elec0 .* (1 .- shr_elec_new)
tfp_bau_endo = zeros(Float64, NumRegion, NumYears)
# --------------------------------------------------------------------------------------------------
# calibration on the GDP & POP growth rate data
# --------------------------------------------------------------------------------------------------
# macro growth rate

if yrgap == 1
    gdpgrdir = joinpath(pwd(), "../input/dyn/short-term/GDP_2035_r18_new.csv")
    gdpgr_short = CSV.read(gdpgrdir, DataFrames.DataFrame, header=1)
    popgrdir = joinpath(pwd(), "../input/dyn/short-term/POP_2035_r18_new.csv")
    popgr_short = CSV.read(popgrdir, DataFrames.DataFrame, header=1)

    gdpgr_longdir = joinpath(pwd(), "../input/dyn/long-term/GDP_SSPN.csv")
    gdpgr_long = CSV.read(gdpgr_longdir, DataFrames.DataFrame, header=1)
    popgr_longdir = joinpath(pwd(), "../input/dyn/long-term/POP_SSP2.csv")
    popgr_long = CSV.read(popgr_longdir, DataFrames.DataFrame, header=1)

    function annual_growth_rates(short_data, long_data, years)
        short_years = parse.(Int, replace.(String.(names(short_data)[2:end]), "gr" => ""))
        long_years = parse.(Int, replace.(String.(names(long_data)[2:end]), "gr" => ""))
        short_rates = Matrix(short_data[:, 2:end])
        long_rates = Matrix(long_data[:, 2:end])
        rates = zeros(Float64, size(short_rates, 1), length(years) - 1)

        for (idx, year) in enumerate(years[1:end-1])
            short_pos = findfirst(==(year), short_years)
            if !isnothing(short_pos)
                rates[:, idx] = short_rates[:, short_pos]
            else
                long_pos = findfirst(>(year), long_years)
                if isnothing(long_pos)
                    long_pos = length(long_years)
                end
                rates[:, idx] = long_rates[:, long_pos]
            end
        end

        return rates
    end

    gdpgr = annual_growth_rates(gdpgr_short, gdpgr_long, Years)
    popgr = annual_growth_rates(popgr_short, popgr_long, Years)

    if tfp_flag == "TFP"
        try
            tfpgrdir = joinpath(pwd(), "../input/dyn/short-term/TFP_2035_new.csv")
            global tfp_bau_exg = CSV.read(tfpgrdir, DataFrames.DataFrame, header=1)[:, :]
        catch
            println("No baseline TFP data!")
        end
        println("tfp_bau_exg")
        println(tfp_bau_exg)
    end


elseif yrgap == 5
    # gdpgrdir = joinpath(pwd(), "../input/dyn/long-term/GDP_SSP2.csv")
    gdpgrdir = joinpath(pwd(), "../input/dyn/long-term/GDP_SSPN.csv")
    gdpgr = CSV.read(gdpgrdir, DataFrames.DataFrame, header=1)[:, 2:end]

    popgrdir = joinpath(pwd(), "../input/dyn/long-term/POP_SSP2.csv")
    popgr = CSV.read(popgrdir, DataFrames.DataFrame, header=1)[:, 2:end]

    try
        tfpgrdir = joinpath(pwd(), "../input/dyn/long-term/TFP_BAU.csv")
        global tfp_bau_exg = CSV.read(tfpgrdir, DataFrames.DataFrame, header=1)[:, :]
    catch
        println("No baseline TFP data!")
    end
end


# tfpbaudir = joinpath(pwd(), "../input/dyn/short-term/TFP_Calibrated.csv")
# tfpbau = CSV.read(tfpgrdir, DataFrames.DataFrame, header=1)[:, 2:end]


# dynamic adjustment of saving rate
savrt = tinv0 ./ gdp0
sav_dyn = ones(Float64, NumRegion, NumYears-1)
# savrt .* [1.15, 3, 1.0] 
sav_dyn[2:2, :] .= gdpgr[2:2, 1:NumYears-1] ./ gdpgr[2, 1] .* 0.5 .+ 0.5
sav_dyn
