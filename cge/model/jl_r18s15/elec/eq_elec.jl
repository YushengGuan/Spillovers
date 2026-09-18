#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_elec()
    # pint + pvae = pprod
    @mapping(m, eq_int_elec[i in ElecType, r in Regions], int_elec[i, r] * pint_elec[i, r] ^ sigmap_elec[i, r] - aint_elec[i, r] * gen_elec[i, r] * pgen_elec[i, r] ^ sigmap_elec[i, r])
    @complementarity(m, eq_int_elec, int_elec)

    @mapping(m, eq_vae_elec[i in ElecType, r in Regions], vae_elec[i, r] * pvae_elec[i, r] ^ sigmap_elec[i, r] - avae_elec[i, r] * gen_elec[i, r] * pgen_elec[i, r] ^ sigmap_elec[i, r])
    @complementarity(m, eq_vae_elec, vae_elec)

    @mapping(m, eq_pgen_elec[i in ElecType, r in Regions], pgen_elec[i, r] ^ (1 - sigmap_elec[i, r]) - aint_elec[i, r] * pint_elec[i, r] ^ (1 - sigmap_elec[i, r]) - avae_elec[i, r] * pvae_elec[i, r] ^ (1 - sigmap_elec[i, r]))
    @complementarity(m, eq_pgen_elec, pgen_elec)

    @mapping(m, eq_pgent_elec[i in ElecType, r in Regions], pgen_elec[i, r] * (1 + trpd_elec[i, r]) - pgent_elec[i, r])
    @complementarity(m, eq_pgent_elec, pgent_elec)

    # qint = int
    @mapping(m, eq_qint_elec[j in IntSec, i in ElecType, r in Regions], qint_elec[j, i, r] - aqint_elec[j, i, r] * int_elec[i, r])
    @complementarity(m, eq_qint_elec, qint_elec[IntSec, ElecType, Regions])

    @mapping(m, eq_pint_elec[i in ElecType, r in Regions], pint_elec[i, r] - sum(aqint_elec[j, i, r] * (pa[j, r] * (1 + strint_elec[j, i, r])) for j in IntSec))
    @complementarity(m, eq_pint_elec, pint_elec)

    # va + ene = vae
    @mapping(m, eq_va_elec[i in ElecType, r in Regions], va_elec[i, r] * pva_elec[i, r] ^ sigmavae_elec[i, r] - ava_elec[i, r] * vae_elec[i, r] * pvae_elec[i, r] ^ sigmavae_elec[i, r])
    @complementarity(m, eq_va_elec, va_elec)

    @mapping(m, eq_ene_elec[i in ElecType, r in Regions], lambdae_elec[i, r] * ene_elec[i, r] * pene_elec[i, r] ^ sigmavae_elec[i, r] - aene_elec[i, r] * vae_elec[i, r] * (lambdae_elec[i, r] * pvae_elec[i, r]) ^ sigmavae_elec[i, r])
    @complementarity(m, eq_ene_elec, ene_elec)

    @mapping(m, eq_pvae_elec[i in ElecType, r in Regions], pvae_elec[i, r] ^ (1 - sigmavae_elec[i, r]) - ava_elec[i, r] * pva_elec[i, r] ^ (1 - sigmavae_elec[i, r]) - aene_elec[i, r] * (pene_elec[i, r] / lambdae_elec[i, r]) ^ (1 - sigmavae_elec[i, r]))
    @complementarity(m, eq_pvae_elec, pvae_elec)

    # energy types += ene
    @mapping(m, eq_ens_elec[j in EnergySec, i in ElecType, r in Regions], qint_elec[j, i, r] * (pa[j, r] * (1 + strint_elec[j, i, r]) + etax_elec[j, i, r]) ^ sigmaene_elec[i ,r] - aens_elec[j, i, r] * ene_elec[i, r] * pene_elec[i, r] ^ sigmaene_elec[i, r])
    @complementarity(m, eq_ens_elec, qint_elec[EnergySec, ElecType, Regions])

    @mapping(m, eq_pene_elec[i in ElecType, r in Regions], pene_elec[i, r] ^ (1 - sigmaene_elec[i ,r]) - sum(aens_elec[j, i, r] * (pa[j, r] * (1 + strint_elec[j, i, r]) + etax_elec[j, i, r]) ^ (1 - sigmaene_elec[i, r]) for j in EnergySec))
    @complementarity(m, eq_pene_elec, pene_elec)

    # k + l = va
    @mapping(m, eq_k_elec[i in ElecType, r in Regions], lambdak_elec[i, r] * k_elec[i, r] * (pk[r] * (1 + trk_elec[i, r])) ^ sigmava_elec[i, r] - ak_elec[i, r] * va_elec[i, r] * (lambdak_elec[i, r] * pva_elec[i, r]) ^ sigmava_elec[i, r])
    @complementarity(m, eq_k_elec, k_elec)

    @mapping(m, eq_l_elec[i in ElecType, r in Regions], lambdal_elec[i, r] * l_elec[i, r] * (pl[r] * (1 + trl_elec[i, r])) ^ sigmava_elec[i, r] - al_elec[i, r] * va_elec[i, r] * (lambdal_elec[i, r] * pva_elec[i, r]) ^ sigmava_elec[i, r])
    @complementarity(m, eq_l_elec, l_elec)

    @mapping(m, eq_pva_elec[i in ElecType, r in Regions], pva_elec[i, r] ^ (1 - sigmava_elec[i, r]) - ak_elec[i, r] * (pk[r] * (1 + trk_elec[i, r]) / lambdak_elec[i, r]) ^ (1 - sigmava_elec[i, r]) - al_elec[i, r] * (pl[r] * (1 + trl_elec[i, r]) / lambdal_elec[i, r]) ^ (1 - sigmava_elec[i, r]))
    @complementarity(m, eq_pva_elec, pva_elec)

    @mapping(m, eq_tint_elec[j in Goods, r in Regions], qint[j, PowerSec, r] - sum(qint_elec[j, i, r] for i in ElecType))
    @complementarity(m, eq_tint_elec, qint[Goods, PowerSec, Regions])

    @mapping(m, eq_tk_elec[r in Regions], k[PowerSec, r] - sum(k_elec[i, r] for i in ElecType))
    @complementarity(m, eq_tk_elec, k[PowerSec, Regions])

    @mapping(m, eq_tl_elec[r in Regions], l[PowerSec, r] - sum(l_elec[i, r] for i in ElecType))
    @complementarity(m, eq_tl_elec, l[PowerSec, Regions])

    @mapping(m, eq_gen_elec[i in GenType, r in Regions], gen_elec[i, r] * pgent_elec[i, r] ^ sigmaelec[r] - agen_elec[i, r] * totgen_elec[r] * ptotgen_elec[r] ^ sigmaelec[r])
    @complementarity(m, eq_gen_elec, gen_elec[GenType, Regions])

    @mapping(m, eq_ptotgen_elec[r in Regions], ptotgen_elec[r] ^ (1 - sigmaelec[r]) - sum(agen_elec[i, r] * pgent_elec[i, r] ^ (1 - sigmaelec[r]) for i in ElecType))
    @complementarity(m, eq_ptotgen_elec, ptotgen_elec)

    @mapping(m, eq_td_elec[r in Regions], gen_elec[TnDType, r] - atd[r] * prod[PowerSec, r])
    @complementarity(m, eq_td_elec, gen_elec[TnDType, Regions])

    @mapping(m, eq_totgen_elec[r in Regions], totgen_elec[r] - atgen[r] * prod[PowerSec, r])
    @complementarity(m, eq_totgen_elec, totgen_elec)

    @mapping(m, eq_pp_elec[r in Regions], atd[r] * pgent_elec[TnDType, r] + atgen[r] * ptotgen_elec[r] - pp[PowerSec, r])
    @complementarity(m, eq_pp_elec, pp[PowerSec, Regions])
end