import sys, math, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tl import *
STYLE="A"
ONLY=[]
W, H, FPS = 1080, 1920, 30
GF = "/usr/share/fonts/truetype/google-fonts/"
def F(n, s): return ImageFont.truetype(GF + n, s)
BOLD, MED = "Poppins-Bold.ttf", "Poppins-Medium.ttf"
INK=(25,40,110); RED=(210,45,55); GREEN=(25,150,80); BLACK=(25,25,25); BOARD=(250,250,246)
COL=[(130,205,150),(120,185,240),(250,212,80),(245,145,175),(185,145,240)]
LAB=["Physiological","Safety","Belonging","Esteem","Self-actualisation"]
EXA=["food, water, pay","job security","team spirit","recognition, status","challenge and growth"]
clamp=lambda x:max(0,min(1,x))
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
rnd=random.Random(5)
def jit(pts, amp=1.6, step=14):
    out=[]
    for (x0,y0),(x1,y1) in zip(pts[:-1],pts[1:]):
        L=math.hypot(x1-x0,y1-y0); n=max(1,int(L/step))
        for i in range(n):
            u=i/n; out.append((x0+(x1-x0)*u+rnd.uniform(-amp,amp), y0+(y1-y0)*u+rnd.uniform(-amp,amp)))
    out.append(pts[-1]); return out
def prefix(pts,f):
    if f<=0: return []
    if f>=1: return pts
    ls=[0]
    for a,b in zip(pts[:-1],pts[1:]): ls.append(ls[-1]+math.hypot(b[0]-a[0],b[1]-a[1]))
    target=ls[-1]*f; out=[pts[0]]
    for i in range(1,len(pts)):
        if ls[i]<=target: out.append(pts[i])
        else:
            u=(target-ls[i-1])/(ls[i]-ls[i-1]); a,b=pts[i-1],pts[i]
            out.append((a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u)); break
    return out
def stroke(d,pts,f,color,w=8):
    p=prefix(pts,clamp(f))
    if len(p)>=2: d.line(p,fill=color,width=w,joint="curve")
    for q in (p[:1]+p[-1:]):
        d.ellipse((q[0]-w/2,q[1]-w/2,q[0]+w/2,q[1]+w/2),fill=color)
def write(d,lines,x,y,font,color,t,t0,dur,gap=10,anchor=None):
    tot=sum(len(l) for l in lines); n=int(clamp((t-t0)/dur)*tot)
    for l in lines:
        k=min(len(l),n); n-=k
        if k>0:
            if anchor=="m": d.text((x,y),l[:k],font=font,fill=color,anchor="ma")
            else: d.text((x,y),l[:k],font=font,fill=color)
        y+=font.size+gap
def wrap(d,text,f,mw):
    out,cur=[],""
    for w in text.split():
        tt=(cur+" "+w).strip()
        if d.textlength(tt,font=f)<=mw: cur=tt
        else: out.append(cur); cur=w
    return out+([cur] if cur else [])
def rel(t,i,frac=0,off=.25): return t-(S[i]+off+frac*v[i])

# ---------------- board content ----------------
BLUE=(130,185,240); YEL=(250,212,80)
def face(d,cx,cy,r,mood,col):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=col,outline=INK,width=6)
    for ex in (cx-r*.35,cx+r*.35): d.ellipse((ex-9,cy-r*.3-9,ex+9,cy-r*.3+9),fill=INK)
    if mood==0: d.arc((cx-r*.45,cy+r*.25,cx+r*.45,cy+r*.85),200,340,fill=INK,width=7)
    elif mood==1: d.line((cx-r*.4,cy+r*.45,cx+r*.4,cy+r*.45),fill=INK,width=7)
    else: d.arc((cx-r*.5,cy-r*.05,cx+r*.5,cy+r*.6),20,160,fill=INK,width=7)
