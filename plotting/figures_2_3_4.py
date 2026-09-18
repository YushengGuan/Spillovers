from pathlib import Path
import os,sys,json,struct,shutil
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent
os.environ['MPLCONFIGDIR']=str(ROOT/'mpl_config')

import numpy as np,pandas as pd,matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath
from matplotlib.collections import PatchCollection
from matplotlib.colors import TwoSlopeNorm
OUT=REPO
T=REPO/'cge/output/tables'
F=OUT/'Figures';D=T
for p in [F,D]:p.mkdir(parents=True,exist_ok=True)
mpl.rcParams.update({'font.family':['Arial','DejaVu Sans'],'font.size':7,'axes.labelsize':7,'axes.titlesize':8,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'legend.fontsize':6.5,'legend.frameon':False,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'svg.fonttype':'none','pdf.fonttype':42})
SC=['S0_BASELINE','S1_NO_CN','S2_CAPACITY'];C=['#228B22','#FF4500','#4682B4'];LAB=['S0 Reference','S1 Without China-related reductions','S2 Carbon-price compensation'];Y=[2025,2030,2035,2040,2045,2050]
g=pd.read_csv(T/'group_equilibria_all_nodes.csv').query('group=="GLOBAL"');r=pd.read_csv(T/'regional_equilibria_all_nodes.csv');reg=r.region.drop_duplicates().tolist()
short={'Australia_Oceania':'Oceania','Central, Western and South Asia':'Central/West/South Asia','EU, UK and EFTA':'EU/UK/EFTA','Sub Saharan':'Sub-Saharan Africa'}
base=g[g.scenario.eq(SC[0])].set_index('year')
rb=r[r.scenario.eq(SC[0])][['region','year','real_GDP','real_household_consumption','CO2_Mt']]
rr=r[r.scenario.ne(SC[0])].merge(rb,on=['region','year'],suffixes=('','_S0'),validate='many_to_one')
rr['GDP_pct']=100*(rr.real_GDP/rr.real_GDP_S0-1);rr['CO2_pct']=100*(rr.CO2_Mt/rr.CO2_Mt_S0-1);rr['EV_pct_C0']=100*rr.EV/rr.real_household_consumption_S0
panels=[]
def letter(ax,code,title):
    ax.text(-.03,1.035,code,transform=ax.transAxes,ha='left',va='bottom',fontsize=8,fontweight='bold',clip_on=False)
def finish(fig,name,codes):
    fig.savefig(F/(name+'.pdf'),format='pdf')
    fig.savefig(F/(name+'.svg'),format='svg')
    fig.savefig(F/(name+'.png'),dpi=300);fig.savefig(F/(name+'.tiff'),dpi=600,pil_kwargs={'compression':'tiff_lzw'})
    for code in codes:panels.append({'figure':name,'panel':code,'status':'pending visual QA'})
    plt.close(fig)
def trajectories(ax,field,gap=False):
    for j,sc in enumerate(SC):
        if gap and j==0:continue
        z=g[g.scenario.eq(sc)].set_index('year').loc[Y];v=z[field]-(base.loc[Y,field] if gap else 0)
        ax.plot(Y,v,color=C[j],marker=['o','s','^'][j],ms=3,lw=1.3,label=LAB[j])
    ax.set_xticks(Y,[str(y) for y in Y]);ax.grid(axis='y',alpha=.15)
    if gap:ax.axhline(0,color='black',lw=.6)
def regional(ax,field,year,show_names=True):
    y=np.arange(len(reg))
    for j,sc in enumerate(SC[1:]):
        v=rr.query('scenario==@sc and year==@year').set_index('region').loc[reg,field]
        ax.barh(y+(j-.5)*.33,v,height=.31,color=C[j+1],edgecolor='black',lw=.25,label=LAB[j+1])
    ax.set_yticks(y,[short.get(n,n) for n in reg] if show_names else ['']*len(reg));ax.invert_yaxis();ax.axvline(0,color='black',lw=.6);ax.grid(axis='x',alpha=.15)

pw=pd.read_csv(T/'power_equilibria_all_nodes.csv').groupby(['scenario','year','technology'],as_index=False).generation_TWh.sum()
pb=pw.query('scenario=="S0_BASELINE"').rename(columns={'generation_TWh':'baseline_TWh'}).drop(columns='scenario')
pg=pw.merge(pb,on=['year','technology']);pg['difference_TWh']=pg.generation_TWh-pg.baseline_TWh;pg['difference_pct']=100*pg.difference_TWh/pg.baseline_TWh
e=pd.read_csv(T/'final_energy_mix.csv').query('group=="GLOBAL"').copy();e['carrier']=e.fuel.replace({'Oil':'Oil fuels','Oil_pct':'Oil fuels'})
e=e.groupby(['scenario','year','carrier'],as_index=False).modeled_final_demand_Mtoe.sum()
tot=e.groupby(['scenario','year'],as_index=False).modeled_final_demand_Mtoe.sum();tot['carrier']='Total';e=pd.concat([e,tot])
eb=e.query('scenario=="S0_BASELINE"').drop(columns='scenario').rename(columns={'modeled_final_demand_Mtoe':'baseline_Mtoe'})
eg=e.merge(eb,on=['year','carrier']);eg['difference_pct']=100*(eg.modeled_final_demand_Mtoe/eg.baseline_Mtoe-1)
def grouped(ax,df,field,categories,key):
    x=np.arange(len(categories));handles=[]
    for j,(year,sc) in enumerate([(2030,SC[1]),(2030,SC[2]),(2050,SC[1]),(2050,SC[2])]):
        z=df.query('year==@year and scenario==@sc').set_index(key).loc[categories,field]
        h=ax.bar(x+(j-1.5)*.19,z,width=.18,color=C[SC.index(sc)],edgecolor='black',lw=.3,hatch='///' if year==2050 else None,label=f'{sc[:2]}, {year}');handles.append(h)
    ax.axhline(0,color='black',lw=.6);ax.grid(axis='y',alpha=.15);return handles

fig,axs=plt.subplots(2,2,figsize=(7.2,5.9),layout='constrained')
trajectories(axs[0,0],'renewable_capacity_GW');letter(axs[0,0],'a','Renewable deployment');axs[0,0].set_ylabel('Capacity equivalent (GW)');axs[0,0].scatter([2030],[11000],facecolors='none',edgecolors='black',s=45,zorder=5);axs[0,0].legend(loc='lower right',fontsize=6.5)
search=pd.read_csv(T/'capacity_price_search.csv').sort_values('additional_price_2024USD_t');pol=pd.read_csv(T/'capacity_policy_selected.csv').iloc[0]
ax=axs[0,1]
price=float(pol.additional_price_2024USD_t)
ax.plot(search.additional_price_2024USD_t,search.capacity_GW,'o-',color=C[2],lw=1.1,ms=3,label='S2 capacity response')
ax.axhline(11000,color='black',ls='--',lw=.7,label='2030 target: 11,000 GW')
ax.axvline(price,color='black',ls='--',lw=.8)
ax.scatter([price],[pol.capacity_GW],color=C[1],marker='*',s=50,zorder=5,label='Selected carbon price')
ax.text(.70,.36,f'{price:.2f} USD/tCO₂',transform=ax.transAxes,fontsize=6.5,color='black',ha='right',va='center')
letter(ax,'b','')
ax.set_xlabel('Additional carbon price (2024 USD/tCO₂)')
ax.set_ylabel('2030 capacity equivalent (GW)')
ax.legend(loc='upper left',bbox_to_anchor=(.015,.92),fontsize=6.5)

tech=['Solar','Wind','Hydro','Biomass','Nuclear','Coal_Power','Gas_Power','Oil_Power'];grouped(axs[1,0],pg,'difference_TWh',tech,'technology');axs[1,0].set_xticks(range(8),['PV','Wind','Hydro','Biomass','Nuclear','Coal','Gas','Oil'],rotation=45,ha='right',rotation_mode='anchor');letter(axs[1,0],'c','Electricity substitution');axs[1,0].set_ylabel('Generation difference (TWh/year)');axs[1,0].legend(loc='lower left',ncol=2,fontsize=6.5)
cat=['Coal','Gas','Oil fuels','Electricity','Total'];grouped(axs[1,1],eg,'difference_pct',cat,'carrier');axs[1,1].set_xticks(range(5),['Coal','Gas','Oil fuels','Electricity','Total'],rotation=35,ha='right',rotation_mode='anchor');letter(axs[1,1],'d','Final-energy demand');axs[1,1].set_ylabel('Difference from S0 (%)')
axs[1,1].legend(loc='lower right',ncol=2,fontsize=6.5)
finish(fig,'Figure2_transition',['a','b','c','d'])

pg.to_csv(D/'global_generation_comparison.csv',index=False)
eg.to_csv(D/'global_final_energy_comparison.csv',index=False)
rr.to_csv(D/'regional_contrasts.csv',index=False)

def load_map():
    geo=OUT/'data/geography';geo.mkdir(exist_ok=True)
    membership=pd.read_csv(geo/'map_name.csv');assert membership.SOC.is_unique
    raw=(geo/'worldmap.dbf').read_bytes();n,head,size=struct.unpack_from('<IHH',raw,4)
    fields=[]
    for i in range(32,head-1,32):
        f=raw[i:i+32];fields.append((f[:11].split(b'\0')[0].decode(),f[16]))
    attrs=[]
    for i in range(n):
        row=raw[head+i*size:head+(i+1)*size];offset=1;record={}
        assert row[0]!=42
        for name,length in fields:
            record[name]=row[offset:offset+length].decode('utf-8',errors='replace').replace('\x00','').strip();offset+=length
        attrs.append(record)
    raw=(geo/'worldmap.shp').read_bytes();assert struct.unpack_from('>i',raw,0)[0]==9994 and struct.unpack_from('<i',raw,32)[0]==5
    offset=100;shapes=[]
    while offset<len(raw):
        number,words=struct.unpack_from('>ii',raw,offset);row=raw[offset+8:offset+8+words*2];offset+=8+words*2
        assert struct.unpack_from('<i',row,0)[0]==5
        parts,points=struct.unpack_from('<ii',row,36)
        starts=np.frombuffer(row,dtype='<i4',count=parts,offset=44)
        xy=np.frombuffer(row,dtype='<f8',count=points*2,offset=44+parts*4).reshape(-1,2)
        codes=np.full(points,MPath.LINETO,dtype=np.uint8);codes[starts]=MPath.MOVETO;codes[np.r_[starts[1:]-1,points-1]]=MPath.CLOSEPOLY
        shapes.append(MPath(xy.copy(),codes))
    frame=pd.DataFrame(attrs).merge(membership[['SOC','RegAgg']],on='SOC',how='left',validate='many_to_one')
    frame.loc[frame.SOC.eq('ATA'),'RegAgg']=np.nan
    assert len(shapes)==len(frame)==243
    assert set(reg)<=set(frame.RegAgg)
    return shapes,frame

shapes,world=load_map();map_records=[]
def map_panel(fig,ax,field,scenario,code,title,limits,ticks,label,cmap_name="RdYlBu"):
    values=rr.query('scenario==@scenario and year==2050').set_index('region')[field]
    assert len(values)==18 and values.index.is_unique and np.isfinite(values).all()
    assert limits[0]<=values.min() and limits[1]>=values.max()
    norm=TwoSlopeNorm(vmin=limits[0],vcenter=0,vmax=limits[1]);cmap=mpl.colormaps[cmap_name]
    v=world.RegAgg.map(values)
    colors=[cmap(norm(x)) if pd.notna(x) else '#DDDDDD' for x in v]
    collection=PatchCollection([PathPatch(s) for s in shapes],facecolor=colors,edgecolor='white',linewidth=.08)
    ax.add_collection(collection);ax.set_xlim(-180,180);ax.set_ylim(-90,90);ax.set_aspect('equal');ax.set_axis_off();letter(ax,code,title)
    mappable=mpl.cm.ScalarMappable(norm=norm,cmap=cmap)
    cb=fig.colorbar(mappable,ax=ax,orientation='horizontal',fraction=.07,pad=.03,shrink=.88,ticks=ticks)
    cb.outline.set_linewidth(.45);cb.ax.tick_params(labelsize=6.5,length=2);cb.set_label(label,fontsize=6.5)
    for region,value in values.items():map_records.append({'panel':code,'year':2050,'scenario':scenario,'region':region,'metric':field,'value_pct':value,'color_min':limits[0],'color_center':0,'color_max':limits[1]})



def map_limits(field,scenario=None):
    z=rr[rr.year.eq(2050)]
    if scenario is not None:z=z[z.scenario.eq(scenario)]
    vals=z[field]
    lo=min(float(vals.min()),-.01);hi=max(float(vals.max()),.01)
    def outward(v):
        step=10**np.floor(np.log10(abs(v)))/5
        return np.sign(v)*np.ceil(abs(v)/step)*step
    lo=outward(lo*1.03);hi=outward(hi*1.03)
    if vals.max()<=0:hi=outward(abs(lo)*.05)
    return (lo,hi),[lo,lo/2,0,hi/2,hi]

# Regional emissions layers sum exactly to each scenario's global total.
emissions=r[r.year.isin(Y)][['year','scenario','region','CO2_Mt']].copy()
assert len(emissions)==6*3*18 and not emissions.duplicated(['year','scenario','region']).any()
assert (emissions.CO2_Mt>=0).all()
emissions['CO2_Gt']=emissions.CO2_Mt/1000
totals=emissions.groupby(['year','scenario'],as_index=False).CO2_Mt.sum()
totals=totals.merge(g[['year','scenario','CO2_Mt']],on=['year','scenario'],suffixes=('_stack','_global'),validate='one_to_one')
assert len(totals)==18 and np.allclose(totals.CO2_Mt_stack,totals.CO2_Mt_global,rtol=1e-12,atol=1e-8)
fig=plt.figure(figsize=(7.2,6.4),layout='constrained')
gs=fig.add_gridspec(3,2,height_ratios=[1.65,.38,1.15]);a=fig.add_subplot(gs[0,:]);legend_ax=fig.add_subplot(gs[1,:]);legend_ax.axis('off')
x=np.arange(len(Y))*1.35;width=.32;region_colors=['#436289', '#80D0E4', '#EEC994', '#B9D2C8', '#61847D', '#AAD498', '#DD9F95', '#F5EFBA', '#7C83AA', '#A5A3C3', '#B8B283', '#E3AE98', '#EBA48F', '#D9B1B7', '#7C8491', '#AFDEF3', '#8ACCC9', '#D2D2A5'];ticks=[]
for j,scenario in enumerate(SC):
    bottom=np.zeros(len(Y));xx=x+(j-1)*width
    for k,region in enumerate(reg):
        v=emissions.query('scenario==@scenario and region==@region').set_index('year').loc[Y,'CO2_Gt'].to_numpy()
        a.bar(xx,v,bottom=bottom,width=width*.92,color=region_colors[k],edgecolor='white',linewidth=.12)
        bottom+=v
    ticks.extend(zip(xx,[scenario[:2]]*len(Y)))
    assert np.allclose(bottom,g.query('scenario==@scenario').set_index('year').loc[Y,'CO2_Mt']/1000)
ticks=sorted(ticks);a.set_xticks([t[0] for t in ticks],[t[1] for t in ticks]);a.tick_params(axis='x',length=0,labelsize=6.5)
for xx,year in zip(x,Y):a.text(xx,-.105,str(year),ha='center',va='top',transform=a.get_xaxis_transform(),fontsize=7)
a.set_xlim(x[0]-.65,x[-1]+.65);a.set_ylim(0,5*np.ceil(emissions.groupby(['year','scenario']).CO2_Gt.sum().max()/5));a.set_ylabel('Annual CO₂ emissions (Gt)');letter(a,'a','Regional composition of global emissions')
a.grid(axis='y',alpha=.12);a.set_axisbelow(True)
handles=[Patch(facecolor=region_colors[k],label=short.get(region,region)) for k,region in enumerate(reg)]
legend_ax.legend(handles=handles,loc='center',ncol=6,fontsize=6.5,handlelength=1.0,columnspacing=1.0,labelspacing=.35)
limits,mapticks=map_limits('CO2_pct')
map_panel(fig,fig.add_subplot(gs[2,0]),'CO2_pct',SC[1],'b','S1: CO₂ emissions, 2050',limits,mapticks,'Difference from S0 (%)',cmap_name='RdYlBu_r')
map_panel(fig,fig.add_subplot(gs[2,1]),'CO2_pct',SC[2],'c','S2: CO₂ emissions, 2050',limits,mapticks,'Difference from S0 (%)',cmap_name='RdYlBu_r')
finish(fig,'Figure3_emissions',['a','b','c'])
pd.DataFrame(map_records).to_csv(D/'emissions_map_values.csv',index=False)
emissions.to_csv(D/'regional_emissions_stacks.csv',index=False)
map_records=[]

fig,axs=plt.subplots(2,2,figsize=(7.2,4.7),layout='constrained')
map_panel(fig,axs[0,0],'GDP_pct',SC[1],'a','',*map_limits('GDP_pct',SC[1]),'Difference from S0 GDP (%)')
map_panel(fig,axs[0,1],'GDP_pct',SC[2],'b','',*map_limits('GDP_pct',SC[2]),'Difference from S0 GDP (%)')
map_panel(fig,axs[1,0],'EV_pct_C0',SC[1],'c','',*map_limits('EV_pct_C0',SC[1]),'EV / S0 household consumption (%)')
map_panel(fig,axs[1,1],'EV_pct_C0',SC[2],'d','',*map_limits('EV_pct_C0',SC[2]),'EV / S0 household consumption (%)')
finish(fig,'Figure4_equity',list('abcd'))


pd.DataFrame(map_records).to_csv(D/'equity_map_values.csv',index=False)
print('Updated manuscript Figures 2, 3 and 4: PDF, SVG, PNG and TIFF.')
