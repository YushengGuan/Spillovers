#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables
#---     May, 2023

@variables m begin
    # initialization of price
    pva_elec[i = ElecType, rr = Regions], (start=pva_elec0[i, rr])
    pene_elec[i = ElecType, rr = Regions], (start=pene_elec0[i, rr])
    pvae_elec[i = ElecType, rr = Regions], (start=pvae_elec0[i, rr])
    pint_elec[i = ElecType, rr = Regions], (start=pint_elec0[i, rr])
    pgen_elec[i = ElecType, rr = Regions], (start=pgen_elec0[i, rr])
    pgent_elec[i = ElecType, rr = Regions], (start=pgent_elec0[i, rr])
    # pp_elec[i = ElecType, rr = Regions], (start=pp_elec0[i, rr])
    
    # initialization of inputs & outputs
    k_elec[i = ElecType, rr = Regions], (start=k_elec0[i, rr])
    l_elec[i = ElecType, rr = Regions], (start=l_elec0[i, rr])
    va_elec[i = ElecType, rr = Regions], (start=va_elec0[i, rr])
    vae_elec[i = ElecType, rr = Regions], (start=vae_elec0[i, rr])
    qint_elec[j = Goods, i = ElecType, rr = Regions], (start=qint_elec0[j, i, rr])
    ene_elec[i = ElecType, rr = Regions], (start=ene_elec0[i, rr])
    int_elec[i = ElecType, rr = Regions], (start=int_elec0[i, rr])
    gen_elec[i = ElecType, rr = Regions], (start=gen_elec0[i, rr])

    totgen_elec[rr = Regions], (start=totgen_elec0[rr])
    ptotgen_elec[rr = Regions], (start=ptotgen_elec0[rr])

    lambdak_elec[i = ElecType, rr = Regions], (start=1)
    lambdal_elec[i = ElecType, rr = Regions], (start=1)
end