import sys
from render import *
from PIL import Image, ImageDraw
ts=[float(x) for x in sys.argv[2:]]
tiles=[]
for t in ts:
    im=frame(t).convert("RGBA"); ov=Image.new("RGBA",im.size,(0,0,0,0)); o=ImageDraw.Draw(ov)
    red=(255,0,0,70)
    o.rectangle((0,0,W,150),fill=red); o.rectangle((0,1420,W,H),fill=red); o.rectangle((930,760,W,1480),fill=red)
    tiles.append(Image.alpha_composite(im,ov).convert("RGB").resize((360,640)))
n=len(tiles); sh=Image.new("RGB",(360*n//2+0,1280),(40,40,40)); cols=n//2
sh=Image.new("RGB",(360*cols,1280))
for i,tl in enumerate(tiles): sh.paste(tl,((i%cols)*360,(i//cols)*640))
sh.save(sys.argv[1])
