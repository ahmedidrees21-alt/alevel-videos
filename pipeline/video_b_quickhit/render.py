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
    seg=max(i for i in range(5) if t>=S[i])
    if seg==0:
        write(d,["POV: the exam asks"],X(.5),Y(.06),F(BOLD,64),INK,t,.05,.5,anchor="m")
        write(d,["PAY"],X(.5),Y(.17),F(BOLD,230),RED,t,.4,.35,anchor="m")
        write(d,["or"],X(.5),Y(.40),F(BOLD,80),(120,120,120),t,.8,.2,anchor="m")
        write(d,["PRAISE?"],X(.5),Y(.48),F(BOLD,190),GREEN,t,1.0,.5,anchor="m")
        stroke(d,jit([(X(.12),Y(.48)+215),(X(.88),Y(.48)+215)]),(t-1.7)/.5,RED,8)
        write(d,["Answer in 25 seconds"],X(.5),Y(.76),F(BOLD,56),INK,t,2.3,.9,anchor="m")
    elif seg<=3:
        write(d,["MOTIVATION"],X(.5),Y(.01),F(BOLD,62),INK,t,S[1]+.1,.7,anchor="m")
        stroke(d,jit([(X(.2),Y(.01)+84),(X(.8),Y(.01)+84)]),(t-S[1]-.9)/.5,RED,7)
        cols=((.02,.49,BLUEC,"FINANCIAL",S[1]+.3),(.51,.98,YEL,"NON-FINANCIAL",S[2]+.3))
        for (x0,x1,c,lab,tt) in cols:
            if t>tt:
                a_=clamp((t-tt)/.4)
                d.rectangle((X(x0),Y(.12),X(x1),Y(.12)+110),fill=lerp(BOARD,c,a_),outline=INK,width=6)
                write(d,[lab],X((x0+x1)/2),Y(.12)+30,F(BOLD,44 if len(lab)>9 else 52),INK,t,tt,.5,anchor="m")
        stroke(d,jit([(X(.5),Y(.12)),(X(.5),Y(.60))]),(t-(S[1]+.6))/1.0,(150,150,150),5)
        fin=["Pay","Bonuses","Commission","Profit sharing"]; nf=["Praise","Promotion","Teamwork","Responsibility"]
        for k in range(4):
            ta=EV["levels"][k]
            if t>=ta:
                d.ellipse((X(.04),Y(.255)+k*98+16,X(.04)+16,Y(.255)+k*98+32),fill=INK)
                write(d,[fin[k]],X(.075),Y(.255)+k*98,F(BOLD,44),BLACK,t,ta,.45)
            tb_=EV["levels"][4+k]
            if t>=tb_:
                d.ellipse((X(.54),Y(.255)+k*98+16,X(.54)+16,Y(.255)+k*98+32),fill=INK)
                write(d,[nf[k]],X(.575),Y(.255)+k*98,F(BOLD,44),BLACK,t,tb_,.45)
        if t>S[1]+.4:
            cx,cy=X(.26),Y(.64)
            d.ellipse((cx-60,cy-60,cx+60,cy+60),fill=(250,205,60),outline=INK,width=6)
            d.text((cx,cy),"£",font=F(BOLD,74),fill=INK,anchor="mm")
        if t>S[2]+.4:
            face(d,X(.68),Y(.64),52,2,(190,235,190)); face(d,X(.84),Y(.64),52,2,(250,215,190))
        if seg==3:
            f3=S[3]+.25
            d.rectangle((X(.03),Y(.74),X(.97),Y(.74)+250),fill=(255,243,170),outline=INK,width=6)
            write(d,["EXAM TRICK"],X(.5),Y(.74)+16,F(BOLD,40),RED,t,f3,.5,anchor="m")
            write(d,["Money = quick results"],X(.5),Y(.74)+70,F(BOLD,46),INK,t,f3+.12*v[3],.8,anchor="m")
            write(d,["Non-financial = lasts longer"],X(.5),Y(.74)+130,F(BOLD,46),INK,t,f3+.36*v[3],1.0,anchor="m")
            write(d,["Say which suits the business"],X(.5),Y(.74)+188,F(MED,38),BLACK,t,f3+.7*v[3],1.0,anchor="m")
    else:
        f0=S[4]+.25
        d.rectangle((X(.05),Y(.22),X(.95),Y(.22)+520),fill=(255,236,120),outline=INK,width=8)
        write(d,["FOLLOW"],X(.5),Y(.22)+60,F(BOLD,150),RED,t,f0,.6,anchor="m")
        write(d,["1 topic a day"],X(.5),Y(.22)+250,F(BOLD,70),INK,t,f0+.5,.8,anchor="m")
        write(d,["A-Level Business"],X(.5),Y(.22)+360,F(MED,48),BLACK,t,f0+1.0,.8,anchor="m")

CAPS=["POV: the exam asks pay or praise. Here's the answer in twenty five seconds.","Financial motivation means money: pay, bonuses, commission, profit sharing.","Non-financial means everything else: praise, promotion, teamwork, more responsibility.","Exam trick: money gets quick results, but non-financial methods tend to last longer. Always say which one suits the business.","Follow for one A-level business topic every day."]
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
        p=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","final_audio.wav","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","quick_hit.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
        for f in range(int(TOTAL*FPS)): p.stdin.write(frame(f/FPS).tobytes())
        p.stdin.close(); p.wait(); print("done")
