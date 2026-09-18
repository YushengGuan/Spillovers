#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables
#---     May, 2023

# --  pp (add prodtax)
# --  pprod (production cost)
# --  pint  pvae
# --  pa    pva             pene
# --        pk pl plnd pns  pfene      pa["elec"]
# --                        pa[FossilSec]
@variables m begin
    # initialization of price
    pkl[i = Sectors_Non_Elec, rr = Regions], (start=pkl0[i, rr])
    pkel[i = Sectors_Non_Elec, rr = Regions], (start=pkel0[i, rr])
    pfene[i = Sectors_Non_Elec, rr = Regions], (start=pfene0[i, rr])
    pene[i = Sectors_Non_Elec, rr = Regions], (start=pene0[i, rr])
    pvae[i = Sectors_Non_Elec, rr = Regions], (start=pvae0[i, rr])
    pint[i = Sectors_Non_Elec, rr = Regions], (start=pint0[i, rr])
    pprod[i = Sectors_Non_Elec, rr = Regions], (start=pprod0[i, rr])
    pp[i =  Sectors, rr = Regions], (start=pp0[i, rr])

    # initialization of inputs & outputs
    k[i =  Sectors, rr = Regions], (start=k0[i, rr])
    l[i =  Sectors, rr = Regions], (start=l0[i, rr])
    lnd[i = AgriSec, rr = Regions], (start=lnd0[i, rr])
    ns[i = NatSec, rr = Regions], (start=ns0[i, rr])
    kl[i = Sectors_Non_Elec, rr = Regions], (start=kl0[i, rr])
    kel[i = Sectors_Non_Elec, rr = Regions], (start=kel0[i, rr])
    qint[j = Goods, i = Sectors, rr = Regions], (start=qint0[j, i, rr])
    fene[i = Sectors_Non_Elec, rr = Regions], (start=fene0[i, rr])
    ene[i = Sectors_Non_Elec, rr = Regions], (start=ene0[i, rr])
    vae[i = Sectors_Non_Elec, rr = Regions], (start=vae0[i, rr])
    int[i = Sectors_Non_Elec, rr = Regions], (start=int0[i, rr])
    prod[i = Sectors, rr = Regions], (start=prod0[i, rr])
end