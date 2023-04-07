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
import time

'''
sample csv：
WES/WGS
patient,sample,lane,fastq1,fastq2
single_cell
patient,sample,lane,fastq1,fastq2,fastq3    i1 fq_r1 fq_r2
'''

script_dir = os.path.split(os.path.realpath(__file__))[0]


## script belong to directory



### setting logging format

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



def running(commands):
    '''
    running subprocess popen fun to running Command line
    '''

    process = sb.Popen(commands, stdin=sb.PIPE, stdout=sb.PIPE,shell=True,executable='/bin/bash')
    out, err = process.communicate()


def make_step(commands,step):

    with open(step,"w") as f:
        f.write(commands)
    return 0




class pipeline(object):
    def __init__(self,output,p):
        self.partition = p
        self.outputs=output
        self.options= global_options["options"]

#TODO:
    # def bedtointerval_list(self,bed,output,fa_dict):
    #     cmd = "".join(self.shell_bed2inter_sh,bed ,fa_dict,output)
    #     return self.pipe + cmd

    def mkdirofRsult(self,sample_name,option_name,p) :
        '''
        建立结果文件夹以及 copy options.json 创建options.json的文件
        '''
        sample_path = self.outputs + "/" + sample_name
        cmd = f"""
mkdir -vp {self.outputs}/{sample_name}/cromwell/{option_name}/{{outputs,wf_logs,call_logs}}
cp {self.options} {sample_path}/option_{option_name}.json 
sed -i "s#/Users/michael_scott/cromwell/#{self.outputs}/{sample_name}/cromwell/{option_name}/#g" {sample_path}/option_{option_name}.json
"""
        cmd_partition= f"""\n sed -i "s#partitions#{p}#g" {sample_path}/option_{option_name}.json"""
        cmd = cmd + cmd_partition
        print(cmd)
        return cmd

    def readgroup(self,fastq1,fastq2,lane,sample_name,sample_path):
        '''
        make readgroup info to fastq to ubam
        '''


        cmd=f'''
#if fastq.gz change cat to zcat
header=$(zcat {fastq1} | head -n 1)
ID=$(echo $header | head -n 1 | cut -f 1-3 -d":" | sed 's/@//' | sed 's/:/./g'|sed 's#/#.#g')
PU=$(echo $header | head -n 1 | cut -f 1-4 -d":" | sed 's/@//' | sed 's/:/./g'|sed 's#/#.#g')
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

        return cmd




    def hard_link(self,fq_list,rawdata):
        from shutil import copyfile
        for fq in fq_list:
            try:
                os.link(fq, os.path.join(rawdata, os.path.basename(fq)))
            except FileExistsError:
                logger.warning(f"{fq} exists")
            except OSError:
                copyfile(fq, os.path.join(rawdata, os.path.basename(fq)))



    def submit(self,submit_tools,wdl,input_json,options,zip_file,sample_log):
        """
        submit task tools
        """
        cmd = f"{submit_tools} {wdl} {input_json} {options} {zip_file} > {sample_log}"
        return cmd







########################process ######################
    def fastp_clean(self,fastq_dir):
        with open("fastp_clean.sh", "w") as f:
            f.write("mkdir -p cleandata \n")
            for fq1 in glob.glob(fastq_dir+"/"+"*1.f*q.gz"):
                fq2 = fq1.replace("R1","R2")
                cfq1 = os.path.basename(fq1.replace(".fastq.gz","clean.fastq.gz"))
                cfq2 = os.path.basename(fq2.replace(".fastq.gz", "clean.fastq.gz"))
                f.write(f"/work/share/ac7m4df1o5/zhaohq/bio/bin/fastp -i {fq1} -I {fq2} -o cleandata/{cfq1} -O cleandata/{cfq2} -j cleandata/{cfq1}.json -h cleandata/{cfq1}.html \n")
        with open("submit_fastp_clean.sh", "w") as f:
            f.write("""sbatch -p wzhcexclu06 -n 10 --wrap \"parallel -j 3 < fastp_clean.sh \" """)

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
            sample_log = f"{self.outputs}/{sample_name}/submit_wes.log"
            logger.info(f"Running Patient: {patient} -----Lane ID : {lane} -----  Sample name : {sample_name}")


            #######################CMD running code #########################
            #0.makedir outputs/{sample/rawdata}
            Path(rawdata).mkdir(parents=True ,exist_ok=True)

            #1.ln fastq
            self.hard_link([fq1,fq2],rawdata)

            #2.mkdir of reuslt
            option_name = "fq2ubam"
            cmd_MR = self.mkdirofRsult(sample_name,option_name,self.partition)
            options = f"{self.outputs}/{sample_name}/option_fq2ubam.json"
            make_step(cmd_MR, f"{self.outputs}/{sample_name}/1.makeResult.sh")

            #3.readgroup
            cmd_RG = self.readgroup(hardL_fq1,hardL_fq2,lane,sample_name,sample_path)
            make_step(cmd_RG,f"{self.outputs}/{sample_name}/2.readGroup.{lane}.sh")
            input_json = f"{self.outputs}/{sample_name}/{lane}.{sample_name}.fq2ubam.json"

            #4.submit to fastq to ubam
            cmd_F2U = self.submit(
                submit_tools=global_options["cromwell_tools"],
                wdl=fastq2ubam["wdl"],
                input_json=input_json,
                options=options,
                zip_file="",
                sample_log=sample_log
            )
            make_step(cmd_F2U,f"{self.outputs}/{sample_name}/3.{lane}.{sample_name}.fq2ubam.sh")
            cmd=cmd+ [cmd_MR] + [cmd_RG] + [cmd_F2U]

        return cmd

    def WES_process(self,bed,rander):

        cmd = []
        for samplelist in rander:
            patient = samplelist["patient"]
            lane = samplelist["lane"]
            sample_name = samplelist["sample"]
            ubamdir = os.path.join(self.outputs,sample_name,"cromwell/fq2ubam/outputs")
            ubamlist = glob.glob(f"{ubamdir}/*unmapped.bam")
            input_json_dict = json.load(open(WES_pipe["wes_input_json"]))
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["sample_name"] = sample_name
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["base_file_name"]=sample_name
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["final_gvcf_base_name"]= sample_name
            input_json_dict["ExomeGermlineSingleSample.sample_and_unmapped_bams"]["flowcell_unmapped_bams"] = ubamlist
            input_json_dict["ExomeGermlineSingleSample.references"]["calling_interval_list"] =bed
            json.dump(input_json_dict,open(f"{self.outputs}/{sample_name}/{sample_name}.json","w"),indent=4,sort_keys=True)
            # TODO
            # update bed file and interval list
            option_name = "WES"
            cmd_MR = self.mkdirofRsult(sample_name, option_name,self.partition)
            options = f"{self.outputs}/{sample_name}/option_{option_name}.json"
            sample_log = f"{self.outputs}/{sample_name}/submit_{option_name}.log"
            # cmd_WES = self.submit_Wes(
            #     WES_pipe["wdl"],
            #     f"{self.outputs}/{sample_name}/{sample_name}.json",
            #     options,
            #     WES_pipe["zip"],
            #     sample_log)
            cmd_SUB = self.submit(
                submit_tools= global_options["cromwell_tools"],
                wdl=WES_pipe["wdl"],
                input_json=f"{self.outputs}/{sample_name}/{sample_name}.json",
                options=options,
                zip_file=WES_pipe["zip"],
                sample_log=sample_log
            )
            make_step(cmd_SUB, f"{self.outputs}/{sample_name}/4.sb_{option_name}.sh")
            cmd = cmd + [cmd_MR] + [cmd_SUB]
        return cmd





    def WGS_process(self,bed,rander):

        cmd = []
        for samplelist in rander:
            patient = samplelist["patient"]
            lane = samplelist["lane"]
            sample_name = samplelist["sample"]
            ubamdir = os.path.join(self.outputs,sample_name,"cromwell/fq2ubam/outputs")
            ubamlist = glob.glob(f"{ubamdir}/*unmapped.bam")
            ####SETTING####
            option_name = "WGS"
            input_json_dict = json.load(open(WGS_pipe["wgs_input_json"]))
            ###############

            input_json_dict["WholeGenomeGermlineSingleSample.sample_and_unmapped_bams"]["sample_name"] = sample_name
            input_json_dict["WholeGenomeGermlineSingleSample.sample_and_unmapped_bams"]["base_file_name"]=sample_name
            input_json_dict["WholeGenomeGermlineSingleSample.sample_and_unmapped_bams"]["final_gvcf_base_name"]= sample_name
            input_json_dict["WholeGenomeGermlineSingleSample.sample_and_unmapped_bams"]["flowcell_unmapped_bams"] = ubamlist
            #input_json_dict["ExomeGermlineSingleSample.references"]["calling_interval_list"] =bed
            json.dump(input_json_dict,open(f"{self.outputs}/{sample_name}/{sample_name}.json","w"),indent=4,sort_keys=True)
            # TODO
            # update bed file and interval list

            cmd_MR = self.mkdirofRsult(sample_name, option_name,self.partition)
            options = f"{self.outputs}/{sample_name}/option_{option_name}.json"
            sample_log = f"{self.outputs}/{sample_name}/submit_{option_name}.log"

            cmd_SUB = self.submit(
                submit_tools= global_options["cromwell_tools"],
                ####SETTING####
                wdl=WGS_pipe["wdl"],
                input_json=f"{self.outputs}/{sample_name}/{sample_name}.json",
                options=options,
                ####SETTING####
                zip_file=WGS_pipe["zip"],
                sample_log=sample_log
            )
            make_step(cmd_SUB, f"{self.outputs}/{sample_name}/4.sb_{option_name}.sh")
            cmd = cmd + [cmd_MR] + [cmd_SUB]
        return cmd


    def genotype(self):
        pass
    def annotation(self):
        pass

    def single_cell(self, rander,version):
        cmd=[]
        for samplelist in rander:
            patient = samplelist["patient"]
            lane = samplelist["lane"]
            sample_name = samplelist["sample"]
            sample_path = self.outputs + "/" + sample_name
            fq1 = samplelist["fastq1"]
            fq2 = samplelist["fastq2"]
            fq3 = samplelist["fastq3"]
            rawdata = self.outputs + "/" + sample_name + "/rawdata"
            hardL_fq1 = os.path.join(rawdata, os.path.basename(fq1))
            hardL_fq2 = os.path.join(rawdata, os.path.basename(fq2))
            hardL_fq3 = os.path.join(rawdata, os.path.basename(fq3))
            #######################CMD running code #########################
            # 0.makedir outputs/{sample/rawdata}
            Path(rawdata).mkdir(parents=True, exist_ok=True)

            # 1.ln fastq
            self.hard_link([fq1, fq2, fq3], rawdata)
            # option setting
            option_name = "single"
            cmd_MR = self.mkdirofRsult(sample_name, option_name,self.partition)
            options = f"{self.outputs}/{sample_name}/option_single.json"
            make_step(cmd_MR, f"{self.outputs}/{sample_name}/1.makeResult.sh")

            # modify json
            input_json_dict = json.load(open(single_pipe[version]["single_input_json"]))
            input_json_dict["Optimus.i1_fastq"] = [hardL_fq1]
            input_json_dict["Optimus.r1_fastq"] = [hardL_fq2]
            input_json_dict["Optimus.r2_fastq"] = [hardL_fq3]
            json.dump(input_json_dict, open(f"{self.outputs}/{sample_name}/{sample_name}.json", "w"), indent=4,
                      sort_keys=True)
            sample_log = f"{self.outputs}/{sample_name}/submit_wes.log"
            cmd_SC = self.submit(
                submit_tools= global_options["cromwell_tools"],
                wdl=single_pipe["wdl"],
                input_json=f"{self.outputs}/{sample_name}/{sample_name}.json",
                options=options,
                zip_file=single_pipe["zip"],
                sample_log=sample_log)
            make_step(cmd_SC, f"{self.outputs}/{sample_name}/2.sb_single.sh")
            cmd =cmd + [cmd_MR] + [cmd_SC]
        return cmd




def alias_cromshell():
    '''
find `pwd` -name "submit_wes.log" >submitlist.txt
for i in `cat submitlist.txt `
do
name=$(dirname $i|awk -F'/' '{print $NF}')
uid=$(cat $i|grep id|grep -oE "[a-zA-Z0-9-]+\"," |grep -oE "[a-zA-Z0-9-]+")
cromshell alias $uid $name
done
    '''
    pass




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file, you can use stdin or python cromwell_task_submit.py input_file' ,nargs='?')
    parser.add_argument("-p","--pipe",help="input pipeline para: fq2ubam,wes")
    parser.add_argument("-o","--output",help="please type output as -o",default=os.getcwd())
    parser.add_argument("-b", "--bed", help="input : bed interval_list")
    parser.add_argument("-d", "--dryrun",action='store_true', help="try to running ")
    parser.add_argument("-partition","--partition",help="输入运行节点or 队列名称，默认 ",default="wzhcexclu06")
    parser.add_argument("-c", "--config", help="config file path",default="config.json")
    args = parser.parse_args()

    if args.input is not  None:
        sample_csv = args.input
    else:
        sample_csv  = '/dev/stdin'
    ### reading  server config

    with open(script_dir +"/"+ args.config) as j:
        config_j = json.load(j)
        # bedtointerval = config_j['bedtointerval']
        # global_options = config_j["global"]
        # fastq2ubam = config_j["fastq2ubam"]
        # WES_pipe = config_j["WES_pipe"]
        # single_pipe = config_j["single_pipe"]
        for k,v in config_j.items():
            globals()[k] = v
            print(k,v)

    pipe = pipeline(args.output,args.partition)
    if "fastp" in args.pipe:
        pipe.fastp_clean(args.input)
        exit(0)
    with open(sample_csv, "r") as f:
        reader = csv.DictReader(f)
        if "fq2ubam" in args.pipe :
            cmds = pipe.fq2ubam_process(reader)
        if "wes" in args.pipe :
            cmds = pipe.WES_process(args.bed,reader)
        if "sc" in args.pipe:
            if "v2" in args.pipe:
                cmds = pipe.single_cell(reader,"v2")
            elif "v3" in args.pipe:
                cmds = pipe.single_cell(reader,"v3")
            else:
                print("error please input single cell fastq version as v2 or v3")
                logger.error("not input single cell fastq version ")
                exit(1)
        if "wgs" in args.pipe:
            cmds = pipe.WGS_process(args.bed, reader)
        # print(cmd)
        if not args.dryrun:
            for cmd in cmds:
                # print(cmd)
                running(cmd)
                time.sleep(30)


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
