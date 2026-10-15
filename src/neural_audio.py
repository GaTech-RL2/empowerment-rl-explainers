"""Offline neural narration, complete utterances, measured visual/caption cues.

Kokoro 82M v1.0 (Apache-2.0), af_heart. Never time-stretch a finished voice.
Use --episode diayn while developing; reruns reuse content-addressed audio.
"""
import argparse, copy, hashlib, json, re, subprocess, wave
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
from content import EPISODES, ROOT
from film_script import SCRIPTS
from prepare_audio import timestamp, spoken

VOICE='af_heart'
SPEED=.94
RAW=ROOT/'media/neural'
RAW.mkdir(exist_ok=True)

def make_engine():
    # Prevent ORT's default all-core pool from contending with video rendering.
    engine=Kokoro(str(ROOT/'.models/kokoro-v1.0.onnx'),str(ROOT/'.models/voices-v1.0.bin'))
    options=ort.SessionOptions();options.intra_op_num_threads=4;options.inter_op_num_threads=1
    engine.sess=ort.InferenceSession(str(ROOT/'.models/kokoro-v1.0.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
    return engine

def synth(engine,text):
    digest=hashlib.sha256(f'kokoro-v1|{VOICE}|{SPEED}|{spoken(text)}'.encode()).hexdigest()[:24]
    path=RAW/(digest+'.wav')
    if not path.exists():
        samples,sr=engine.create(spoken(text),voice=VOICE,speed=SPEED,lang='en-us')
        assert sr==24000
        assert len(samples)>24000, text
        sf.write(path,samples,sr,subtype='PCM_16')
    samples,sr=sf.read(path,dtype='int16')
    return samples

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--episode');args=ap.parse_args()
    engine=make_engine()
    old={e['id']:e for e in json.loads((ROOT/'content.json').read_text())}
    for source in EPISODES:
        if args.episode and source['id']!=args.episode:continue
        ep=copy.deepcopy(source);cursor=0.;parts=[];subs=[];cues=[]
        def pause(seconds):
            nonlocal cursor
            parts.append(np.zeros(round(seconds*24000),dtype=np.int16));cursor+=seconds
        for ci,(title,beats) in enumerate(SCRIPTS[ep['id']]):
            ch=ep['chapters'][ci];start=cursor;starts=[];paragraphs=[]
            pause(.7 if ci==0 else .9)
            for bi,beat in enumerate(beats):
                starts.append(cursor);utterances=[s.strip() for s in beat.split('|')]
                assert len(utterances)==2,(ep['id'],ci,bi)
                paragraphs.append(' '.join(utterances))
                for ui,text in enumerate(utterances):
                    samples=synth(engine,text);dur=len(samples)/24000
                    parts.append(samples)
                    subs.append(dict(start=cursor,end=cursor+dur,text=text))
                    cues.append(dict(start=cursor,end=cursor+dur,chapter=ci,beat=bi,part=ui,text=text))
                    cursor+=dur;pause(.42 if ui==0 else .75)
                print(ep['id'],ci+1,bi+1,round(cursor,1),'seconds',flush=True)
            pause(.55)
            ch.update(title=title,start=start,end=cursor,duration=cursor-start,beat_starts=starts,paragraphs=paragraphs,narration='\n\n'.join(paragraphs))
        ep.update(duration=round(cursor,5),subtitles=subs,cues=cues,voice='Kokoro 82M · af_heart · neural synthetic narration',edition=2)
        assembled=RAW/(ep['id']+'-assembled.wav');sf.write(assembled,np.concatenate(parts),24000,subtype='PCM_16')
        # Consistent speech loudness, with no change to speed or pitch.
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(assembled),'-af','loudnorm=I=-18:TP=-2:LRA=9','-ar','24000','-ac','1',str(ROOT/'media'/f'{ep["id"]}.wav')],check=True)
        assembled.unlink()
        (ROOT/'captions'/f'{ep["id"]}.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{timestamp(s["start"])} --> {timestamp(s["end"])}\n{s["text"]}' for s in subs)+'\n')
        (ROOT/'captions'/f'{ep["id"]}.srt').write_text('\n\n'.join(f'{i+1}\n{timestamp(s["start"],True)} --> {timestamp(s["end"],True)}\n{s["text"]}' for i,s in enumerate(subs))+'\n')
        transcript=f'{ep["paper"]}\n{ep["authors"]}\n{ep["url"]}\nVisual edition 2. Original educational examples. Neural synthetic narration.\n\n'
        for ch in ep['chapters']:
            transcript+=f'{timestamp(ch["start"])} — {ch["title"]}\n{ch["narration"]}\nSource / scope: {ch["source"]}\n\n'
        (ROOT/'transcripts'/f'{ep["id"]}.txt').write_text(transcript)
        (ROOT/'media'/f'{ep["id"]}-chapters.ffmeta').write_text(';FFMETADATA1\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(ch["start"]*1000)}\nEND={round(ch["end"]*1000)}\ntitle={ch["title"]}\n' for ch in ep['chapters']))
        old[ep['id']]=ep
        (ROOT/'content.json').write_text(json.dumps(list(old.values()),ensure_ascii=False,indent=2))
        print('FINISHED',ep['id'],round(cursor,2),'seconds',flush=True)
    (ROOT/'content.js').write_text('window.EPISODES = '+json.dumps(list(old.values()),ensure_ascii=False)+';\n')

if __name__=='__main__':main()
