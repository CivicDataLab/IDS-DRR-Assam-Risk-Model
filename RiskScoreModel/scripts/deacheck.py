import DEA

DMU,X,Y=DEA.csv2dict("data.csv",in_range=[2,4],out_range=[5,8],assign=True)

print(X)