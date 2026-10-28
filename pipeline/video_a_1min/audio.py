import numpy as np, wave, subprocess, json
from tl import *
np.random.seed(2); SR=44100; N=int(SR*TOTAL)
mus=np.zeros(N); fx=np.zeros(N)
def put(buf,t,x,g=1.0):
    i=int(t*SR)
    if i>=N or i<0: return
    x=x[:N-i]; buf[i:i+len(x)]+=x*g
def note(f,d,att=.01,dec=6,harm=(1,.3,.1)):
    t=np.arange(int(d*SR))/SR
    return sum(h*np.sin(2*np.pi*f*(k+1)*t) for k,h in enumerate(harm))*np.minimum(1,t/att)*np.exp(-t*dec)
def kick():
    t=np.arange(int(.3*SR))/SR; f=110*np.exp(-t*18)+45; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*12)
def hat():
    n=int(.06*SR); x=np.diff(np.random.randn(n),prepend=0); return x*np.exp(-np.arange(n)/SR*90)
def snare():
    n=int(.2*SR); t=np.arange(n)/SR; return np.random.randn(n)*np.exp(-t*25)*.6+np.sin(2*np.pi*190*t)*np.exp(-t*30)*.4
bpm=92; beat=60/bpm; hz=lambda m:440*2**((m-69)/12)
prog=[(57,[57,60,64,67]),(53,[53,57,60,64]),(48,[48,52,55,59]),(55,[55,59,62,65])]
for b in range(int(TOTAL/(4*beat))+1):
    root,ch=prog[b%4]; t0=b*4*beat
    put(mus,t0,note(hz(root-12),beat*3.8,dec=1.2,harm=(1,.5,.2)),.5)
    for k,m in enumerate(ch):
        for off in (0,2*beat): put(mus,t0+off+k*.012,note(hz(m),beat*1.8,att=.02,dec=2.2),.12)
    for s in range(8): put(mus,t0+s*beat/2,note(hz(ch[[0,2,1,3,2,3,1,2][s]]+12),.35,dec=7),.10)
    for k in (0,2.5): put(mus,t0+k*beat,kick(),.5)
    for k in (1,3): put(mus,t0+k*beat,snare(),.22)
    for s in range(8): put(mus,t0+s*beat/2,hat(),.10 if s%2 else .06)
mus=np.convolve(mus,np.ones(6)/6,'same'); fi=SR; fo=2*SR; mus[:fi]*=np.linspace(0,1,fi); mus[-fo:]*=np.linspace(1,0,fo)
def pop(f0):
    t=np.arange(int(.18*SR))/SR; f=f0*(1+1.2*np.exp(-t*40)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*22)
def whoosh(d=.4):
    n=int(d*SR); x=np.convolve(np.random.randn(n),np.ones(30)/30,'same'); y=x*np.sin(np.pi*np.linspace(0,1,n))**2; return y/abs(y).max()
def ding():
    t=np.arange(int(.9*SR))/SR; return (np.sin(2*np.pi*1318*t)+.4*np.sin(2*np.pi*2636*t))*np.exp(-t*5)
def tick():
    t=np.arange(int(.08*SR))/SR; return np.sin(2*np.pi*900*t)*np.exp(-t*50)
put(fx,.05,whoosh(),.3)
for k,t in enumerate(EV["levels"]): put(fx,t,pop(440+k*80),.7)
put(fx,S[1]+.25,whoosh(.4),.2)
for t in EV["cuts"]: put(fx,t+.02,whoosh(),.3)
for t in EV["ticks"]: put(fx,t,tick(),.6)
put(fx,EV["ding"],ding(),.4); put(fx,S[6]+.2,pop(700),.7)
mus=mus/abs(mus).max()*.55; fx=fx/max(1,abs(fx).max())*.9
def wr(name,x):
    w=wave.open(name,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes()); w.close()
wr("music.wav",mus); wr("fx.wav",fx)
IN=[];F=""
for i in range(7):
    IN+=["-i",f"vo/l{i+1}.wav"]; ms=int((S[i]+.25)*1000); F+=f"[{i}]aresample=44100,adelay={ms}|{ms}[v{i}];"
F+="".join(f"[v{i}]" for i in range(7))+"amix=inputs=7:normalize=0,volume=1.6[voice]"
subprocess.run(["ffmpeg","-y",*IN,"-filter_complex",F,"-map","[voice]","-t",str(TOTAL),"voice_track.wav"],capture_output=True,check=True)
subprocess.run(["ffmpeg","-y","-i","voice_track.wav","-i","music.wav","-i","fx.wav","-filter_complex","[0]asplit=2[v1][v2];[1]volume=0.55[m];[m][v2]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md];[2]volume=0.5[f];[v1][md][f]amix=inputs=3:normalize=0,alimiter=limit=0.95[a]","-map","[a]","-t",str(TOTAL),"final_raw.wav"],capture_output=True,check=True)
print("ok")
