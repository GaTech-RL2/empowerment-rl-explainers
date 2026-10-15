"""Fetch the pinned, openly licensed Kokoro v1.0 model for local narration."""
import hashlib, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/'
FILES={
    'kokoro-v1.0.onnx':'beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a',
    'voices-v1.0.bin':'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d',
}

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    folder=ROOT/'.models';folder.mkdir(exist_ok=True)
    for name,sha in FILES.items():
        path=folder/name
        if path.exists() and digest(path)==sha:
            print('Verified',name);continue
        temp=path.with_suffix(path.suffix+'.download')
        print('Downloading',name,flush=True)
        urllib.request.urlretrieve(BASE+name,temp)
        if digest(temp)!=sha:
            temp.unlink();raise RuntimeError('Model checksum mismatch: '+name)
        temp.replace(path)
        print('Verified',name)

if __name__=='__main__':main()
