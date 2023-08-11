#!/usr/bin/env bash
 ## LDprune
 hrun "
 	plink
 	--bfile result/QC/qc.all.chr
     --maf 0.01 --hwe 1e-10 --geno 0.05
 	--indep-pairwise 1000 50 0.2
 	--out result/LDprune/ld
 	&&
 	plink
 	--bfile result/QC/qc.all.chr
 	--extract result/LDprune/ld.prune.in
     --make-bed
 	--out result/LDprune/pruned.all
 	"