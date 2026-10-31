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
    seg=max(i for i in range(7) if t>=S[i])
    if seg==0:
        write(d,["PRICE ELASTICITY"],X(.5),Y(.03),F(BOLD,100),INK,t,.05,.5,anchor="m")
        write(d,["ISN'T AS HARD"],X(.5),Y(.17),F(BOLD,98),RED,t,.55,.6,anchor="m")
        stroke(d,jit([(X(.14),Y(.17)+150),(X(.86),Y(.17)+150)]),(t-1.2)/.5,RED,8)
        write(d,["AS THEY MAKE IT SEEM"],X(.5),Y(.33),F(BOLD,60),INK,t,1.3,.9,anchor="m")
        write(d,["One formula. One minute."],X(.5),Y(.47),F(BOLD,64),GREEN,t,2.5,.9,anchor="m")
        write(d,["% demand ÷ % price"],X(.5),Y(.60),F(BOLD,54),INK,t,3.5,.8,anchor="m")
    elif seg<=3:
        write(d,["PRICE ELASTICITY (PED)"],X(.5),Y(.01),F(BOLD,56),INK,t,S[1]+.1,.9,anchor="m")
        stroke(d,jit([(X(.1),Y(.01)+82),(X(.9),Y(.01)+82)]),(t-S[1]-1.1)/.5,RED,7)
        tR=S[1]+.25+.05*v[1]; tL=S[2]+.25+.02*v[2]
        cols=((.02,.49,BLUEC,"FORMULA","how much demand reacts",S[1]+.25+.05*v[1]),(.51,.98,YEL,"EXAMPLE","Northway raises its price",S[2]+.25+.02*v[2]))
        for (x0,x1,c,lab,sub,tt) in cols:
            if t>tt:
                a=clamp((t-tt)/.4)
                d.rectangle((X(x0),Y(.12),X(x1),Y(.12)+110),fill=lerp(BOARD,c,a),outline=INK,width=6)
                write(d,[lab],X((x0+x1)/2),Y(.12)+26,fitf(d,lab,BOLD,52,X(x1-x0)-30),INK,t,tt,.5,anchor="m")
                write(d,[sub],X((x0+x1)/2),Y(.12)+128,fitf(d,sub,MED,32,X(x1-x0)-20),(70,70,70),t,tt+.3,.7,anchor="m")
        stroke(d,jit([(X(.5),Y(.12)),(X(.5),Y(.67))]),(t-(S[1]+1.0))/1.0,(150,150,150),5)
        g=["% change in demand","÷ % change in price","= PED","reacts a lot or a little"]
        n=["Price up 10%","Demand down 20%","−20 ÷ 10 = −2","elastic: reacts a lot"]
        for k in range(4):
            y=Y(.29)+k*104
            bullet_row(d,t,EV["levels"][k],X(.04),y,g[k],X(.455)-X(.04),BLACK,(200,225,250) if k==2 else None,X(.485))
            bullet_row(d,t,EV["levels"][4+k],X(.54),y,n[k],X(.955)-X(.54),BLACK,(255,236,150) if k==2 else None,X(.975))
        if seg==3:
            f3=S[3]+.25
            d.rectangle((X(.03),Y(.73),X(.97),Y(.73)+260),fill=(255,243,170),outline=INK,width=6)
            write(d,["USE PERCENTAGES"],X(.5),Y(.73)+22,fitf(d,"USE PERCENTAGES",BOLD,60,X(.9)),RED,t,f3+.1*v[3],1.0,anchor="m")
            write(d,["Not pounds. Ignore the minus."],X(.5),Y(.73)+120,F(BOLD,40),INK,t,f3+.4*v[3],1.2,anchor="m")
            write(d,["Above 1 elastic, below 1 inelastic"],X(.5),Y(.73)+186,F(MED,36),BLACK,t,f3+.7*v[3],1.2,anchor="m")
    elif seg==4:
        f0=S[4]+.25
        write(d,["YOUR TURN"],X(.5),Y(.02),F(BOLD,74),RED,t,f0,.6,anchor="m")
        stroke(d,jit([(X(.3),Y(.02)+100),(X(.7),Y(.02)+100)]),(t-f0-.7)/.5,RED,7)
        q="Northway cuts its price by 5%. Demand rises by 15%. What is the price elasticity of demand?"
        f=F(MED,50); lines=wrap(d,q,f,VW*.88)
        write(d,lines,X(.06),Y(.15),f,BLACK,t,f0+.6,6.0,gap=14)
        tc=f0+8.8
        for k,(lab,xx,c) in enumerate((("A  −3",.05,BLUEC),("B  −0.33",.53,YEL))):
            if t>tc+k*.3:
                d.rounded_rectangle((X(xx),Y(.50),X(xx+.42),Y(.50)+110),radius=20,fill=c,outline=INK,width=6)
                d.text((X(xx+.21),Y(.50)+55),lab,font=F(BOLD,52),fill=INK,anchor="mm")
        for k,tk in enumerate(EV["ticks"]):
            if tk<=t<tk+1: d.text((X(.5),Y(.60)),str(3-k),font=F(BOLD,300),fill=RED,anchor="ma")
    elif seg==5:
        f0=S[5]+.25
        write(d,["ANSWER: A  (−3)"],X(.5),Y(.02),F(BOLD,70),GREEN,t,f0,.7,anchor="m")
        stroke(d,jit([(X(.15),Y(.02)+98),(X(.85),Y(.02)+98)]),(t-f0-.8)/.5,GREEN,7)
        items=[(.20,"1. Percentages:\n    price −5%, demand +15%"),(.42,"2. Divide:\n    15 ÷ −5 = −3"),(.60,"3. Read it:\n    3 is above 1 = elastic")]
        y=Y(.15)
        for fr,txt in items:
            ls=txt.split("\n"); write(d,ls,X(.06),y,F(MED,46),BLACK,t,f0+fr*v[5],1.3,gap=8); y+=len(ls)*56+30
        tb=f0+.76*v[5]
        if t>tb:
            d.rectangle((X(.04),Y(.66),X(.96),Y(.66)+210),fill=(255,243,170),outline=INK,width=6)
            write(d,["B flips the formula","Demand % goes on top"],X(.5),Y(.66)+34,F(BOLD,44),INK,t,tb,1.4,gap=22,anchor="m")
    else:
        f0=S[6]+.25
        d.rectangle((X(.05),Y(.22),X(.95),Y(.22)+520),fill=(255,236,120),outline=INK,width=8)
        write(d,["Comment","MOCK"],X(.5),Y(.22)+40,F(BOLD,150),RED,t,f0,.8,gap=0,anchor="m")
        write(d,["for my free exam checklist"],X(.5),Y(.22)+410,F(MED,42),BLACK,t,f0+.9,1.0,anchor="m")


CAPS=["Price elasticity isn't as hard as they make it seem. One formula, and you've got it. Let's go.", "Price elasticity of demand shows how much demand reacts to a price change. It is the percentage change in demand, divided by the percentage change in price.", "Northway raises its price 10%, and demand falls 20%. 20 divided by 10 is minus 2. That's elastic.", "Here's the trap. Use percentages, not pounds. Ignore the minus sign. Above 1 is elastic, below 1 is inelastic.", "Your turn. Northway cuts its price by 5%, and demand rises by 15%. What is the price elasticity of demand? A, minus 3. Or B, minus 0.33.", "The answer is A. 15 divided by minus 5 is minus 3. That is elastic. B flips the formula upside down.", "Want my free checklist? Comment MOCK."]
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
        p=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","final_audio.wav","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","day05_price_elasticity.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
        for f in range(int(TOTAL*FPS)): p.stdin.write(frame(f/FPS).tobytes())
        p.stdin.close(); p.wait(); print("done")
