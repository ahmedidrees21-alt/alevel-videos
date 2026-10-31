import json
v=[3.6,7.52,7.84,6.4,3.52]
dur=[x+0.35 for x in v]; dur[4]=v[4]+0.8
S=[0]
for d in dur[:-1]: S.append(S[-1]+d)
TOTAL=round(S[-1]+dur[-1],2)
L=[S[1]+.25+f*v[1] for f in (.38,.62,.88)]+[S[2]+.25+f*v[2] for f in (.42,.60,.86)]
EV={"levels":L,"cuts":[S[3],S[4]],"ticks":[],"ding":S[3]+.25+.12*v[3]}
if __name__=="__main__":
    json.dump({"S":S,"v":v,"dur":dur,"TOTAL":TOTAL,"EV":EV},open("tl.json","w")); print(S,TOTAL)
