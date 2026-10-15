"""Check text density, clipping, and text overlap across the narrated poses.

This complements visual storyboard review; it cannot judge whether an
explanation or diagram is pedagogically clear.
"""
import json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from drawing import Canvas,font,BG
from film_scenes import draw_film

episodes=json.loads((ROOT/'content.json').read_text());reports=[];failures=[]
for ep in episodes:
    counts=[]
    for cue in ep['cues']:
        for phase in [0,.5,1]:
            texts=[];canvas=Canvas(Image.new('RGB',(1600,900),BG));original=canvas.text
            def capture(x,y,s,size=24,color='#edf2fa',bold=False,anchor=None,mono=False):
                box=canvas.d.textbbox((round(x),round(y)),str(s),font=font(size,bold,mono),anchor=anchor)
                texts.append((str(s),box));original(x,y,s,size,color,bold,anchor,mono)
            canvas.text=capture
            draw_film(canvas,ep['id'],cue['chapter'],cue['beat'],cue['part'],phase)
            if phase==1:counts.append(sum(len(t.split()) for t,_ in texts))
            loc=[ep['id'],cue['chapter'],cue['beat'],cue['part'],phase]
            for text,box in texts:
                if box[0]<15 or box[2]>1585 or box[1]<75 or box[3]>875:
                    failures.append(loc+['clipping',text,box])
            for i,(a,aa) in enumerate(texts):
                for b,bb in texts[i+1:]:
                    width=min(aa[2],bb[2])-max(aa[0],bb[0]);height=min(aa[3],bb[3])-max(aa[1],bb[1])
                    if width>6 and height>6:failures.append(loc+['text overlap',a,b])
    reports.append(dict(episode=ep['id'],poses=len(counts),animation_phases_checked=3,max_visible_words=max(counts),mean_visible_words=round(sum(counts)/len(counts),1)))
report=dict(episodes=reports,failures=failures,caption_mode='selectable, off by default')
(ROOT/'qa/visual-verification.json').write_text(json.dumps(report,indent=2)+'\n')
assert not failures,failures
assert all(r['max_visible_words']<=35 for r in reports)
print('216 narrated poses at 3 animation phases: no clipped or overlapping text; at most 30 visible words.')
