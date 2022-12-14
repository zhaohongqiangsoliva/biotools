# !/usr/bin/env python3
# coding: utf-8
import glob
import sys, os ,logging
import argparse
from signal import signal, SIGPIPE, SIG_DFL
import subprocess as sb
import json,csv
signal(SIGPIPE, SIG_DFL)
from pathlib import Path


script_dir = os.path.split(os.path.realpath(__file__))[0]
'''
process path : /work/share/ac7m4df1o5/bin/cromwell/5_process 
gatk path : /work/share/ac7m4df1o5/bin/GATK-4.2.6.1/gatk-4.2.6.1/gatk
fasta dict path ： /work/share/ac7m4df1o5/data/ref/gatk_bundle_hg38/data/Homo_sapiens_assembly38.dict
outputs path : output
ReadGroup: /work/share/ac7m4df1o5/bin/cromwell/5_process/Exome_Germline_Single_Sample/ReadGroup.sh

'''
### reading  server config
with open(script_dir+'/config.json') as j:
    config_j = json.load(j)
    bedtointerval = config_j['bedtointerval']
    global_options = config_j["global"]
    fastq2ubam = config_j["fastq2ubam"]
    WES_pipe = config_j["WES_pipe"]

## script belong to directory



### setting logging format

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
'''
sample csv：

patient,sample,lane,fastq1,fastq2
'''


def running(commands):
    '''
    running subprocess popen fun to running Command line
    '''

    process = sb.Popen(commands, stdin=sb.PIPE, stdout=sb.PIPE,shell=True)
    out, err = process.communicate()
    print(out)

def make_step(commands,step):
    with open(step,"w") as f:
        f.write(commands)
    return 0




class pipeline(object):
    def __init__(self,output):
        self.outputs=output
        self.fa_dict = None
        self.shell_bed2inter_sh = "/work/share/ac7m4df1o5/bin/cromwell/5_process/Exome_Germline_Single_Sample/1.bedtointervalLsit.sh"
        self.makeresult_sh = "/work/share/ac7m4df1o5/bin/cromwell/5_process/Exome_Germline_Single_Sample/2.makeResult_dir.sh"
        self.readgroup_sh = "/work/share/ac7m4df1o5/bin/cromwell/5_process/Exome_Germline_Single_Sample/ReadGroup.sh"
        self.pipe = ""
        self.options= global_options["options"]

    def bedtointerval_list(self,bed,output,fa_dict):
        cmd = "".join(self.shell_bed2inter_sh,bed ,fa_dict,output)
        return self.pipe + pipe

    def mkdirofRsult(self,sample_name):
        sample_path = self.outputs + "/" + sample_name
        cmd = f"""
mkdir -vp {self.outputs}/{sample_name}/cromwell/{{outputs,wf_logs,call_logs}}
cp {self.options} {sample_path}
sed -i "s#/Users/michael_scott/#{self.outputs}/#g" {sample_path}/options.json 
        """
        return cmd

    def readgroup(self,fastq1,fastq2,lane,sample_name,sample_path):
        cmd=f'''
#if fastq.gz change cat to zcat
header=$(zcat {fastq1} | head -n 1)
ID=$(echo $header | head -n 1 | cut -f 1-3 -d":" | sed 's/@//' | sed 's/:/./g')
PU=$(echo $header | head -n 1 | cut -f 1-4 -d":" | sed 's/@//' | sed 's/:/./g')
SM={sample_name}
LB="$ID.$(echo $header | head -n 1 | grep -Eo "[ATGCN]+$")_.{lane}"
cat> {sample_path}/{lane}.{sample_name}.fq2ubam.json<<EOF
{{
"ConvertPairedFastQsToUnmappedBamWf.readgroup_name": "$ID.{lane}.$SM",
  "ConvertPairedFastQsToUnmappedBamWf.sample_name": "{sample_name}",
  "ConvertPairedFastQsToUnmappedBamWf.fastq_1": "{fastq1}",
  "ConvertPairedFastQsToUnmappedBamWf.fastq_2": "{fastq2}",
  "ConvertPairedFastQsToUnmappedBamWf.library_name": "$LB",
  "ConvertPairedFastQsToUnmappedBamWf.platform_unit": "$PU.{lane}.$SM",
  "ConvertPairedFastQsToUnmappedBamWf.run_date": "2016-09-01T02:00:00+0200",
  "ConvertPairedFastQsToUnmappedBamWf.platform_name": "ILLUMINA",
  "ConvertPairedFastQsToUnmappedBamWf.sequencing_center": "BI",

  "ConvertPairedFastQsToUnmappedBamWf.make_fofn": "true"
  }}
EOF
'''
        # cmd = " ".join(["sh" ,self.readgroup_sh , fastq1 , fastq2 , sample_name])
        return cmd

    def fq2ubam(self,fq2ubam_wdl,input_json,option_json):

        cmd =f"""cromshell-alpha submit \
{fq2ubam_wdl} \
{input_json}  \
-op {option_json} \
-n 
            """

        return cmd

    def hard_link(self,fq1,fq2,rawdata):
        try:
            os.link(fq1, os.path.join(rawdata, os.path.basename(fq1)))

        except FileExistsError:
            logger.warning(f"{fq1} exists")
        try:
            os.link(fq2, os.path.join(rawdata, os.path.basename(fq2)))

        except FileExistsError:
            logger.warning(f"{fq2} exists")

    def submit_Wes(self,wdl,input_json,options,zip_file):
        cmd = f"""
cromshell-alpha submit  {wdl}  {input_json} -op {options} -d {zip_file}      
        """
        return cmd







########################process ######################
    def fq2ubam_process(self,rander):
        cmd = []
        # self.wdl_path =
        for samplelist in rander:
            patient = samplelist["patient"]
            lane = samplelist["lane"]
            sample_name = samplelist["sample"]
            sample_path = self.outputs + "/" + sample_name
            fq1 = samplelist["fastq1"]
            fq2 = samplelist["fastq2"]
            rawdata = self.outputs + "/" + sample_name + "/rawdata"
            hardL_fq1 = os.path.join(rawdata, os.path.basename(fq1))
            hardL_fq2 = os.path.join(rawdata, os.path.basename(fq2))
            logger.info(f"Running Patient: {patient} -----Lane ID : {lane} -----  Sample name : {sample_name}")


            #######################CMD running code #########################
            #0.makedir outputs/{sample/rawdata}
            Path(rawdata).mkdir(parents=True ,exist_ok=True)

            #1.ln fastq
            self.hard_link(fq1,fq2,rawdata)

            #2.mkdir of reuslt
            cmd_MR = self.mkdirofRsult(sample_name)

            # print(cmd_MR)
            make_step(cmd_MR, f"{self.outputs}/{sample_name}/1.makeResult.sh")

            #3.readgroup
            cmd_RG = self.readgroup(hardL_fq1,hardL_fq2,lane,sample_name,sample_path)

            # print(cmd_RG)
            make_step(cmd_RG,f"{self.outputs}/{sample_name}/2.readGroup.{lane}.sh")
            input_json = f"{lane}.{sample_name}.fq2ubam.json"

            #4.submit to fastq to ubam
            cmd_F2U = self.fq2ubam(fastq2ubam["wdl"],input_json,self.options)
            print(cmd_F2U)
            make_step(cmd_F2U,f"{self.outputs}/{sample_name}/3.{lane}.{sample_name}.fq2ubam.sh")
            cmd=cmd+ [cmd_MR] + [cmd_RG] #+ [cmd_F2U]

        return cmd

    def WES_process(self,rander):

        cmd = []
        for samplelist in rander:
            patient = samplelist["patient"]
            lane = samplelist["lane"]
            sample_name = samplelist["sample"]
            ubamdir = os.path.join(self.outputs,sample_name,"cromwell/outputs")
            ubamlist = glob.glob(f"{ubamdir}/*unmaped.bam")
            input_json_dict = json.load(open(WES_pipe["wes_input_json"]))
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["sample_name"] = sample_name
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["base_file_name"]=sample_name
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["final_gvcf_base_name"]= sample_name
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["flowcell_unmapped_bams"] = ubamlist
            json.dump(input_json_dict,open(f"{self.outputs}/{sample_name}/{sample_name}.json","w"),indent=4,sort_keys=True)
            # TODO
            # update bed file and interval list
            cmd_WES = self.submit_Wes(WES_pipe["wdl"],
                            f"{self.outputs}/{sample_name}/{sample_name}.json",
                            self.options,
                            WES_pipe["zip"])
            make_step(cmd_WES, f"{self.outputs}/{sample_name}/4.sb_wes.sh")

        #5.modify json for WES pipe
        #6.submit WES
        #7.cp bam to result dir
        #8.hard filter
        #9.genotype filter





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file, you can use stdin or python task_submit.py input_file' ,nargs='?')
    parser.add_argument("-p","--pipe",help="input pipeline para: fq2ubam,wes")
    parser.add_argument("-o","--output",help="please type output as -o",default=os.getcwd())
    args = parser.parse_args()

    if args.input is not  None:
        sample_csv = args.output
    else:
        sample_csv  = '/dev/stdin'


    pipe = pipeline(args.output)
    with open(sample_csv, "r") as f:
        reader = csv.DictReader(f)
        if args.pipe == "fq2ubam":
            cmds = pipe.fq2ubam_process(reader)
        if args.pipe == "wes":
            cmds = pipe.WES_process(reader)
        # print(cmd)
        for cmd in cmds:
            print(cmd)
            running(cmd)


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()