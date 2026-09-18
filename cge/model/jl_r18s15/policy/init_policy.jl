#---     Global-Regional Integrated Dynamic (GRID) model

#---     All rights reserved
#---     Kangxin An, Can Wang
#---     School of Environment, Tsinghua University

#---     Email: akx21@mails.tsinghua.edu.cn

#---     File Information: initialize variables
#---     May, 2023
if cp_flag == "Cap_g"
    @variables m begin
        # -- initialize the policy variables
        pco2_g >= 0, (start = 0)
        pco2[rr = Regions], (start = 0)
        etax[j = FossilSec, i = Sectors_Non_Elec, rr = Regions], (start=0)
        etax_h[j = Goods, rr = Regions], (start=0)
        etax_elec[j = EnergySec, i = ElecType, rr = Regions], (start=0)
        emisrev[rr = Regions], (start=0)
        # cbam[i = Sectors, rr = Regions], (start=0)
        # cbam_burden[i = Sectors, rr = Regions], (start=0)
        # cbam_revenue[r = Regions], (start=0)
        pfens[j = FossilSec, i = Sectors, rr = Regions], (start=0) # price of fens
    end
else
    @variables m begin
        # -- initialize the policy variables
        pco2[rr = Regions] >= 0, (start = pco20[rr])
        etax[j = FossilSec, i = Sectors_Non_Elec, rr = Regions], (start=0)
        etax_h[j = Goods, rr = Regions], (start=0)
        etax_elec[j = EnergySec, i = ElecType, rr = Regions], (start=0)
        emisrev[rr = Regions], (start=0)
        # cbam[i = Sectors, rr = Regions], (start=0)
        # cbam_burden[i = Sectors, rr = Regions], (start=0)
        # cbam_revenue[r = Regions], (start=0)
        # pfens[j = FossilSec, i = Sectors, rr = Regions], (start=0) # price of fens
    end
end

# if ch4_flag == "None"
#     @variables m begin
#         # -- initialize the policy variables for CH4
#         ch4_tax_ff[j = FossilSec, i = Sectors_Non_Elec, rr = Regions], (start = 0)
#         ch4_tax_prod[i = Sectors_Non_Elec, rr = Regions], (start = 0)
#         ch4_tax_h[i = Goods, rr = Regions], (start = 0)
#     end
# elseif ch4_flag == "Cap_g"
#     @variables m begin
#         # -- initialize the policy variables for CH4
#         pch4 >= 0, (start = 0)
#         ch4_tax_ff[j = FossilSec, i = Sectors_Non_Elec, rr = Regions], (start = 0)
#         ch4_tax_prod[i = Sectors_Non_Elec, rr = Regions], (start = 0)
#         ch4_tax_h[i = Goods, rr = Regions], (start = 0)
#     end
# elseif ch4_flag == "Cap_n"
#     @variables m begin
#         # -- initialize the policy variables for CH4
#         pch4[rr = Regions] >= 0, (start = 0)
#         ch4_tax_ff[j = FossilSec, i = Sectors_Non_Elec, rr = Regions], (start = 0)
#         ch4_tax_prod[i = Sectors_Non_Elec, rr = Regions], (start = 0)
#         ch4_tax_h[i = Goods, rr = Regions], (start = 0)
#     end
# end