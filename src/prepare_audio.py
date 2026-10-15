"""Local, cached narration. Captions use actual sentence audio boundaries.

Requires macOS `say`, FFmpeg, and ffprobe. No API key or remote service.
"""
import concurrent.futures, hashlib, json, re, subprocess, wave
from pathlib import Path
from content import EPISODES, ROOT
RAW = ROOT/'media'/'narration'
RAW.mkdir(exist_ok=True)
VOICE='Samantha'
RATE=155

def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def spoken(s):
    names={'DIAYN':'Dye in','SEE':'see','ESR':'E S R','LLM':'L L M','KL':'K L','RL':'R L','MDP':'M D P','SFT':'S F T','InfoNCE':'Info N C E'}
    for a,b in names.items(): s=re.sub(r'\b'+a+r'\b',b,s)
    return s

def chunks(para):
    sentences=re.split(r'(?<=[.!?])\s+',para.strip())
    out=[]
    for sentence in sentences:
        # Smaller utterances keep captions readable; all timestamps still come
        # from the audio files, never a guessed words-per-minute conversion.
        words=sentence.split(); line=[]
        for w in words:
            if len(' '.join(line+[w]))>136 and line:
                out.append(' '.join(line));line=[]
            line.append(w)
        if line:out.append(' '.join(line))
    return out

def synth(text):
    digest=hashlib.sha256(f'{VOICE}|{RATE}|{spoken(text)}'.encode()).hexdigest()[:20]
    base=RAW/digest; wav=base.with_suffix('.wav')
    if not wav.exists():
        txt=base.with_suffix('.txt');aiff=base.with_suffix('.aiff')
        txt.write_text(spoken(text))
        run(['say','-v',VOICE,'-r',str(RATE),'-o',str(aiff),'-f',str(txt)])
        run(['ffmpeg','-y','-v','error','-i',str(aiff),'-ar','24000','-ac','1','-c:a','pcm_s16le',str(wav)])
        aiff.unlink();txt.unlink()
    with wave.open(str(wav),'rb') as f: duration=f.getnframes()/f.getframerate()
    return wav,duration

def timestamp(t,comma=False):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02}{"," if comma else "."}{ms:03}'

def silence(out,seconds):out.writeframes(b'\x00\x00'*round(24000*seconds))

def main():
    all_text=list(dict.fromkeys(text for ep in EPISODES for ch in ep['chapters'] for para in ch['paragraphs'] for text in chunks(para)))
    audio={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for i,(text,result) in enumerate(zip(all_text,pool.map(synth,all_text))):
            audio[text]=result
            if i%40==0:print('Narrated',i,'/',len(all_text),'utterances',flush=True)
    for ep in EPISODES:
        raw=RAW/(ep['id']+'-assembled.wav');cursor=0.;subtitles=[]
        with wave.open(str(raw),'wb') as out:
            out.setparams((1,2,24000,0,'NONE','not compressed'))
            for ch in ep['chapters']:
                start=cursor;beats=[]
                silence(out,.4);cursor+=.4
                for para in ch['paragraphs']:
                    beats.append(cursor)
                    for text in chunks(para):
                        path,dur=audio[text]
                        with wave.open(str(path),'rb') as inp:out.writeframes(inp.readframes(inp.getnframes()))
                        subtitles.append(dict(start=cursor,end=cursor+dur,text=text))
                        cursor+=dur;silence(out,.1);cursor+=.1
                    silence(out,.15);cursor+=.15
                silence(out,.5);cursor+=.5
                ch.update(start=start,end=cursor,duration=cursor-start,beat_starts=beats)
        scale=ep['target_duration']/cursor
        assert .72<scale<1.35,(ep['id'],scale)
        run(['ffmpeg','-y','-v','error','-i',str(raw),'-af',f'atempo={1/scale:.10f},apad','-t',str(ep['target_duration']),'-ar','24000','-ac','1',str(ROOT/'media'/f'{ep["id"]}.wav')])
        for ch in ep['chapters']:
            for k in ('start','end','duration'):ch[k]*=scale
            ch['beat_starts']=[t*scale for t in ch['beat_starts']]
        for sub in subtitles:
            sub['start']*=scale;sub['end']*=scale
        ep.update(duration=ep['target_duration'],subtitles=subtitles,voice=f'macOS {VOICE} · synthetic narration')
        (ROOT/'captions'/f'{ep["id"]}.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{timestamp(s["start"])} --> {timestamp(s["end"])}\n{s["text"]}' for s in subtitles)+'\n')
        (ROOT/'captions'/f'{ep["id"]}.srt').write_text('\n\n'.join(f'{i+1}\n{timestamp(s["start"],True)} --> {timestamp(s["end"],True)}\n{s["text"]}' for i,s in enumerate(subtitles))+'\n')
        transcript=f'{ep["paper"]}\n{ep["authors"]}\n{ep["url"]}\nOriginal educational narration. Toy examples are not benchmark replications.\n\n'
        for ch in ep['chapters']:
            transcript+=f'{timestamp(ch["start"])} — {ch["title"]}\n{ch["narration"]}\nSource / scope: {ch["source"]}\n\n'
        (ROOT/'transcripts'/f'{ep["id"]}.txt').write_text(transcript)
        (ROOT/'media'/f'{ep["id"]}-chapters.ffmeta').write_text(';FFMETADATA1\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(ch["start"]*1000)}\nEND={round(ch["end"]*1000)}\ntitle={ch["title"]}\n' for ch in ep['chapters']))
        print('Timeline',ep['id'],ep['duration'],'seconds; time scale',round(scale,3),flush=True)
    (ROOT/'content.json').write_text(json.dumps(EPISODES,ensure_ascii=False,indent=2))
    (ROOT/'content.js').write_text('window.EPISODES = '+json.dumps(EPISODES,ensure_ascii=False)+';\n')

if __name__=='__main__': main()
