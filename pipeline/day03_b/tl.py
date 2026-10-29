import json
v=[3.76,7.04,4.24,5.92,3.36]
dur=[x+0.5 for x in v]; dur[4]=v[4]+0.8
S=[0]
for d in dur[:-1]: S.append(S[-1]+d)
TOTAL=round(S[-1]+dur[-1],2)
L=[S[1]+.25+f*v[1] for f in (.28,.62,.84)]+[S[2]+.25+f*v[2] for f in (.12,.38,.66)]
EV={"levels":L,"cuts":[S[3],S[4]],"ticks":[],"ding":S[3]+.25+.12*v[3]}
if __name__=="__main__":
    json.dump({"S":S,"v":v,"dur":dur,"TOTAL":TOTAL,"EV":EV},open("tl.json","w")); print(S,TOTAL)
