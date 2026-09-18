"""Shapley historical attribution; deterministic point estimates, no joint intervals."""
from pathlib import Path
import os, sys, json, hashlib
OUT = Path(__file__).resolve().parents[1]
ROOT = OUT

os.environ['MPLCONFIGDIR']=str(OUT/'QA/matplotlib_cache')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

SRC=OUT/'costs/Source_Data'
raw=pd.read_csv(SRC/'results.csv')
d=raw.loc[raw.method.eq('Shapley')].copy()
EFFECTS=['P_direct','S_share','T_cn_tariff','K_spillover','G_other']
NAMES={'AUS':'Australia','BRA':'Brazil','CAN':'Canada','DEU':'Germany','ESP':'Spain','FRA':'France','GBR':'UK','IND':'India','ITA':'Italy','JPN':'Japan','KOR':'South Korea','POL':'Poland','SWE':'Sweden','TUR':'Türkiye','USA':'USA'}
CAP_NAMES=dict(NAMES,KOR='Korea Rep')
cap=pd.read_csv(SRC/'capacity_weights_all_countries.csv').set_index(['technology','country'])
coverage=pd.read_csv(SRC/'coverage.csv').set_index('technology')
d['net_additions_2024_mw']=[cap.loc[(r.technology,CAP_NAMES[r.iso3]),'net_additions_2024_mw'] for r in d.itertuples()]
d['common_window']=d.start_year.eq(2010)&d.end_year.eq(2024)
d['negative_initial_balance'] = d.technology.eq('wind')&d.iso3.eq('IND')
assert len(raw)==23 and len(d)==23 and d.common_window.sum()==23
assert not d.duplicated(['technology','iso3']).any()
assert (d.total_decline>0).all() and (d.net_additions_2024_mw>0).all()
assert np.allclose(d[EFFECTS].sum(axis=1),d.cn_related_net)
assert np.allclose(d.cn_related_net+d.remainder,d.total_decline)
assert (d.loc[d.technology.eq('wind'),'G_other']==0).all()
for col in ['P','S','T','K','G','net']:
 key={'P':'P_direct','S':'S_share','T':'T_cn_tariff','K':'K_spillover','G':'G_other','net':'cn_related_net'}[col]
 assert np.allclose(d[col+'_pct'],100*d[key]/d.total_decline)
d.to_csv(SRC/'plot_country_data.csv',index=False)
rows=[]
for tech in ['pv','wind']:
 for sample in (['main','without_India'] if tech=='wind' else ['main']):
  a=d.loc[d.technology.eq(tech)&d.common_window].copy()
  if sample=='without_India': a=a.loc[a.iso3.ne('IND')]
  w=a.net_additions_2024_mw/a.net_additions_2024_mw.sum()
  r=dict(technology=tech,sample=sample,n=len(a),coverage_pct=100*a.net_additions_2024_mw.sum()/coverage.loc[tech,'rest_world_additions_2024_mw'])
  for k in ['total_decline',*EFFECTS,'cn_related_net','remainder']:
   r[k]=float(np.dot(a[k],w))
   r[k+'_pct']=100*r[k]/r['total_decline']
  assert abs(r['cn_related_net']+r['remainder']-r['total_decline'])<1e-7
  rows.append(r)
agg=pd.DataFrame(rows)
agg.to_csv(SRC/'weighted_shapley_summary.csv',index=False)
(SRC/'manuscript_statistics.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')

plt.rcParams.update({'font.family':'Arial','font.size':8,'axes.titlesize':9,'axes.labelsize':8,
 'xtick.labelsize':7,'ytick.labelsize':8,'legend.fontsize':7,'axes.linewidth':.6,
 'pdf.fonttype':42,'svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white'})
COLORS=['#B54848','#D1A04A','#45988C','#3D7CA5','#927BAC']
REST='#E3E5E7'
def summary(tech): return agg.loc[agg.technology.eq(tech)&agg['sample'].eq('main')].iloc[0]
def country(tech):
 x=d.loc[d.technology.eq(tech)].copy()
 x['name']=x.iso3.map(NAMES)
 return x.sort_values('name')
def label(tech,iso):
 return NAMES[iso]
def decorate(ax):
 ax.spines[['top','right','left']].set_visible(False)
 ax.tick_params(axis='y',length=0,pad=4)
 ax.tick_params(axis='x',length=3)
 ax.set_axisbelow(True)
 ax.grid(axis='x',color='#EDEEEF',linewidth=.5)
def letter(ax,l): ax.text(-.23,1.10,l,transform=ax.transAxes,fontsize=10,fontweight='bold',va='top')
exports=[]
def save(fig,stem):
 fig.canvas.draw()
 # Ensure every visible text object remains inside the figure canvas.
 renderer=fig.canvas.get_renderer()
 for t in fig.findobj(matplotlib.text.Text):
  if t.get_visible() and t.get_text():
   b=t.get_window_extent(renderer)
   assert b.x0>=-1 and b.y0>=-1 and b.x1<=fig.bbox.width+1 and b.y1<=fig.bbox.height+1,(stem,t.get_text(),b)
 fig.savefig(OUT/'Figures'/f'{stem}.pdf',facecolor='white')
 fig.savefig(OUT/'Figures'/f'{stem}.svg',facecolor='white')
 fig.savefig(OUT/'Figures'/f'{stem}.png',facecolor='white',dpi=300)
 fig.savefig(OUT/'Figures'/f'{stem}.tiff',facecolor='white',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
 for ext in ['pdf','svg','png','tiff']:
  f=OUT/'Figures'/f'{stem}.{ext}'
  exports.append(dict(file=f.name,width_mm=fig.get_figwidth()*25.4,height_mm=fig.get_figheight()*25.4,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 plt.close(fig)

annual=pd.read_csv(SRC/'annual_plot_costs.csv')
fig=plt.figure(figsize=(183/25.4,215/25.4))
gs=fig.add_gridspec(2,2,left=.15,right=.975,top=.925,bottom=.15,
                   height_ratios=[1.5,2.65],hspace=.48,wspace=.60)
label_audit=[];aggregate_labels=[]
for c,tech in enumerate(['pv','wind']):
 ax=fig.add_subplot(gs[0,c]);letter(ax,'ab'[c])
 ax.set_title('Solar photovoltaics' if tech=='pv' else 'Onshore wind',loc='left',pad=15,fontweight='bold')
 ts=annual.loc[annual.technology.eq(tech)].sort_values('year')
 assert len(ts)==15 and np.all(np.diff(ts.year)>0)
 ax.plot(ts.year,ts.model_factual,color='#397DA8',linewidth=1.3,zorder=3)
 ax.plot(ts.year,ts.model_without_china_contribution,color='#B54848',linewidth=1.3,linestyle='--',zorder=2)
 assert ts.observed_completed.notna().all()
 ax.scatter(ts.year,ts.observed_completed,s=13,color='#292929',edgecolor='white',linewidth=.35,zorder=4)
 ax.spines[['right','top']].set_visible(False)
 ax.set_xlim(2009.7,2024.4);ax.set_xticks([2010,2015,2020,2024])
 ax.set_xlabel('Year',labelpad=3)
 ax.set_ylabel('Total installed costs\n(2024 US$/kW)',fontsize=7,labelpad=5)
 ax.set_ylim((0,8000) if tech=='pv' else (1000,3500))
 ax.set_yticks([0,2000,4000,6000,8000] if tech=='pv' else [1000,2000,3000])
 ax.tick_params(axis='both',labelsize=7,length=3)
 ax.grid(axis='y',color='#EDEEEF',linewidth=.5);ax.set_axisbelow(True)

 # Mechanism-only inset in unused upper-right region of the trajectory panel.
 parent=ax
 bounds=[.56,.52,.42,.45] if tech=='pv' else [.56,.65,.42,.32]
 ax=parent.inset_axes(bounds);r=summary(tech)
 ax.patch.set_alpha(0)
 keys=[k for k in EFFECTS if tech=='pv' or k!='G_other']
 names=dict(zip(EFFECTS,['P','S','T','K','E']));colors=dict(zip(EFFECTS,COLORS))
 yy=np.arange(len(keys));total=float(r.total_decline)
 for j,key in enumerate(keys):
  value=float(r[key]);pct=100*value/total
  ax.barh(j,value,height=.54,color=colors[key],hatch='////' if key=='T_cn_tariff' else None,edgecolor='#255C55' if key=='T_cn_tariff' else 'none',linewidth=0)
  text_pct=f'{pct:.2f}%' if 0<abs(pct)<1 else f'{pct:.1f}%'
  ax.text(max(value,0)+(45 if tech=='pv' else 9),j,text_pct,va='center',fontsize=6.5)
  aggregate_labels.append(dict(technology=tech,mechanism=key,amount=value,total_decline=total,percentage=pct,label=text_pct,n=int(r['n'])))
 ax.axvline(0,color='#7D8287',linewidth=.5)
 ax.set_yticks(yy,[names[k] for k in keys]);ax.set_ylim(len(keys)-.45,-.65)
 ax.set_xlim((-200,2000) if tech=='pv' else (-12,360))
 ax.set_xticks([0,1000] if tech=='pv' else [0,100,200])
 ax.set_xlabel('Cost reductions\n(2024 US$/kW)',fontsize=6.5,labelpad=1)
 ax.spines[['top','right','left']].set_visible(False)
 ax.tick_params(axis='y',labelsize=6.5,length=0,pad=2)
 ax.tick_params(axis='x',labelsize=6.5,length=2,pad=1)
 assert np.isclose(sum(r[k] for k in keys),r.cn_related_net)

 ax=fig.add_subplot(gs[1,c]);letter(ax,'cd'[c]);x=country(tech)
 rr=[r for _,r in x.iterrows()];y=np.arange(len(x))
 pos=np.zeros(len(rr));neg=np.zeros(len(rr))
 for key,color in [*zip(EFFECTS,COLORS),('remainder',REST)]:
  if tech=='wind' and key=='G_other':continue
  values=np.array([r[key] for r in rr],dtype=float)
  ax.barh(y,values,left=np.where(values>=0,pos,neg),height=.57,color=color,
          hatch='////' if key=='T_cn_tariff' else None,
          edgecolor='#255C55' if key=='T_cn_tariff' else 'none',linewidth=0)
  pos+=np.maximum(values,0);neg+=np.minimum(values,0)
 assert np.allclose(pos+neg,[r['total_decline'] for r in rr])
 ax.scatter([r['cn_related_net'] for r in rr],y,s=16,marker='D',facecolor='#222222',edgecolor='white',linewidth=.4,zorder=5)
 ax.set_xlim(min(neg.min()-pos.max()*.015,-pos.max()*.05),pos.max()*1.25)
 for i,r in enumerate(rr):
  pct=100*r['cn_related_net']/r['total_decline']
  ax.text(pos[i]+pos.max()*.025,y[i],f'{pct:.1f}%',va='center',fontsize=7)
  label_audit.append(dict(technology=tech,iso3=r['iso3'],cost_reduction=r['total_decline'],china_net=r['cn_related_net'],label_pct=pct))
 ax.set_yticks(y,[label(tech,k) for k in x.iso3]);ax.set_ylim(12.7,-.8)
 ax.tick_params(axis='y',labelsize=7)
 ax.axvline(0,color='#7D8287',linewidth=.6)
 ax.set_xticks([0,2000,4000,6000,8000] if tech=='pv' else [0,1000,2000,3000])
 ax.set_xlabel('Cost reductions (2024 US$/kW)',labelpad=8)
 decorate(ax)
line_legend=[Line2D([],[],marker='o',markersize=3.5,color='none',markerfacecolor='#292929',markeredgecolor='#292929',label='Observed'),
 Line2D([],[],color='#397DA8',linewidth=1.3,label='Model'),
 Line2D([],[],color='#B54848',linewidth=1.3,linestyle='--',label='Without China contribution')]
fig.legend(handles=line_legend,loc='center',bbox_to_anchor=(.55,.62),ncol=3,frameon=False,handlelength=2,columnspacing=1.5)
legend=[Patch(facecolor=c,label=l,hatch='////' if i==2 else None,edgecolor='#255C55' if i==2 else 'none') for i,(c,l) in enumerate(zip(COLORS,['P  Direct price','S  Sourcing share','T  Tariff on China imports','K  Deployment spillover','E  Global experience (PV)']))]
legend += [Patch(facecolor=REST,label='Remainder'),Line2D([],[],marker='D',markersize=4,color='none',markerfacecolor='#222222',markeredgecolor='#222222',label='Net China contribution')]
# Matplotlib fills columns first: display P/S/T/K above E/remainder/net.
legend=[legend[i] for i in [0,4,1,5,2,6,3]]
fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.52,.018),ncol=4,frameon=False,handlelength=1.3,columnspacing=1.4,labelspacing=.65)
save(fig,'Figure1_costs')
pd.DataFrame(aggregate_labels).to_csv(SRC/'aggregate_figure_labels.csv',index=False)
pd.DataFrame(label_audit).to_csv(SRC/'figure_labels.csv',index=False)
(OUT/'QA/figure_exports.json').write_text(json.dumps(exports,indent=2),encoding='utf-8')
(OUT/'QA/data_checks.json').write_text(json.dumps(dict(input_rows=len(raw),shapley_rows=len(d),main_rows=int(d.common_window.sum()),all_assertions_pass=True,max_closure_error=float(abs(d.cn_related_net+d.remainder-d.total_decline).max()),label_count=len(label_audit),annual_model_points=30,observation_series_points=30,points_containing_interpolation=int(annual.contains_imputation.sum())),indent=2),encoding='utf-8')
print('Annual panels and historical mechanism panels rendered.')

