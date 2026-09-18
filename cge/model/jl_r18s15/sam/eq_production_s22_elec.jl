#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: define model equations
#---     May, 2023

function eq_production()
    # pprod + prodtax = pp
    @mapping(m, eq_pp[i in Sectors_Non_Elec, r in Regions], pprod[i, r] * (1 + trpd[i, r]) - pp[i, r])
    @complementarity(m, eq_pp, pp[Sectors_Non_Elec, Regions])

    # pint + pvae = pprod
    @mapping(m, eq_int[i in Sectors_Non_Elec, r in Regions], int[i, r] * pint[i, r] ^ sigmap[i, r] - aint[i, r] * prod[i, r] * pprod[i, r] ^ sigmap[i, r])
    @complementarity(m, eq_int, int)

    @mapping(m, eq_vae[i in Sectors_Non_Elec, r in Regions], vae[i, r] * pvae[i, r] ^ sigmap[i, r] - avae[i, r] * prod[i, r] * pprod[i, r] ^ sigmap[i, r])
    @complementarity(m, eq_vae, vae)

    @mapping(m, eq_pprod[i in Sectors_Non_Elec, r in Regions], pprod[i, r] ^ (1 - sigmap[i, r]) - aint[i, r] * pint[i,r] ^ (1 - sigmap[i, r]) - avae[i, r] * pvae[i, r] ^ (1 - sigmap[i, r]))
    @complementarity(m, eq_pprod, pprod)

    # qint = int
    @mapping(m, eq_qint[j in IntSec, i in Sectors_Non_Elec, r in Regions], qint[j, i, r] - aqint[j, i, r] * int[i, r])
    @complementarity(m, eq_qint, qint[IntSec, Sectors_Non_Elec, Regions])

    @mapping(m, eq_pint[i in Sectors_Non_Elec, r in Regions], pint[i, r] - sum(aqint[j, i, r] * (pa[j, r] * (1 + strint[j, i, r])) for j in IntSec))
    @complementarity(m, eq_pint, pint)

    # KEL + Land = vae for i in AgriSec
    @mapping(m, eq_kel[i in Sectors_Non_Elec, r in Regions], kel[i, r] * pkel[i, r] ^ sigmavae[i, r] - akel[i, r] * vae[i, r] * pvae[i, r] ^ sigmavae[i, r])
    @complementarity(m, eq_kel, kel)

    @mapping(m, eq_lnd[i in AgriSec, r in Regions], lnd[i, r] * (plnd[r] * (1 + trlnd[i, r])) ^ sigmavae[i, r] - alnd[i, r] * vae[i, r] * pvae[i, r] ^ sigmavae[i, r])
    @complementarity(m, eq_lnd, lnd)

    @mapping(m, eq_pvae_agri[i in AgriSec, r in Regions], pvae[i, r] ^ (1 - sigmavae[i, r]) - akel[i, r] * pkel[i, r] ^ (1 - sigmavae[i, r]) - alnd[i, r] * (plnd[r] * (1 + trlnd[i, r])) ^ (1 - sigmavae[i, r]))
    @complementarity(m, eq_pvae_agri, pvae[AgriSec, Regions])

    # KEL + Natural Resource = vae for i in NatSec
    @mapping(m, eq_ns[i in NatSec, r in Regions], ns[i, r] * (pns[i, r] * (1 + trns[i, r])) ^ sigmavae[i, r] - ans[i, r] * vae[i, r] * pvae[i, r] ^ sigmavae[i, r])
    @complementarity(m, eq_ns, ns)

    @mapping(m, eq_pvae_ns[i in NatSec, r in Regions], pvae[i, r] ^ (1 - sigmavae[i, r]) - akel[i, r] * pkel[i, r] ^ (1 - sigmavae[i, r]) - ans[i, r] * (pns[i, r] * (1 + trns[i, r])) ^ (1 - sigmavae[i, r]))
    @complementarity(m, eq_pvae_ns, pvae[NatSec, Regions])

    # KEL = VAE for i in other sectors non elec
    @mapping(m, eq_pvae_oth[i in OtherSec_Non_Elec, r in Regions], pvae[i, r] ^ (1 - sigmavae[i, r]) - akel[i, r] * pkel[i, r] ^ (1 - sigmavae[i, r]))
    @complementarity(m, eq_pvae_oth, pvae[OtherSec_Non_Elec, Regions])

    # va + ene = KEL
    @mapping(m, eq_kl[i in Sectors_Non_Elec, r in Regions], kl[i, r] * pkl[i, r] ^ sigmakel[i, r] - akl[i, r] * kel[i, r] * pkel[i, r] ^ sigmakel[i, r])
    @complementarity(m, eq_kl, kl)

    @mapping(m, eq_ene[i in Sectors_Non_Elec, r in Regions], lambdae[i, r] * ene[i, r] * pene[i, r] ^ sigmakel[i, r] - aene[i, r] * kel[i, r] * (lambdae[i, r] * pkel[i, r]) ^ sigmakel[i, r])
    @complementarity(m, eq_ene, ene)

    @mapping(m, eq_pkel[i in Sectors_Non_Elec, r in Regions], pkel[i, r] ^ (1 - sigmakel[i, r]) - akl[i, r] * pkl[i, r] ^ (1 - sigmakel[i, r]) - aene[i, r] * (pene[i, r] / lambdae[i, r]) ^ (1 - sigmakel[i, r]))
    @complementarity(m, eq_pkel, pkel)

    # fossil fuel + elec = ene
    @mapping(m, eq_fene[i in Sectors_Non_Elec, r in Regions], fene[i, r] * pfene[i, r] ^ sigmaene[i, r] - afene[i, r] * ene[i, r] * pene[i, r] ^ sigmaene[i, r])
    @complementarity(m, eq_fene, fene)

    @mapping(m, eq_elec[i in Sectors_Non_Elec, r in Regions], qint[PowerSec, i, r] * (pa[PowerSec, r] * (1 + strint[PowerSec, i, r])) ^ sigmaene[i, r] - aelec[i, r] * ene[i, r] * pene[i, r] ^ sigmaene[i, r])
    @complementarity(m, eq_elec, qint[PowerSec, Sectors_Non_Elec, Regions])

    @mapping(m, eq_pene[i in Sectors_Non_Elec, r in Regions], pene[i, r] ^ (1 - sigmaene[i, r]) - afene[i, r] * pfene[i, r] ^ (1 - sigmaene[i, r]) - aelec[i, r] * (pa[PowerSec, r] * (1 + strint[PowerSec, i, r])) ^ (1 - sigmaene[i, r]) )
    @complementarity(m, eq_pene, pene)

    # fossul fuel types += fene
    @mapping(m, eq_fens[j in FossilSec, i in Sectors_Non_Elec, r in Regions], qint[j, i, r] * (pa[j, r] * (1 + strint[j, i, r]) + etax[j, i, r]) ^ sigmafe[i ,r] - afens[j, i, r] * fene[i, r] * pfene[i, r] ^ sigmafe[i, r])
    @complementarity(m, eq_fens, qint[FossilSec, Sectors_Non_Elec, Regions])

    @mapping(m, eq_pfene[i in Sectors_Non_Elec, r in Regions], pfene[i, r] ^ (1 - sigmafe[i ,r]) - sum(afens[j, i, r] * (pa[j, r] * (1 + strint[j, i, r]) + etax[j, i, r]) ^ (1 - sigmafe[i ,r]) for j in FossilSec))
    @complementarity(m, eq_pfene, pfene)

    # k + l + lnd + ns = kl
    @mapping(m, eq_k[i in Sectors_Non_Elec, r in Regions], lambdak[i, r] * k[i, r] * (pk[r] * (1 + trk[i, r])) ^ sigmakl[i, r] - ak[i, r] * kl[i, r] * (lambdak[i, r] * pkl[i, r]) ^ sigmakl[i, r])
    @complementarity(m, eq_k, k[Sectors_Non_Elec, Regions])

    @mapping(m, eq_l[i in Sectors_Non_Elec, r in Regions], lambdal[i, r] * l[i, r] * (pl[r] * (1 + trl[i, r])) ^ sigmakl[i, r] - al[i, r] * kl[i, r] * (lambdal[i, r] * pkl[i, r]) ^ sigmakl[i, r])
    @complementarity(m, eq_l, l[Sectors_Non_Elec, Regions])

    @mapping(m, eq_pkl[i in Sectors_Non_Elec, r in Regions], pkl[i, r] ^ (1 - sigmakl[i, r]) - 
            ak[i, r] * (pk[r] * (1 + trk[i, r]) / lambdak[i, r]) ^ (1 - sigmakl[i, r]) - 
            al[i, r] * (pl[r] * (1 + trl[i, r]) / lambdal[i, r]) ^ (1 - sigmakl[i, r]))
    @complementarity(m, eq_pkl, pkl)
end

