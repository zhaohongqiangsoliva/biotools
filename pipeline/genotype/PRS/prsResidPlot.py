import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


res=pd.read_csv("./residual.txt")
res.sort_values("PRS_RESID",ascending=False)
ax=sns.histplot(data=res,x='PRS_RESID',kde=True,bins=20,color="#CDAA7D",linewidth=0)
plt.axvline(res.loc[0,"PRS_RESID"], 0,0.7,color="grey",linestyle='--')
plt.axvline(res.loc[1,"PRS_RESID"], 0,0.7,color="grey",linestyle='--')
plt.axvline(res.loc[2,"PRS_RESID"], 0,0.7,color="grey",linestyle='--')
plt.text(res.loc[0,"PRS_RESID"],0.1,'hxt',rotation=60)
plt.text(res.loc[1,"PRS_RESID"],0.20,'hxt_M',rotation=60)
plt.text(res.loc[2,"PRS_RESID"],0.20,'hxt_F',rotation=60)
plt.xlabel("PRS Residual score")
ax.lines[0].set_color('grey')
plt.savefig("PRSscore.pdf",dpi=1200)