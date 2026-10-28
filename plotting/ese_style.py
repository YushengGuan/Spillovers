"""Journal typography and physical-size export, with no changes to data artists."""
from pathlib import Path
import os
import json
import numpy as np
import matplotlib as mpl
import matplotlib._mathtext as mathtext
from matplotlib.figure import Figure
from matplotlib.artist import Artist
from matplotlib.path import Path as MPath
from matplotlib.transforms import IdentityTransform
from matplotlib.text import Text
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.collections import Collection

ROOT=Path(os.environ['SPILLOVERS_WORK'])
_savefig=Figure.savefig
_installed=False

class VectorHatch(Artist):
    """Explicit vector strokes instead of SVG pattern fills rasterized by Office."""
    def __init__(self, patch, hatch):
        super().__init__()
        self.patch=patch
        self.spacing_pt=24/max(1,hatch.count('/'))
        self.color=patch._hatch_color
        self.set_zorder(100)
    def draw(self,renderer):
        p=self.patch
        bbox=p.get_path().get_extents(p.get_transform())
        x0,y0,x1,y1=bbox.extents
        inset=renderer.points_to_pixels(.25)
        x0+=inset;y0+=inset;x1-=inset;y1-=inset
        if x1<=x0 or y1<=y0:return
        step=renderer.points_to_pixels(self.spacing_pt)
        vertices=[];codes=[]
        for b in np.arange(np.floor((y0-x1)/step)*step,y1-x0+step,step):
            left=max(x0,y0-b);right=min(x1,y1-b)
            if right<=left:continue
            vertices.extend([(left,left+b),(right,right+b)])
            codes.extend([MPath.MOVETO,MPath.LINETO])
        if not vertices:return
        gc=renderer.new_gc()
        gc.set_foreground(self.color)
        gc.set_linewidth(.5)
        gc.set_capstyle('butt')
        from matplotlib.transforms import TransformedPath
        gc.set_clip_path(TransformedPath(p.get_path(),p.get_transform()))
        renderer.draw_path(gc,MPath(vertices,codes),IdentityTransform())
        gc.restore()

def style(fig):
    fig.set_size_inches(183/25.4,fig.get_figheight(),forward=True)
    for t in fig.findobj(Text):
        t.set_fontfamily('Arial')
        if 'CO₂' in t.get_text():
            t.set_text(t.get_text().replace('$',r'\$').replace('CO₂',r'CO$_2$'))
        is_panel=t.get_text() in list('abcd') and t.get_fontweight() in ['bold',700]
        t.set_fontsize(8 if is_panel else min(7,max(6,t.get_fontsize())))
        if 'CO$_2$' in t.get_text(): t.set_fontsize(7)
    for a in fig.findobj():
        a.set_rasterized(False)
        if isinstance(a,(Line2D,Patch)):
            w=a.get_linewidth()
            if w>0: a.set_linewidth(min(1.5,max(.5,w)))
            if isinstance(a,Patch) and a.get_hatch():
                h=VectorHatch(a,a.get_hatch())
                a.set_hatch(None)
                fig.add_artist(h)
        elif isinstance(a,Collection):
            a.set_linewidth([min(1.5,max(.5,float(v))) if v>0 else 0 for v in a.get_linewidths()])
    # Prevent map colorbars from silently becoming raster image blocks.
    mathtext.SHRINK_FACTOR=0.86
    mpl.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'hatch.linewidth':.5,
                        'mathtext.fontset':'custom','mathtext.rm':'Arial',
                        'mathtext.it':'Arial:italic','mathtext.bf':'Arial:bold'})

def savefig(fig, filename, *args, **kwargs):
    style(fig)
    result=_savefig(fig,filename,*args,**kwargs)
    if Path(filename).suffix=='.svg':
        renderer=fig.canvas.get_renderer()
        texts=[]
        for t in fig.findobj(Text):
            if not t.get_visible() or not t.get_text(): continue
            b=t.get_window_extent(renderer)
            texts.append({'text':t.get_text(),'size_pt':t.get_fontsize(), 'font':t.get_fontfamily(),
                          'bbox':list(b.extents), 'within_canvas':bool(b.x0>=-1 and b.y0>=-1 and b.x1<=fig.bbox.width+1 and b.y1<=fig.bbox.height+1)})
        (ROOT/'QA'/f'{Path(filename).stem}_text.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def install():
    global _installed
    if not _installed:
        Figure.savefig=savefig
        _installed=True
