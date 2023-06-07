#Created by Xingyu Chen
#Need R, getopt R package
#GWAS summary file require:Tab-separated CHR,SNP,POSITION,A1,A2,A1_FREQ,BETA,SE,P,N_MISSING,N_OBSERVATION with header, .gz file
###Next could try how to let inputed plink file be multiple line for multiple sample

workflow PandT{
	File summary_statistic_2 #Tab-separated CHR,SNP,POSITION,A1,A2,A1_FREQ,BETA,SE,P,N_MISSING,N_OBSERVATION with header, gz file
	String ldref_0 #dir of LD for each algrithom
	File addbeta_script_0 = "/p300s/wangmx_group/chenxy/project/10algorithm/P+T/wdl/adjustformat.R"
	File split_script_0 = "/p300s/wangmx_group/chenxy/project/10algorithm/P+T/wdl/P+T_split.R"
	Array[Float] R2_1_value #comma-seprated r2 value
	Array[Float] Range_1_value #comma-seprated P upper limits

	call adjustformat { input: script=addbeta_script_0, in=summary_statistic_2 }
	call clumping { input: in1_addbeta_summary=adjustformat.out, in2_bfile=ldref_0, r2_value=R2_1_value }
	call split { input: in_rangelist=Range_1_value, in_clumping_summary=clumping.out, script=split_script_0 }
	call zip { input: in_split_result=split.out}
}

#This task will add beta value through OR, using R script
task adjustformat{
	File script
	File in
	command { /p300s/wangmx_group/chenxy/software/conda/envs/wdl/bin/Rscript ${script} -i ${in} -o output_adjustformat.ext}
	output { File out = "output_adjustformat.ext"}
}

#This task will finish clumping
task clumping{
	File in1_addbeta_summary
	String in2_bfile
	Array[Float] r2_value
	command {
		for i in ${sep=" " r2_value}
		do
		/p300s/wangmx_group/chenxy/software/plink/plink \
			--bfile ${in2_bfile}/P_T/plink  \
			--clump-p1 1 \
			--clump-r2 $i \
			--clump-kb 250 \
			--clump ${in1_addbeta_summary} \
			--clump-snp-field SNP \
			--clump-field P \
			--out $i
		done
	}
	output { Array[File] out = glob("*.clumped") }
}

task split{
	Array[Float] in_rangelist
	Array[File] in_clumping_summary
	File script
	command {
		for i in ${sep=" " in_clumping_summary}
		do
		/p300s/wangmx_group/chenxy/software/conda/envs/wdl/bin/Rscript ${script} -i $i -o $(basename $i) --rangelist ${sep=" " in_rangelist}
		done
	}
	output { Array[File] out = glob("*_result") }
}

task zip{
	Array[File] in_split_result
	command {
		IN_DIR=$(dirname ${in_split_result[1]})
		for i in ${sep=" " in_split_result}
			do
			basename $i >> tempfile_name
			done
		less tempfile_name | tr -s "\n" " " | xargs tar czvf result_P+T.tar.gz -C $IN_DIR
		rm tempfile_name
	}
	output { File out = "result_P+T.tar.gz" }
}