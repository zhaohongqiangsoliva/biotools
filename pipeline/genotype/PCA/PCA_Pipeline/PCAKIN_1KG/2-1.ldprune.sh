# Do LD prune for run PCA and estimate kinship matrix.

pp -j 1 -q wecho "
	plink
	--bfile data/{}
    --maf 0.01 --hwe 1e-10 --geno 0.05
	--indep-pairwise 1000 50 0.2
	--out data/ld
	&&
	plink
	--bfile data/{}
	--extract data/ld.prune.in
    --make-bed
	--out data/pruned.{}
" ::: qc.all.chr
