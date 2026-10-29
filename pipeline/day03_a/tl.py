import json
v=[5.52,11.84,8.08,6.16,13.6,12.96,2.72]
dur=[x+0.6 for x in v]; dur[4]=v[4]+3.5; dur[6]=v[6]+0.8
S=[0]
for d in dur[:-1]: S.append(S[-1]+d)
TOTAL=round(S[-1]+dur[-1],2)
L=[S[1]+.25+f*v[1] for f in (.28,.50,.66,.84)]+[S[2]+.25+f*v[2] for f in (.14,.40,.62,.86)]
EV={"levels":L,"cuts":[S[4],S[5],S[6]],"ticks":[S[5]-3,S[5]-2,S[5]-1],"ding":S[5]+.25+.1*v[5]}
if __name__=="__main__":
    json.dump({"S":S,"v":v,"dur":dur,"TOTAL":TOTAL,"EV":EV},open("tl.json","w")); print(S,TOTAL,EV)
