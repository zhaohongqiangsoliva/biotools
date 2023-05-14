'Naval Fate.

Usage:

  naval_fate.R <file> <x> <y>
  naval_fate.R (-h | --help)
  naval_fate.R --version

Options:
  -h --help     Show this screen.
  --version     Show version.

' -> doc

pacman::p_load(dplyr,pROC,bigreadr,stringr,ggplot2,tidyverse,docopt)
pca=read.table("./pca.pc",header = 1)

arguments <- docopt(doc, version = 'plotPCA v1')

pca=read.table(arguments$file,header = 1)
