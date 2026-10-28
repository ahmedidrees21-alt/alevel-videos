import sys
from common import *
import numpy as np
VW,VH=1000,1250          # virtual board size
SC=0.84                  # scale -> 840 x 1050
BX,BY=70,190             # board placed inside TikTok safe zone
SAFE=(60,180,920,1380)   # x0,y0,x1,y1 : nothing may be drawn outside
CAPY=1262
BLUEC=(130,185,240); YEL=(250,212,80)
def board(d,t):
    X=lambda x:x*VW; Y=lambda y:y*VH
    seg=max(i for i in range(7) if t>=S[i])
    if seg==0:
        write(d,["TAYLOR"],X(.5),Y(.05),F(BOLD,170),INK,t,.05,.45,anchor="m")
        write(d,["vs"],X(.5),Y(.25),F(BOLD,90),(120,120,120),t,.45,.25,anchor="m")
        write(d,["MAYO"],X(.5),Y(.33),F(BOLD,170),RED,t,.65,.45,anchor="m")
        write(d,["isn't as hard"],X(.5),Y(.57),F(BOLD,88),INK,t,1.2,.6,anchor="m")
        write(d,["as they make it seem"],X(.5),Y(.67),F(BOLD,64),INK,t,1.8,.8,anchor="m")
        stroke(d,jit([(X(.1),Y(.67)+84),(X(.9),Y(.67)+84)]),(t-2.5)/.5,RED,8)
        write(d,["Motivation theories in ONE minute"],X(.5),Y(.82),F(BOLD,44),GREEN,t,2.9,.9,anchor="m")
    elif seg<=3:
        write(d,["TAYLOR vs MAYO"],X(.5),Y(.01),F(BOLD,62),INK,t,S[1]+.1,.9,anchor="m")
        stroke(d,jit([(X(.1),Y(.01)+84),(X(.9),Y(.01)+84)]),(t-S[1]-1.1)/.5,RED,7)
        cols=((.02,.49,BLUEC,"TAYLOR","Scientific management",S[1]+.9),(.51,.98,YEL,"MAYO","Human relations",S[2]+.3))
        for (x0,x1,c,lab,sub,tt) in cols:
            if t>tt:
                a=clamp((t-tt)/.4)
                d.rectangle((X(x0),Y(.12),X(x1),Y(.12)+110),fill=lerp(BOARD,c,a),outline=INK,width=6)
                write(d,[lab],X((x0+x1)/2),Y(.12)+26,F(BOLD,52),INK,t,tt,.5,anchor="m")
                write(d,[sub],X((x0+x1)/2),Y(.12)+128,F(MED,32),(70,70,70),t,tt+.3,.7,anchor="m")
        stroke(d,jit([(X(.5),Y(.12)),(X(.5),Y(.60))]),(t-(S[1]+1.0))/1.0,(150,150,150),5)
        tay=["Pay for output","Watch closely","Simple jobs"]; may=["Teamwork","Attention","Being listened to"]
        for k in range(3):
            ta=EV["levels"][k]
            if t>=ta:
                d.ellipse((X(.04),Y(.285)+k*110+16,X(.04)+16,Y(.285)+k*110+32),fill=INK)
                write(d,[tay[k]],X(.075),Y(.285)+k*110,F(BOLD,46),BLACK,t,ta,.5)
            tb=EV["levels"][3+k]
            if t>=tb:
                d.ellipse((X(.54),Y(.285)+k*110+16,X(.54)+16,Y(.285)+k*110+32),fill=INK)
                write(d,[may[k]],X(.575),Y(.285)+k*110,F(BOLD,46),BLACK,t,tb,.5)
        # icons
        if t>S[1]+.25+.15*v[1]:
            cx,cy=X(.26),Y(.60)
            d.ellipse((cx-62,cy-62,cx+62,cy+62),fill=(250,205,60),outline=INK,width=6)
            d.text((cx,cy),"£",font=F(BOLD,76),fill=INK,anchor="mm")
        if t>S[2]+.25+.30*v[2]:
            face(d,X(.68),Y(.60),52,2,(190,235,190)); face(d,X(.84),Y(.60),52,2,(250,215,190))
        if seg==3:
            f3=S[3]+.25
            bx=(X(.03),Y(.72),X(.97),Y(.72)+270)
            d.rectangle(bx,fill=(255,243,170),outline=INK,width=6)
            write(d,["TAYLOR = PAY + CONTROL"],X(.5),Y(.72)+34,F(BOLD,46),INK,t,f3+.38*v[3],1.0,anchor="m")
            write(d,["MAYO = PEOPLE + TEAMWORK"],X(.5),Y(.72)+150,F(BOLD,46),RED,t,f3+.66*v[3],1.1,anchor="m")
    elif seg==4:
        f0=S[4]+.25
        write(d,["YOUR TURN"],X(.5),Y(.02),F(BOLD,74),RED,t,f0,.6,anchor="m")
        stroke(d,jit([(X(.3),Y(.02)+100),(X(.7),Y(.02)+100)]),(t-f0-.7)/.5,RED,7)
        q="Northway's warehouse pays staff per item packed, but staff say nobody listens to them, and many are leaving. Whose theory fits best?"
        f=F(MED,50); lines=wrap(d,q,f,VW*.88)
        write(d,lines,X(.06),Y(.15),f,BLACK,t,f0+.7,5.2,gap=14)
        tc=f0+6.2
        for k,(lab,xx,c) in enumerate((("A  Taylor",.05,BLUEC),("B  Mayo",.53,YEL))):
            if t>tc+k*.3:
                d.rounded_rectangle((X(xx),Y(.50),X(xx+.42),Y(.50)+110),radius=20,fill=c,outline=INK,width=6)
                d.text((X(xx+.21),Y(.50)+55),lab,font=F(BOLD,48),fill=INK,anchor="mm")
        for k,tk in enumerate(EV["ticks"]):
            if tk<=t<tk+1: d.text((X(.5),Y(.60)),str(3-k),font=F(BOLD,300),fill=RED,anchor="ma")
    elif seg==5:
        f0=S[5]+.25
        write(d,["ANSWER: MAYO"],X(.5),Y(.02),F(BOLD,70),GREEN,t,f0,.7,anchor="m")
        stroke(d,jit([(X(.2),Y(.02)+98),(X(.8),Y(.02)+98)]),(t-f0-.8)/.5,GREEN,7)
        items=[(.09,"1. Pay per item is\n    Taylor's idea."),(.25,"2. Staff feel ignored and leave:\n    a social need (Mayo)."),(.53,"3. So build teamwork and\n    listen to staff.")]
        y=Y(.15)
        for fr,txt in items:
            ls=txt.split("\n"); write(d,ls,X(.06),y,F(MED,46),BLACK,t,f0+fr*v[5],1.4,gap=8); y+=len(ls)*56+30
        tb=f0+.74*v[5]
        if t>tb:
            d.rectangle((X(.04),Y(.64),X(.96),Y(.64)+300),fill=(255,243,170),outline=INK,width=6)
            write(d,["Name the theory","Link it to the case","Explain the effect"],X(.5),Y(.64)+28,F(BOLD,46),INK,t,tb,2.0,gap=14,anchor="m")
    else:
        f0=S[6]+.25
        d.rectangle((X(.05),Y(.22),X(.95),Y(.22)+520),fill=(255,236,120),outline=INK,width=8)
        write(d,["Comment","MOCK"],X(.5),Y(.22)+40,F(BOLD,150),RED,t,f0,.8,gap=0,anchor="m")
        write(d,["for my free exam checklist"],X(.5),Y(.22)+410,F(MED,42),BLACK,t,f0+.9,1.0,anchor="m")

CAPS=["Taylor versus Mayo isn't as hard as they make it seem.","Taylor thought workers only care about money. So pay them for output, watch them closely, and keep each job simple.","Mayo disagreed. People work harder when they feel valued: teamwork, attention, and being listened to.","Easy way to remember. Taylor is pay and control. Mayo is people and teamwork.","Your turn. Northway's warehouse pays staff per item packed, but staff say nobody listens to them, and many are leaving. Whose theory fits best?","The answer: Mayo. Pay per item is Taylor's idea, but staff are leaving because they feel ignored, which is a social need. So Northway should build teamwork and listen to staff. Name the theory, link it to the case, explain the effect.","Want my free checklist? Comment MOCK."]
_dd=ImageDraw.Draw(Image.new("RGB",(10,10))); CF=F(BOLD,58)
MAXTXT=740
def groups():
    out=[]
    for i,tx in enumerate(CAPS):
        gs=[];cur=[]
        for w_ in tx.split():
            if cur and (len(cur)>=3 or _dd.textlength(" ".join(cur+[w_]).upper(),font=CF)>MAXTXT): gs.append(" ".join(cur)); cur=[w_]
            else: cur.append(w_)
        if cur: gs.append(" ".join(cur))
        tot=sum(len(g) for g in gs); t0=S[i]+.25
        for g in gs:
            d_=v[i]*len(g)/tot; out.append((t0,t0+d_,g)); t0+=d_
    return out
GR=groups()
CXC=(SAFE[0]+SAFE[2])//2   # 490
def caption(d,t):
    for a,b,g in GR:
        if a<=t<b+.05:
            w=d.textlength(g.upper(),font=CF); x0=CXC-w/2-30
            d.rounded_rectangle((x0,CAPY,x0+w+60,CAPY+104),radius=26,fill=(255,214,10),outline=BLACK,width=6)
            d.text((CXC,CAPY+52),g.upper(),font=CF,fill=BLACK,anchor="mm"); return
def frame(t,border=True):
    img=Image.new("RGB",(W,H),BOARD); d=ImageDraw.Draw(img)
    if border: d.rectangle((14,14,W-14,H-14),outline=(200,200,196),width=10)
    vb=Image.new("RGB",(VW,VH),BOARD); board(ImageDraw.Draw(vb),t)
    vb=vb.resize((int(VW*SC),int(VH*SC)),Image.LANCZOS); img.paste(vb,(BX,BY))
    caption(ImageDraw.Draw(img),t)
    return img
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="check":
        bad=0; bb=[9999,9999,0,0]
        for k in range(0,int(TOTAL*10)):
            t=k/10; a=np.array(frame(t,False)).astype(int); m=(np.abs(a-np.array(BOARD)).sum(2)>30)
            ys,xs=np.where(m)
            if len(xs)==0: continue
            x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
            bb=[min(bb[0],x0),min(bb[1],y0),max(bb[2],x1),max(bb[3],y1)]
            if x0<SAFE[0] or y0<SAFE[1] or x1>SAFE[2] or y1>SAFE[3]: bad+=1; print("OUT",t,x0,y0,x1,y1)
        print("bbox",bb,"safe",SAFE,"violations",bad)
    elif mode=="prev":
        for tt in sys.argv[2:]: frame(float(tt)).save(f"prev_{float(tt):.0f}.png")
    else:
        p=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","final_audio.wav","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","taylor_mayo.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
        for f in range(int(TOTAL*FPS)): p.stdin.write(frame(f/FPS).tobytes())
        p.stdin.close(); p.wait(); print("done")
