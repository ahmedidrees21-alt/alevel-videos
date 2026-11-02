import sys
from common import *
import numpy as np
VW,VH=1000,1250          # virtual board size
SC=0.84                  # scale -> 840 x 1050
BX,BY=70,190             # board placed inside TikTok safe zone
SAFE=(60,180,920,1380)   # x0,y0,x1,y1 : nothing may be drawn outside
CAPY=1262
BLUEC=(130,185,240); YEL=(250,212,80)
def fitf(d,text,name,size,maxw):
    while size>20 and d.textlength(text,font=F(name,size))>maxw: size-=2
    return F(name,size)
def bullet_row(d,t,tt,x,y,text,maxw,color=BLACK,hl=None,x1=None):
    if t<tt: return
    if hl is not None: d.rounded_rectangle((x-14,y-8,x1,y+58),radius=14,fill=hl)
    f=fitf(d,text,BOLD,42,maxw); write(d,[text],x,y,f,color,t,tt,.5)
def mark(d,cx,cy,ok,t,t0):
    a=clamp((t-t0)/.25)
    if a<=0: return
    r=int(58*a)
    col=GREEN if ok else RED
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=col)
    if a>=1:
        if ok: d.line([(cx-26,cy+2),(cx-8,cy+22),(cx+28,cy-22)],fill=(255,255,255),width=12,joint="curve")
        else:
            d.line([(cx-24,cy-24),(cx+24,cy+24)],fill=(255,255,255),width=12); d.line([(cx+24,cy-24),(cx-24,cy+24)],fill=(255,255,255),width=12)
def board(d,t):
    X=lambda x:x*VW; Y=lambda y:y*VH
    seg=max(i for i in range(5) if t>=S[i])
    if seg==0:
        write(d,["POV: THE EXAM ASKS"],X(.5),Y(.04),fitf(d,"POV: THE EXAM ASKS",BOLD,70,X(.94)),INK,t,.05,.5,anchor="m")
        write(d,["PRODUCT"],X(.5),Y(.12),fitf(d,"PRODUCT",BOLD,130,X(.94)),RED,t,.5,.5,anchor="m")
        write(d,["OR PRICE?"],X(.5),Y(.30),fitf(d,"OR PRICE?",BOLD,110,X(.94)),RED,t,1.0,.6,anchor="m")
        stroke(d,jit([(X(.12),Y(.30)+150),(X(.88),Y(.30)+150)]),(t-1.8)/.5,INK,8)
        write(d,["Which one wins?"],X(.5),Y(.59),F(BOLD,68),GREEN,t,2.3,.6,anchor="m")
        write(d,["Marketing mix worked example"],X(.5),Y(.70),fitf(d,"Marketing mix worked example",BOLD,44,X(.94)),INK,t,3.0,.8,anchor="m")
    elif seg<=3:
        write(d,["NORTHWAY: £5 DELIVERY"],X(.5),Y(.01),F(BOLD,50),INK,t,S[1]+.1,.7,anchor="m")
        stroke(d,jit([(X(.1),Y(.01)+78),(X(.9),Y(.01)+78)]),(t-S[1]-.9)/.5,RED,7)
        cols=((.02,.49,BLUEC,"PRICE-LED",S[1]+.3),(.51,.98,YEL,"PRODUCT-LED",S[2]+.2))
        for (x0,x1,c,lab,tt) in cols:
            if t>tt:
                a_=clamp((t-tt)/.4)
                d.rectangle((X(x0),Y(.12),X(x1),Y(.12)+110),fill=lerp(BOARD,c,a_),outline=INK,width=6)
                write(d,[lab],X((x0+x1)/2),Y(.12)+26,fitf(d,lab,BOLD,52,X(x1-x0)-30),INK,t,tt,.5,anchor="m")
        stroke(d,jit([(X(.5),Y(.12)),(X(.5),Y(.66))]),(t-(S[1]+.6))/1.0,(150,150,150),5)
        w=["Fee: £5 to £3","Demand rises","Margin shrinks"]; r=["Add live tracking","Fee: £7","Loyal buyers stay"]
        for k in range(3):
            y=Y(.27)+k*110
            bullet_row(d,t,EV["levels"][k],X(.04),y,w[k],X(.455)-X(.04),BLACK,(200,225,250) if k==2 else None,X(.485))
            bullet_row(d,t,EV["levels"][3+k],X(.54),y,r[k],X(.955)-X(.54),BLACK,(255,236,150) if k==2 else None,X(.975))
        if seg==3:
            f3=S[3]+.25
            d.rectangle((X(.03),Y(.74),X(.97),Y(.74)+250),fill=(255,243,170),outline=INK,width=6)
            write(d,["EXAM TRICK"],X(.5),Y(.74)+16,F(BOLD,40),RED,t,f3,.5,anchor="m")
            write(d,["Neither always wins"],X(.5),Y(.74)+70,F(BOLD,46),INK,t,f3+.1*v[3],.9,anchor="m")
            write(d,["Match the target market"],X(.5),Y(.74)+130,F(BOLD,46),INK,t,f3+.4*v[3],1.0,anchor="m")
            write(d,["Then justify it"],X(.5),Y(.74)+188,F(MED,38),BLACK,t,f3+.68*v[3],1.0,anchor="m")
    else:
        f0=S[4]+.25
        d.rectangle((X(.05),Y(.22),X(.95),Y(.22)+520),fill=(255,236,120),outline=INK,width=8)
        write(d,["FOLLOW"],X(.5),Y(.22)+60,F(BOLD,150),RED,t,f0,.6,anchor="m")
        write(d,["1 topic a day"],X(.5),Y(.22)+250,F(BOLD,70),INK,t,f0+.5,.8,anchor="m")
        write(d,["A-Level Business"],X(.5),Y(.22)+360,F(MED,48),BLACK,t,f0+1.0,.8,anchor="m")


CAPS=["POV: the exam asks product or price. Which one wins?", "Price-led: Northway cuts its fee from five pounds to three. Demand rises, but the margin shrinks.", "Product-led: it adds live tracking and charges seven. Quality-focused customers stay.", "Exam trick: neither always wins. Match the mix to the target market, then justify it.", "Follow for one A-level business topic every day."]
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
        p=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","final_audio.wav","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","day07_product-vs-price.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
        for f in range(int(TOTAL*FPS)): p.stdin.write(frame(f/FPS).tobytes())
        p.stdin.close(); p.wait(); print("done")
