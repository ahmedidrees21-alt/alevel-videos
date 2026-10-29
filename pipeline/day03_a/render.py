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
        write(d,["THIS ONE"],X(.5),Y(.03),F(BOLD,150),INK,t,.05,.4,anchor="m")
        write(d,["MISTAKE"],X(.5),Y(.19),F(BOLD,150),RED,t,.4,.45,anchor="m")
        write(d,["COSTS MARKS"],X(.5),Y(.37),F(BOLD,104),INK,t,.85,.6,anchor="m")
        stroke(d,jit([(X(.1),Y(.37)+128),(X(.9),Y(.37)+128)]),(t-1.5)/.5,RED,8)
        write(d,["on every profit margin question"],X(.5),Y(.55),F(BOLD,46),INK,t,2.0,.9,anchor="m")
        write(d,["Gross vs net in ONE minute"],X(.5),Y(.67),F(BOLD,58),GREEN,t,2.9,.8,anchor="m")
    elif seg<=3:
        write(d,["GROSS vs NET MARGIN"],X(.5),Y(.01),F(BOLD,58),INK,t,S[1]+.1,.9,anchor="m")
        stroke(d,jit([(X(.1),Y(.01)+82),(X(.9),Y(.01)+82)]),(t-S[1]-1.1)/.5,RED,7)
        cols=((.02,.49,BLUEC,"GROSS","before overheads",S[1]+.9),(.51,.98,YEL,"NET","after overheads",S[2]+.1))
        for (x0,x1,c,lab,sub,tt) in cols:
            if t>tt:
                a=clamp((t-tt)/.4)
                d.rectangle((X(x0),Y(.12),X(x1),Y(.12)+110),fill=lerp(BOARD,c,a),outline=INK,width=6)
                write(d,[lab],X((x0+x1)/2),Y(.12)+26,F(BOLD,52),INK,t,tt,.5,anchor="m")
                write(d,[sub],X((x0+x1)/2),Y(.12)+128,F(MED,32),(70,70,70),t,tt+.3,.7,anchor="m")
        stroke(d,jit([(X(.5),Y(.12)),(X(.5),Y(.67))]),(t-(S[1]+1.0))/1.0,(150,150,150),5)
        g=["Revenue £200k","− Cost of sales £120k","= Gross profit £80k","÷ Revenue = 40%"]
        n=["Gross profit £80k","− Overheads £50k","= Net profit £30k","÷ Revenue = 15%"]
        for k in range(4):
            y=Y(.29)+k*104
            bullet_row(d,t,EV["levels"][k],X(.04),y,g[k],X(.455)-X(.04),BLACK,(200,225,250) if k==3 else None,X(.485))
            bullet_row(d,t,EV["levels"][4+k],X(.54),y,n[k],X(.955)-X(.54),BLACK,(255,236,150) if k==3 else None,X(.975))
        if seg==3:
            f3=S[3]+.25
            d.rectangle((X(.03),Y(.73),X(.97),Y(.73)+260),fill=(255,243,170),outline=INK,width=6)
            write(d,["ALWAYS ÷ REVENUE"],X(.5),Y(.73)+22,F(BOLD,60),RED,t,f3+.1*v[3],1.0,anchor="m")
            write(d,["Not cost of sales. Not profit."],X(.5),Y(.73)+120,F(BOLD,42),INK,t,f3+.4*v[3],1.2,anchor="m")
            write(d,["Margin = profit ÷ revenue × 100"],X(.5),Y(.73)+186,F(MED,38),BLACK,t,f3+.7*v[3],1.2,anchor="m")
    elif seg==4:
        f0=S[4]+.25
        write(d,["YOUR TURN"],X(.5),Y(.02),F(BOLD,74),RED,t,f0,.6,anchor="m")
        stroke(d,jit([(X(.3),Y(.02)+100),(X(.7),Y(.02)+100)]),(t-f0-.7)/.5,RED,7)
        q="Northway: revenue £400,000, cost of sales £260,000, overheads £100,000. What is the net profit margin?"
        f=F(MED,50); lines=wrap(d,q,f,VW*.88)
        write(d,lines,X(.06),Y(.15),f,BLACK,t,f0+.6,6.0,gap=14)
        tc=f0+8.5
        for k,(lab,xx,c) in enumerate((("A  10%",.05,BLUEC),("B  35%",.53,YEL))):
            if t>tc+k*.3:
                d.rounded_rectangle((X(xx),Y(.50),X(xx+.42),Y(.50)+110),radius=20,fill=c,outline=INK,width=6)
                d.text((X(xx+.21),Y(.50)+55),lab,font=F(BOLD,52),fill=INK,anchor="mm")
        for k,tk in enumerate(EV["ticks"]):
            if tk<=t<tk+1: d.text((X(.5),Y(.60)),str(3-k),font=F(BOLD,300),fill=RED,anchor="ma")
    elif seg==5:
        f0=S[5]+.25
        write(d,["ANSWER: A  (10%)"],X(.5),Y(.02),F(BOLD,70),GREEN,t,f0,.7,anchor="m")
        stroke(d,jit([(X(.15),Y(.02)+98),(X(.85),Y(.02)+98)]),(t-f0-.8)/.5,GREEN,7)
        items=[(.12,"1. Gross profit:\n    400 − 260 = £140k"),(.34,"2. Net profit:\n    140 − 100 = £40k"),(.58,"3. Margin:\n    40 ÷ 400 = 10%")]
        y=Y(.15)
        for fr,txt in items:
            ls=txt.split("\n"); write(d,ls,X(.06),y,F(MED,46),BLACK,t,f0+fr*v[5],1.3,gap=8); y+=len(ls)*56+30
        tb=f0+.80*v[5]
        if t>tb:
            d.rectangle((X(.04),Y(.66),X(.96),Y(.66)+210),fill=(255,243,170),outline=INK,width=6)
            write(d,["35% = the GROSS margin","Check which one is asked"],X(.5),Y(.66)+34,F(BOLD,46),INK,t,tb,1.4,gap=22,anchor="m")
    else:
        f0=S[6]+.25
        d.rectangle((X(.05),Y(.22),X(.95),Y(.22)+520),fill=(255,236,120),outline=INK,width=8)
        write(d,["Comment","MOCK"],X(.5),Y(.22)+40,F(BOLD,150),RED,t,f0,.8,gap=0,anchor="m")
        write(d,["for my free exam checklist"],X(.5),Y(.22)+410,F(MED,42),BLACK,t,f0+.9,1.0,anchor="m")

CAPS=['This one mistake costs marks on every profit margin question. Fix it in one minute.', 'Gross profit is revenue minus cost of sales. Northway: revenue £200,000, cost of sales £120,000. Gross profit is £80,000, so a 40% margin.', 'Net profit also takes off overheads. £50,000 of overheads leaves £30,000. £30,000 over £200,000 is 15%.', "Here's the trap. Always divide by revenue. Never by cost of sales, never by profit.", 'Your turn. Revenue is £400,000, cost of sales is £260,000, overheads are £100,000. What is the net profit margin? A, 10%. Or B, 35%.', 'The answer is A. Gross profit is £140,000. Take off £100,000 of overheads and net profit is £40,000. £40,000 over £400,000 is 10%. 35% is the gross margin.', 'Want my free checklist? Comment MOCK.']
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
        p=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","final_audio.wav","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","day03_gross_net_margin.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
        for f in range(int(TOTAL*FPS)): p.stdin.write(frame(f/FPS).tobytes())
        p.stdin.close(); p.wait(); print("done")
