#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: calibration of the core model
#---     May, 2023


# --------------------------------------------------------------------------------------------------
# Basic price based on the law of one price
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Trade
# --------------------------------------------------------------------------------------------------
# -- Bilateral Trade
er0 = ones(Float64, NumRegion)' #exchange rate 
ptrst0 = 1 # assume as one as the price of international trade supplier
pe0 = ones(Float64, NumGood, NumRegion) # export price
imrr0 = (Vimrr0 .- te0) ./ pe0
pfob0 = Vimrr0 ./ imrr0
ter = te0 ./ (imrr0 .* pe0)

qtmg0 = margin0 ./ ptrst0 ./ imrr0 # quantity of margin
pcif0 = pfob0 .+ qtmg0 * ptrst0 # add trade margin as world CIF price 
tmr = tm0 ./ (imrr0 .* pcif0) # import tariff rate, ad valorem tax
imt0 = sum(imrr0, dims=2)[:, 1, :] # import volumns from region r
pm0 = sum(pcif0 .* (1 .+ tmr) .* imrr0, dims=2)[:, 1, :] ./ imt0 .* er0 # average import price of region r
aimrr = zeros(Float64, NumGood, NumRegion, NumRegion)
for j in Goods
    for r in Regions
        for rr in Regions
            aimrr[j, r, rr] = imrr0[j, r, rr] * (pcif0[j, r, rr] * (1 + tmr[j, r, rr])) ^ sigmarr[j, rr] / (imt0[j, rr] * pm0[j, rr] ^ sigmarr[j, rr])
        end
    end
end

# 计算平均进口税率
tmrm = sum(tmr .* pcif0 .* imrr0, dims=2)[:, 1, :] ./ sum((1 .+ tmr) .* pcif0 .* imrr0, dims=2)[:, 1, :]

# 计算平均出口税率
term = sum(te0, dims=3)[:, :, 1] ./ sum(imrr0, dims=3)[:, :, 1] 

# 计算平均margin量
qtmgm0 = sum(margin0, dims=2)[:, 1, :] ./ imt0 ./ ptrst0

#总进口量不含税
# -- Import v.s. Domestic
pdm0 = ones(Float64, NumGood, NumRegion) # domestic supply price
dmd0 = Vdmd0 ./ pdm0 # domestically produced for domestic demand
tdd0 = (Vconsh0 .+ Vconsg0 .+ Vinv0 .+ sum(Vqint0, dims=2)[:, 1, :])
pa0 =  (pdm0 .* dmd0 .+ pm0 .* imt0) ./ tdd0 # price of armington goods
aimt = imt0 .* pm0 .^ sigmam ./ (tdd0 .* pa0 .^ sigmam) # share of imported goods
admd = dmd0 .* pdm0 .^ sigmam ./ (tdd0 .* pa0 .^ sigmam) # share of domestically produced goods
# -- Export v.s. Domestic
# !! -- to do: check the export tax
ext0 = sum(imrr0, dims=3)[:, :, 1]
qs0 = sum(pe0 .* imrr0, dims=3)[:, :, 1] .+ dmd0 # supply level
pp0 = ones(Float64, NumGood, NumRegion) # price of armington goods
aext = ext0 .* pe0 .^ sigmae ./ (qs0 .* pp0 .^ sigmae) # share of imported goods
adms = dmd0 .* pdm0 .^ sigmae ./ (qs0 .* pp0 .^ sigmae) # share of domestically produced goods

# -- International Trade Supplier
qtrs0 = Vqtrs0 ./ pp0[TransSec, :]
trst0 = sum(pp0[TransSec, :] .* qtrs0) ./ ptrst0
atrs = qtrs0 .* pp0[TransSec, :] .^ sigmatrs ./ (trst0 .* ptrst0 .^ sigmatrs)

# --------------------------------------------------------------------------------------------------
# Consumption Behavior
# --------------------------------------------------------------------------------------------------
consh0 = Vconsh0 ./ pa0
strh = stax_fd0[:, 1, :] ./ (consh0 .* pa0) # sale tax rate on households
strh = replace(strh, NaN=>0)
tch0 = sum(consh0 .* pa0 .* (1 .+ strh), dims=1)[1, :]
thetah = consh0 .* pa0 .* (1 .+ strh) ./ sum(consh0 .* pa0 .* (1 .+ strh), dims=1) # household consumption share - basic
# Extended Linear Expenditure System for household consumption
etah = etah .+ thetah .* (1 .- sum(thetah .* etah, dims=1)) ./ sum(thetah .* thetah, dims=1)
muh = etah .* thetah
minh = consh0 .* (1 .+ etah ./ (-2))

consg0 = Vconsg0 ./ pa0
strg = stax_fd0[:, 2, :] ./ (consg0 .* pa0) # sale tax rate on government
strg = replace(strg, NaN=>0)
tcg0 = sum(consg0 .* pa0 .* (1 .+ strg), dims=1)[1, :]
thetag = consg0 .* pa0 .* (1 .+ strg) ./ sum(consg0 .* pa0 .* (1 .+ strg), dims=1) # household consumption share - basic

inv0 = Vinv0 ./ pa0
strinv = stax_fd0[:, 3, :] ./ (inv0 .* pa0) # sale tax rate on investment
strinv = replace(strinv, NaN=>0)

tinv0 = sum(inv0, dims=1)[1, :]
ptinv0 = sum(inv0 .* (pa0 .* (1 .+ strinv)), dims=1)[1, :] ./ tinv0 # keep constant !! -- to do: check
ainv = (inv0 .* (pa0 .* (1 .+ strinv)) .^ sigmav') ./ (tinv0 .* ptinv0 .^ sigmav)'
# ainv = inv0 .* pa0 .* (1 .+ strinv) ./ (ptinv0 .* tinv0)'
# --------------------------------------------------------------------------------------------------
# Production Behavior
# --------------------------------------------------------------------------------------------------
qint0 = Vqint0 ./ reshape(pa0, (NumGood, 1, NumRegion))
strint = stax_int0 ./ (qint0 .* reshape(pa0, (NumGood, 1, NumRegion)))

# -- fossil fuel demand
fene0 = sum(qint0[FossilSec, Sectors, Regions], dims=1)[1, :, :] # total fossil fuel demand
pfene0 = sum(qint0[j, Sectors, Regions] .* pa0[j, Regions]' .* (1 .+ strint[j, Sectors, Regions]) for j in FossilSec) ./ fene0
afens = zeros(Float64, NumGood, NumSector, NumRegion)
for j in FossilSec
    for i in Sectors
        for r in Regions
            afens[j, i, r] = qint0[j, i, r] * (pa0[j, r] * (1 + strint[j, i, r])) ^ sigmafe[i ,r] / (fene0[i, r] * pfene0[i, r] ^ sigmafe[i, r])
        end
    end
end

# -- energy demand
ene0 = fene0 .+ qint0[PowerSec, Sectors, Regions] # total energy demand
pene0 = (pfene0 .* fene0 .+ (pa0[PowerSec, :]' .* (1 .+ strint[PowerSec, Sectors, Regions])) .* 
        qint0[PowerSec, Sectors, Regions]) ./ ene0 # price of energy demand
afene = (fene0 .* pfene0 .^ sigmaene) ./ (ene0 .* pene0 .^ sigmaene)
aelec = (qint0[PowerSec, Sectors, Regions] .* 
        (pa0[PowerSec, :]' .* (1 .+ strint[PowerSec, Sectors, Regions])) .^ sigmaene) ./ 
        (ene0 .* pene0 .^ sigmaene)

# -- Other Intermediate Demand
int0 =sum(qint0[IntSec, Sectors, Regions], dims=1)[1,:,:]
aqint = qint0 ./ (sum(qint0[IntSec, Sectors, Regions], dims=1))
pint0 = sum(qint0[j, Sectors, Regions] .* pa0[j, Regions]' .* (1 .+ strint[j, Sectors, Regions]) for j in IntSec) ./ int0

# -- Production Factors
pk0 = ones(Float64, NumRegion) # capital price
pl0 = ones(Float64, NumRegion) # labor price
plnd0 = ones(Float64, NumRegion) # land price
pns0 = ones(Float64, NumSector, NumRegion) # natural resource price, sector-specific
k0 = Vvam0[3, :, :] ./ pk0'
l0 = (Vvam0[1, :, :] .+ Vvam0[2, :, :]) ./ pl0'
lnd0 = Vvam0[4, :, :] ./ plnd0'
ns0 = Vvam0[5, :, :] ./ pns0

# -- Tax rate on production factors
trl = (vatax0[1, :, :] .+ vatax0[2, :, :]) ./ (l0 .* pl0')
trk = vatax0[3, :, :] ./ (k0 .* pk0')
trlnd = vatax0[4, :, :] ./ (lnd0 .* plnd0')
trlnd = replace(trlnd, NaN=>0)
trns = vatax0[5, :, :] ./ (ns0 .* pns0)
trns = replace(trns, NaN=>0)

# -- Income Tax rate on production factors
trlinc = (inctax0[1, :, :] .+ inctax0[2, :, :]) ./ (l0 .* pl0')
trkinc = inctax0[3, :, :] ./ (k0 .* pk0')
trlndinc = inctax0[4, :, :] ./ (lnd0 .* plnd0')
trlndinc = replace(trlndinc, NaN=>0)
trnsinc = inctax0[5, :, :] ./ (ns0 .* pns0)
trnsinc = replace(trnsinc, NaN=>0)

# -- Aggregation of production factors
kl0 = k0 .+ l0
pkl0 = (k0 .* pk0' .* (1 .+ trk) .+ 
        l0 .* pl0' .* (1 .+ trl)) ./ kl0
ak = (k0 .* (pk0' .* (1 .+ trk)) .^ sigmakl) ./ (kl0 .* pkl0 .^ sigmakl)
al = (l0 .* (pl0' .* (1 .+ trl)) .^ sigmakl) ./ (kl0 .* pkl0 .^ sigmakl)

# -- Aggregation of production factors and energy demand
kel0 = kl0 .+ ene0
pkel0 = (kl0 .* pkl0 .+ ene0 .* pene0) ./ kel0
akl = (kl0 .* pkl0 .^ sigmakel) ./ (kel0 .* pkel0 .^ sigmakel)
aene = (ene0 .* pene0 .^ sigmakel) ./ (kel0 .* pkel0 .^ sigmakel)

# -- Aggregation of kel and land/natural resources
vae0 = kel0 .+ lnd0 .+ ns0
pvae0 = (kel0 .* pkel0 .+ lnd0 .* (plnd0' .* (1 .+ trlnd)) .+ ns0 .* (pns0 .* (1 .+ trns))) ./ vae0
alnd = (lnd0 .* (plnd0' .* (1 .+ trlnd)) .^ sigmavae) ./ (vae0 .* pvae0 .^ sigmavae)
ans = (ns0 .* (pns0 .* (1 .+ trns)) .^ sigmavae) ./ (vae0 .* pvae0 .^ sigmavae)
akel = (kel0 .* pkel0 .^ sigmavae) ./ (vae0 .* pvae0 .^ sigmavae)

# -- Aggregation of vae and intermediate inputs
prod0 = (vae0 .* pvae0 .+ int0 .* pint0 .+ prodtax0)
pprod0 = (vae0 .* pvae0 .+ int0 .* pint0) ./ prod0
trpd = prodtax0 ./ (vae0 .* pvae0 .+ int0 .* pint0)
avae = (vae0 .* pvae0 .^ sigmap) ./ (prod0 .* pprod0 .^ sigmap)
aint = (int0 .* pint0 .^ sigmap) ./ (prod0 .* pprod0 .^ sigmap)
# --------------------------------------------------------------------------------------------------
# Income Distribution
# --------------------------------------------------------------------------------------------------
# -- income from different factors
tlinc0 = sum((1 .- trlinc) .* l0 .* pl0', dims=1)[1, :]
tkinc0 = sum((1 .- trkinc) .* k0 .* pk0', dims=1)[1, :]
tlndinc0 = sum((1 .- trlndinc) .* lnd0 .* plnd0', dims=1)[1, :]
tnsinc0 = sum((1 .- trnsinc) .* ns0 .* pns0, dims=1)[1, :]

inch0 = tlinc0 .+ Vcapital0[1, :] .+ tlndinc0 .+ tnsinc0 # income of households

# -- income of government through taxes
incg0 = sum(
    trpd .* pprod0 .* prod0 .+ # production tax
    trk .* k0 .* pk0' .+ # capital tax in production stage
    trl .* l0 .* pl0' .+ # labor tax
    trlnd .* lnd0 .* plnd0' .+ # land tax
    trns .* ns0 .* pns0 .+ # natural resource tax
    trkinc .* k0 .* pk0' .+ # income tax on capital
    trlinc .* l0 .* pl0' .+ # labor income tax
    trlndinc .* lnd0 .* plnd0' .+ # land income tax
    trnsinc .* ns0 .* pns0 .+ # natural resource income tax
    sum(strint[j, :, :] .* qint0[j, :, :] .* pa0[j, :]' for j in Goods) .+ # sale tax on intermediates
    strh .* consh0 .* pa0 .+ # sale tax on households
    strg .* consg0 .* pa0 .+ # sale tax on households
    strinv .* inv0 .* pa0 .+ # sale tax on households
    sum(ter .* imrr0, dims=3)[:, :, 1] .* pe0 .+ # export tax
    sum(tmr .* pcif0 .* imrr0, dims=2)[:, 1, :] # import tax
    , dims = 1)[1, :]

# --------------------------------------------------------------------------------------------------
# Saving & Investment
# --------------------------------------------------------------------------------------------------
# -- saving from different institutions
savg0 = incg0 .- tcg0 # saving of government as the imbalance between income and consumption
asavg = savg0 ./ incg0

savk0 = Vcapital0[2, :] .* 0 # saving of capital
aksav = savk0 ./ tkinc0
akh = 1 .- aksav
inch0 = tlinc0 .+ Vcapital0[1, :] .+ tlndinc0 .+ tnsinc0 .+ Vcapital0[2, :] 
savh0 = inch0 .- tch0 # saving of household
asavh = savh0 ./ inch0
save0 = sum(Vsave0, dims=1)[1, :] # saving of foreigners

savtrs0 = sum(imrr0 .* qtmg0 .* ptrst0, dims=(1, 2))[1, 1, :] - pp0[TransSec, :] .* qtrs0

# -- investment from different institutions: exogenous setting on investment for long-term running
ainvg = savg0 ./ (tinv0 .* ptinv0 .- savtrs0 .- save0 .- savg0)
ainvh = savh0 ./ (tinv0 .* ptinv0 .- savtrs0 .- save0 .- savg0)
ainvk = savk0 ./ (tinv0 .* ptinv0 .- savtrs0 .- save0 .- savg0)

# -- √ check balance between saving and investment 
diff_savinv = tinv0 .* ptinv0 .- (savk0 .+ savh0 .+ savg0 .+ save0 .+ savtrs0)
# -- √ check balance between saving of foreigners and net export

diff_save = sum(sum(pfob0 .* imrr0, dims=3)[:, :, 1], dims=1)[1, :] .+ save0 .- sum(pfob0 .* imrr0, dims=(1, 2))[1, 1, :]

# -- √ check balance between total demand and total supply

# --------------------------------------------------------------------------------------------------
# Macro Variables
# --------------------------------------------------------------------------------------------------
gdp0 = sum((consh0 .+ consg0 .+ inv0) .* pa0 .+ sum(imrr0 .* pfob0, dims = 3)[:, :, 1] .- sum(imrr0 .* pcif0, dims=2)[:, 1, :], dims=1)[1, :] .+ pp0[TransSec, :] .* qtrs0

savrt = tinv0 .* ptinv0 ./ gdp0
savh0 ./ gdp0

tinv0