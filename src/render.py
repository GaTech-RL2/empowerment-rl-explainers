"""Narrated mathematical films with paragraph-aligned visual derivation steps."""
import argparse,bisect,json,math,subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image
from drawing import *
from scenes import scene
from prepare_math import key
ROOT=Path(__file__).resolve().parents[1]

@lru_cache(256)
def equation(math,color):
    im=Image.open(ROOT/'assets/math'/f'{key(math,color)}.png').convert('RGBA')
    # math_to_image uses a white canvas. Derive alpha from coverage so colored
    # antialiasing remains crisp on the dark film and HTML backgrounds.
    import numpy as np
    a=np.array(im).astype(float)
    target=np.array([int(color[i:i+2],16) for i in (1,3,5)])
    channel=int(np.argmax(255-target));coverage=(255-a[:,:,channel])/max(1,255-target[channel])
    a[:,:,:3]=target;a[:,:,3]=np.clip(coverage,0,1)*255
    im=Image.fromarray(a.astype('uint8'),'RGBA')
    bbox=im.getbbox()
    if bbox:im=im.crop(bbox)
    scale=min(1,1470/im.width,79/im.height)
    if scale<1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    return im

def frame(ep,t,subtitles=False):
    from film_scenes import draw_film
    cues=ep['cues'];i=max(0,bisect.bisect_right([q['start'] for q in cues],t)-1)
    cue=cues[i];elapsed=t-cue['start']
    # Complete a physical demonstration, then give the viewer time to inspect it.
    p=clamp(elapsed/min(6.0,(cue['end']-cue['start'])*.65))
    im=Image.new('RGB',(W,H),BG);c=Canvas(im)
    draw_film(c,ep['id'],cue['chapter'],cue['beat'],cue['part'],p)
    if i and 0<=elapsed<.38:
        previous=cues[i-1];old=Image.new('RGB',(W,H),BG)
        draw_film(Canvas(old),ep['id'],previous['chapter'],previous['beat'],previous['part'],1)
        im=Image.blend(old,im,ease(elapsed/.38));c=Canvas(im)
    c.text(48,35,f'{ep["number"]} / {ep["short"].upper()}',18,ep['color'])
    c.text(1552,35,f'{cue["chapter"]+1} / 6',18,MUTED,anchor='ra')
    # Captions are selectable tracks. The picture has no burnt-in narration.
    c.d.rectangle((0,895,W,H),fill=LINE)
    c.d.rectangle((0,895,W*clamp(t/ep['duration']),H),fill=ep['color'])
    for ch in ep['chapters']:
        x=W*ch['start']/ep['duration'];c.line([(x,895),(x,900)],BG,2)
    if t<.5:im=Image.blend(Image.new('RGB',(W,H),BG),im,ease(t/.5))
    return im

def render(ep,fps=24):
    out=ROOT/'media'/f'{ep["id"]}.mp4';duration=ep['duration']
    args=['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(fps),'-i','-',
          '-i',str(ROOT/'media'/f'{ep["id"]}.wav'),'-i',str(ROOT/'captions'/f'{ep["id"]}.srt'),'-i',str(ROOT/'media'/f'{ep["id"]}-chapters.ffmeta'),
          '-map','0:v','-map','1:a','-map','2:s','-map_metadata','3','-map_chapters','3','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-threads','3',
          '-c:a','aac','-b:a','112k','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata','title='+ep['short']+' — '+ep['title'],
          '-metadata','comment=Original educational animation and synthetic narration. All toy experiments are labeled; paper sources in companion HTML.',
          '-t',str(duration),'-movflags','+faststart',str(out)]
    with (ROOT/'qa'/f'{ep["id"]}-ffmpeg.log').open('w') as log:
        proc=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=log)
        try:
            for i in range(round(duration*fps)):
                proc.stdin.write(frame(ep,i/fps).tobytes())
                if i%(60*fps)==0:print(ep['id'],f'{i/fps:.0f}/{duration}s',flush=True)
        finally:proc.stdin.close()
        if proc.wait():raise RuntimeError(f'Render failed: {ep["id"]}')
    print('COMPLETE',ep['id'],round(out.stat().st_size/1e6,1),'MB',flush=True)

def previews(eps):
    for ep in eps:
        thumbs=[]
        for i,ch in enumerate(ep['chapters']):
            for b in range(3):
                starts=ch['beat_starts'];end=starts[b+1] if b<2 else ch['end']
                im=frame(ep,starts[b]+(end-starts[b])*.8,False)
                if b==1:im.save(ROOT/'previews'/f'{ep["id"]}-{i+1:02}.png')
                thumbs.append(im.resize((400,225)))
            if i==0:frame(ep,ch['start']+ch['duration']*.28,False).save(ROOT/'previews'/f'{ep["id"]}.jpg',quality=92)
        sheet=Image.new('RGB',(1600,225*math.ceil(len(thumbs)/4)),BG)
        for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*400,(i//4)*225))
        sheet.save(ROOT/'qa'/f'{ep["id"]}-storyboard.jpg',quality=90)
    print('Prepared full-resolution chapter previews and derivation storyboards.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--episode');ap.add_argument('--previews',action='store_true');ap.add_argument('--fps',type=int,default=24);a=ap.parse_args()
    eps=json.loads((ROOT/'content.json').read_text())
    if a.episode:eps=[e for e in eps if e['id']==a.episode]
    if a.previews:previews(eps)
    else:
        for e in eps:render(e,a.fps)
