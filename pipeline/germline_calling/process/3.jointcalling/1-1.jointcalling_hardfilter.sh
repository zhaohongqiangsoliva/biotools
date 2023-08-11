reference=$2
outname=$1
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
ped_file=$3
hrun -s hard_filter.log "
#combin gvcf to vcf file
sh ${SHELL_FOLDER}/1.gvcfcombin.sh
${outname}
${reference}
${ped_file}
&&
#using gatk hard filter vcf
sh ${SHELL_FOLDER}/HardFilter/hard_filter.sh
${reference}
${outname}


"
