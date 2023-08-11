'Naval Fate.

Usage:
  naval_fate.R [-pca <pca>] [-s <sumprs>]


Options:
  -h --help     Show this screen.
  --version     Show version.
  -pca          pca files
  -s            sumPRS SCORE file

' -> doc

pacman::p_load(dplyr,pROC,bigreadr,stringr,docopt,ggplot2,tidyverse)


arguments <- docopt(doc, version = 'Naval Fate 2.0')
print(arguments)

pca <- read.table(arguments$pca, header = 1)

score <- read.table(arguments$sumprs)
score_df <- rename(score, IID=V1, y=V2)
mdf <- inner_join(pca,score_df,by="IID")
reg.formula <- paste("y ~ ",paste('PC', 1:10, sep = "", collapse = " + ") ,sep="",collapse = " + ")
reg.fit <- lm(reg.formula, data=mdf)
resid <- residuals(reg.fit)
resid_df <- data.frame(IID=mdf$IID, PRS_RESID=resid)
write.csv(x = resid_df,file = "residual.txt",quote=FALSE,row.names = FALSE)