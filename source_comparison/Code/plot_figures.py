from pathlib import Path
import os,sys,json
OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[1]

os.environ['MPLCONFIGDIR']=str(OUT/'QA/matplotlib_cache')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator

d=pd.read_csv(OUT/'Source_Data/country_endpoints.csv')
a=pd.read_csv(OUT/'Source_Data/weighted_annual.csv')
w=pd.read_csv(OUT/'Source_Data/weighted_endpoints.csv')
names={'CHN':'China','USA':'USA','DEU':'Germany','AUS':'Australia','BRA':'Brazil','CAN':'Canada','ESP':'Spain','FRA':'France','GBR':'UK','IND':'India','ITA':'Italy','JPN':'Japan','KOR':'South Korea','POL':'Poland','SWE':'Sweden','TUR':'Türkiye'}
effects=['P','S','T','K','E'];colors=['#B54848','#D1A04A','#45988C','#3D7CA5','#927BAC'];rest='#E3E5E7'
plt.rcParams.update({'font.family':'Arial','font.size':8,'axes.titlesize':9,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':8,'legend.fontsize':7,'axes.linewidth':.6,'pdf.fonttype':42,'svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white'})
audits=[]
def letter(ax,l):ax.text(-.23,1.10,l,transform=ax.transAxes,fontsize=10,fontweight='bold',va='top')
for target in ['USA','DEU']:
 fig=plt.figure(figsize=(7.2047244094,8.4645669291))  # 183 x 215 mm
 fig.text(.55,.979,names[target]+' as source country',ha='center',va='top',fontsize=10,fontweight='bold')
 gs=fig.add_gridspec(2,2,left=.15,right=.975,top=.925,bottom=.15,height_ratios=[1.5,2.65],hspace=.48,wspace=.60)
 for col,tech in enumerate(['pv','wind']):
  ax=fig.add_subplot(gs[0,col]);letter(ax,'ab'[col])
  ax.set_title('Solar photovoltaics' if tech=='pv' else 'Onshore wind',loc='left',pad=15,fontweight='bold')
  ts=a[a.target.eq(target)&a.technology.eq(tech)&a.scope.eq('foreign_sample')].sort_values('year')
  assert len(ts)==15 and ts.observed_completed.notna().all()
  ax.plot(ts.year,ts.model_factual,color='#397DA8',lw=1.3,zorder=3)
  ax.plot(ts.year,ts.model_without_source_contribution,color='#B54848',lw=1.3,ls='--',zorder=2)
  ax.scatter(ts.year,ts.observed_completed,s=13,color='#292929',edgecolor='white',lw=.35,zorder=4)
  ax.spines[['right','top']].set_visible(False);ax.set_xlim(2009.7,2024.4);ax.set_xticks([2010,2015,2020,2024])
  ax.set_xlabel('Year',labelpad=3);ax.set_ylabel('Total installed costs\n(2024 US$/kW)',fontsize=7,labelpad=5)
  ax.set_ylim((0,8000) if tech=='pv' else (0,3500));ax.set_yticks([0,2000,4000,6000,8000] if tech=='pv' else [0,1000,2000,3000])
  ax.tick_params(axis='both',labelsize=7,length=3);ax.grid(axis='y',color='#EDEEEF',lw=.5);ax.set_axisbelow(True)
  inset=ax.inset_axes([.52,.53,.46,.44] if tech=='pv' else [.54,.65,.44,.32]);inset.patch.set_alpha(0)
  r=w[w.target.eq(target)&w.technology.eq(tech)&w.scope.eq('foreign_sample')].iloc[0]
  keys=effects if tech=='pv' else effects[:4]
  vals=[r[k] for k in keys];low=min(min(vals),0);high=max(max(vals),0);span=max(high-low,10.)
  for j,key in enumerate(keys):
   value=float(r[key]);pct=100*value/r.total_decline
   inset.barh(j,value,height=.54,color=colors[effects.index(key)],hatch='////' if key=='T' else None,edgecolor='#255C55' if key=='T' else 'none',lw=0)
   label=f'{pct:.2f}%' if abs(pct)<1 else f'{pct:.1f}%'
   inset.text(max(value,0)+span*.06,j,label,va='center',fontsize=6)
   audits.append(dict(target=target,technology=tech,mechanism=key,value=value,percentage=pct))
  inset.axvline(0,color='#7D8287',lw=.5);inset.set_yticks(range(len(keys)),keys);inset.set_ylim(len(keys)-.45,-.65)
  inset.set_xlim(low-span*.12,high+span*.85);inset.xaxis.set_major_locator(MaxNLocator(nbins=3))
  inset.set_xticks([v for v in inset.get_xticks() if inset.get_xlim()[0]<=v<=inset.get_xlim()[1]])
  inset.set_xlabel('Cost reductions\n(2024 US$/kW)',fontsize=6,labelpad=1)
  inset.spines[['top','right','left']].set_visible(False);inset.tick_params(axis='y',labelsize=6,length=0,pad=2);inset.tick_params(axis='x',labelsize=6,length=2,pad=1)
  ax=fig.add_subplot(gs[1,col]);letter(ax,'cd'[col])
  x=d[d.target.eq(target)&d.technology.eq(tech)].copy();x['name']=x.iso3.map(names);x=x.sort_values('name')
  y=np.arange(len(x));pos=np.zeros(len(x));neg=np.zeros(len(x))
  for key,color in list(zip(effects,colors))+[('remainder',rest)]:
   if tech=='wind' and key=='E':continue
   v=x[key].to_numpy();ax.barh(y,v,left=np.where(v>=0,pos,neg),height=.57,color=color,hatch='////' if key=='T' else None,edgecolor='#255C55' if key=='T' else 'none',lw=0)
   pos+=np.maximum(v,0);neg+=np.minimum(v,0)
  assert np.allclose(pos+neg,x.total_decline)
  ax.scatter(x.net,y,s=16,marker='D',facecolor='#222222',edgecolor='white',lw=.4,zorder=5)
  mx=pos.max();ax.set_xlim(min(neg.min()-mx*.015,-mx*.05),mx*1.26)
  for i,r in enumerate(x.itertuples()):ax.text(pos[i]+mx*.025,y[i],f'{r.net_pct:.1f}%',va='center',fontsize=7)
  ax.set_yticks(y,x['name']);ax.set_ylim(12.7,-.8);ax.tick_params(axis='y',labelsize=7,length=0,pad=4)
  ax.axvline(0,color='#7D8287',lw=.6);ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
  ax.set_xticks([v for v in ax.get_xticks() if ax.get_xlim()[0]<=v<=ax.get_xlim()[1]])
  ax.set_xlabel('Cost reductions (2024 US$/kW)',labelpad=8);ax.spines[['top','right','left']].set_visible(False)
  ax.grid(axis='x',color='#EDEEEF',lw=.5);ax.set_axisbelow(True)
 handles=[Line2D([],[],marker='o',markersize=3.5,color='none',markerfacecolor='#292929',markeredgecolor='#292929',label='Observed'),Line2D([],[],color='#397DA8',lw=1.3,label='Model'),Line2D([],[],color='#B54848',lw=1.3,ls='--',label='Historical contribution restored')]
 fig.legend(handles=handles,loc='center',bbox_to_anchor=(.55,.62),ncol=3,frameon=False,handlelength=2,columnspacing=1.25)
 handles=[Patch(facecolor=c,label=l,hatch='////' if i==2 else None,edgecolor='#255C55' if i==2 else 'none') for i,(c,l) in enumerate(zip(colors,['P  Price','S  Source','T  Tariff','K  Spillover','E  Experience']))]
 handles += [Patch(facecolor=rest,label='Remainder'),Line2D([],[],marker='D',markersize=4,color='none',markerfacecolor='#222222',markeredgecolor='#222222',label='Net '+names[target]+' contribution')]
 fig.legend(handles=[handles[i] for i in [0,4,1,5,2,6,3]],loc='lower center',bbox_to_anchor=(.52,.028),ncol=4,frameon=False,handlelength=1.3,columnspacing=1.1,labelspacing=.65)
 fig.canvas.draw();renderer=fig.canvas.get_renderer()
 for t in fig.findobj(matplotlib.text.Text):
  if t.get_visible() and t.get_text():
   b=t.get_window_extent(renderer)
   assert b.x0>=-1 and b.y0>=-1 and b.x1<=fig.bbox.width+1 and b.y1<=fig.bbox.height+1,(target,t.get_text(),b)
 stem='Fig_S_'+target+'_Historical_Mechanisms'
 fig.savefig(OUT/'Figures'/f'{stem}.pdf',facecolor='white')
 fig.savefig(OUT/'Figures'/f'{stem}.svg',facecolor='white')
 fig.savefig(OUT/'Figures'/f'{stem}.png',facecolor='white',dpi=300)
 fig.savefig(OUT/'Figures'/f'{stem}.tiff',facecolor='white',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
 plt.close(fig)
pd.DataFrame(audits).to_csv(OUT/'Source_Data/figure_inset_labels.csv',index=False)
(OUT/'QA/figure_checks.json').write_text(json.dumps(dict(figure_count=2,panels=8,geometry_pass=True,dimensions_mm=[183,215],source='country_endpoints.csv and weighted_annual.csv',P='historical equipment-price decline',uncertainty='point estimates; joint uncertainty not propagated'),indent=2),encoding='utf-8')
print('Two source-country figures written.')
