#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: read data of the energy and emissions
#---     May, 2023

# --------------------------------------------------------------------------------------------------
# Production Behavior
# --------------------------------------------------------------------------------------------------
qint_elec0 = Vqint_elec0 ./ reshape(pa0, (NumGood, 1, NumRegion))
qint_elec0 = replace(qint_elec0, NaN=>0)
qint_elec0[FossilSec, :, :]
strint_elec = zeros(Float64, NumGood, NumElec, NumRegion)
for i in ElecType
    strint_elec[:, i, :] = strint[:, PowerSec, :]
end

# -- energy demand
ene_elec0 = sum(qint_elec0[EnergySec, ElecType, Regions], dims=1)[1, :, :] # total fossil fuel demand
pene_elec0 = sum(qint_elec0[j, ElecType, Regions] .* pa0[j, Regions]' .* (1 .+ strint_elec[j, ElecType, Regions]) for j in EnergySec) ./ ene_elec0
pene_elec0 = replace(pene_elec0, NaN=>1)
aens_elec = zeros(Float64, NumGood, NumElec, NumRegion)
for j in EnergySec
    for i in ElecType
        for r in Regions
            aens_elec[j, i, r] = qint_elec0[j, i, r] * (pa0[j, r] * (1 + strint_elec[j, i, r])) ^ sigmaene_elec[i ,r] / (ene_elec0[i, r] * pene_elec0[i, r] ^ sigmaene_elec[i, r])
        end
    end
end
strint_elec[findall(isnan, aens_elec)] .= 0
aens_elec[EnergySec[1], :, :] = replace(aens_elec[EnergySec[1], :, :], NaN=>1)
aens_elec = replace(aens_elec, NaN=>0)

# -- Other Intermediate Demand
int_elec0 = sum(qint_elec0[IntSec, ElecType, Regions], dims=1)[1,:,:]
aqint_elec = qint_elec0 ./ (sum(qint_elec0[IntSec, ElecType, Regions], dims=1))
pint_elec0 = sum(qint_elec0[j, ElecType, Regions] .* pa0[j, Regions]' .* (1 .+ strint_elec[j, ElecType, Regions]) for j in IntSec) ./ int_elec0
pint_elec0 = replace(pint_elec0, NaN=>1)
strint_elec[findall(isnan, aqint_elec)] .= 0
aqint_elec[1, :, :] = replace(aqint_elec[1, :, :], NaN=>1)
aqint_elec = replace(aqint_elec, NaN=>0)

pp_elec0 = ones(Float64, NumElec, NumRegion) # price of armington goods

# -- Production Factors
k_elec0 = Vvaelec0[3, :, :] ./ pk0'
l_elec0 = (Vvaelec0[1, :, :] .+ Vvaelec0[2, :, :]) ./ pl0'

idx_k_elec_yes = findall(x -> x != 0, k_elec0)
idx_k_elec_yes_2 = [(i[1], i[2]) for i in idx_k_elec_yes]
idx_k_elec_no = findall(x -> x == 0, k_elec0)

# -- Tax rate on production factors
trl_elec = (vatax_elec0[1, :, :] .+ vatax_elec0[2, :, :]) ./ (l_elec0 .* pl0')
trk_elec = vatax_elec0[3, :, :] ./ (k_elec0 .* pk0')
trl_elec = replace(trl_elec, NaN=>0)
trk_elec = replace(trk_elec, NaN=>0)

# -- Aggregation of production factors
va_elec0 = k_elec0 .+ l_elec0
pva_elec0 = (k_elec0 .* pk0' .* (1 .+ trk_elec) .+ l_elec0 .* pl0' .* (1 .+ trl_elec)) ./ va_elec0
ak_elec = (k_elec0 .* (pk0' .* (1 .+ trk_elec)) .^ sigmava_elec) ./ (va_elec0 .* pva_elec0 .^ sigmava_elec)
al_elec = (l_elec0 .* (pl0' .* (1 .+ trl_elec)) .^ sigmava_elec) ./ (va_elec0 .* pva_elec0 .^ sigmava_elec)

pva_elec0 = replace(pva_elec0, NaN=>1)
ak_elec = replace(ak_elec, NaN=>1)
al_elec = replace(al_elec, NaN=>0)

# -- Aggregation of production factors and capital demand
vae_elec0 = va_elec0 .+ ene_elec0
pvae_elec0 = (va_elec0 .* pva_elec0 + ene_elec0 .* pene_elec0) ./ vae_elec0
ava_elec = (va_elec0 .* pva_elec0 .^ sigmavae_elec) ./ (vae_elec0 .* pvae_elec0 .^ sigmavae_elec)
aene_elec = (ene_elec0 .* pene_elec0 .^ sigmavae_elec) ./ (vae_elec0 .* pvae_elec0 .^ sigmavae_elec)

pvae_elec0 = replace(pvae_elec0, NaN=>1)
ava_elec = replace(ava_elec, NaN=>1)
aene_elec = replace(aene_elec, NaN=>0)

# -- Aggregation of vae and intermediate inputs
prodtax_elec0
gen_elec0 = zeros(Float64, NumElec, NumRegion)
gen_elec0[GenType, :] = Vgen0
gen_elec0[TnDType, :] = sum(Vgen0, dims=1)[1, :]
gen_elec0
pgen_elec0 = (vae_elec0 .* pvae_elec0 .+ int_elec0 .* pint_elec0) ./ gen_elec0
# println("vae_elec0:", vae_elec0)
# println(pvae_elec0)
# println(int_elec0)
# println(pint_elec0)
pgen_elec0 = replace(pgen_elec0, NaN=>1)
trpd_elec = prodtax_elec0 ./ (vae_elec0 .* pvae_elec0 .+ int_elec0 .* pint_elec0)
trpd_elec = replace(trpd_elec, NaN=>0)
pgent_elec0 = (1 .+ trpd_elec) .* pgen_elec0
avae_elec = (vae_elec0 .* pvae_elec0 .^ sigmap_elec) ./ (gen_elec0 .* pgen_elec0 .^ sigmap_elec)
aint_elec = (int_elec0 .* pint_elec0 .^ sigmap_elec) ./ (gen_elec0 .* pgen_elec0 .^ sigmap_elec)

avae_elec = replace(avae_elec, NaN=>1)
aint_elec = replace(aint_elec, NaN=>0)

# Power Generation Cost
totgen_elec0 = sum(gen_elec0[GenType, :], dims=1)[1, :]
ptotgen_elec0 = sum(gen_elec0[GenType, :] .* pgent_elec0[GenType, :], dims=1)[1, :] ./ totgen_elec0
agen_elec0 = zeros(Float64, NumElec, NumRegion)
for i in GenType, r in Regions
    agen_elec0[i, r] = (gen_elec0[i, r] * pgent_elec0[i, r] ^ sigmaelec[r]) / (totgen_elec0[r] * ptotgen_elec0[r] ^ sigmaelec[r])
end
println("pgent_elec0[9, 16]:", pgent_elec0[9, 16])
println("pgent_elec0[:, 16]:", pgent_elec0[:, 16])
println("pgent_elec0[9, :]:", pgent_elec0[9, :])
println("agen_elec0[9, 16]:", agen_elec0[9, 16])
println("agen_elec0[:, 16]:", agen_elec0[:, 16])
println("agen_elec0[9, :]:", agen_elec0[9, :])
println("gen_elec0:", gen_elec0[9, 16])
println("totgen_elec0[2]:", totgen_elec0[2])
println(:"sum of gen_elec0[:, 2]:", sum(gen_elec0[:, 2]))
println("gen_elec0[1, 2]:", gen_elec0[1, 2])
println("totgen_elec0[3:", totgen_elec0[3])
println(:"sum of gen_elec0[:, 3]:", sum(gen_elec0[:, 3]))
println("share_elec0[2, 2]:", gen_elec0[2, 2] / totgen_elec0[2])
atd = gen_elec0[TnDType, :] ./ prod0[PowerSec, :]
atgen = totgen_elec0 ./ prod0[PowerSec, :]
# --------------------------------------------------------------------------------------------------
# Energy Demand and Carbon Emissions
# --------------------------------------------------------------------------------------------------
enefac_elec = zeros(Float64, NumGood, NumElec, NumRegion)
for i in ElecType
    enefac_elec[:, i, :] = enefac_int[:, PowerSec, :]
end

emisfac_elec = zeros(Float64, NumGood, NumElec, NumRegion)

for i in ElecType, j in FossilSec, r in Regions
    if qint_elec0[j, i, r] != 0
        emisfac_elec[j, i, r] = emisfac_int[j, PowerSec, r]
    end
end
emisfac_elec[FossilSec, :, 1]
eint_elec0 = enefac_elec .* qint_elec0
emis_elec0 = emisfac_elec .* qint_elec0