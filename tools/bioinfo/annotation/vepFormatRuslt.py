import io
import os
import pandas as pd
import numpy as np

def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})

def format_type(lists,df):
    '''
    格式化 vep 中的结果，替换 . 为 None
    '''
    for i in lists:
        df[i]=df[i].replace('.',np.nan).astype(float)
    return df

def unfunction(df,names):
    '''
    去除非功能区

    '''
    for name in names:
        df =df[-df["Consequence"].str.contains(name, regex=True)]
    return df

def read_header(vepannotations):

    global header
    with open(vepannotations) as f:
        for line in f.readlines():
            line.strip()
            if line.startswith('##INFO=<ID=CSQ'):
                header = line.split('Format:')[1][:-2].strip().split('|')
                print(header)
    return header

def Pathogenic(df,names):
    '''
    寻找names  病人的 致病区域 ： 1/1 0/1 1/0
    '''
    for name in names:
        df =df[df[name].str.contains("1/1|0/1|1/0", regex=True)]
    return df


def famcall(files,famname,person,allperson):
    data = pd.read_table(files)
    data=format_type(['gnomADe_AF','gnomADg_AF'],data)
    fam =data.query("gnomADe_AF<0.01 and gnomADg_AF <0.01")
    fam=unfunction(fam,["downstream","intron","synonymous","upstream","non_coding"])
    fam=fam.drop_duplicates(["CHROM-POS-REF-ALT","Consequence"])
    print(fam.columns)
    fam=fam[['CHROM-POS-REF-ALT', 'FORMAT', ]+allperson+[ 'Allele', 'Consequence', 'IMPACT', 'SYMBOL', 'Gene',
       'Feature_type', 'Feature', 'BIOTYPE', 'EXON','gnomADe_AF','gnomADg_AF','CLIN_SIG','SOMATIC', 'PHENO', 'PUBMED',
       'ClinVar', 'ClinVar_CLNSIG',
       'ClinVar_CLNREVSTAT', 'ClinVar_CLNDN','INTRON', 'HGVSc',
       'HGVSp', 'cDNA_position', 'CDS_position', 'Protein_position',
       'Amino_acids', 'Codons', 'Existing_variation', 'ALLELE_NUM', 'DISTANCE',
       'STRAND', 'FLAGS', 'VARIANT_CLASS', 'SYMBOL_SOURCE', 'HGNC_ID',
       'CANONICAL', 'MANE_SELECT', 'MANE_PLUS_CLINICAL', 'TSL', 'APPRIS',
       'CCDS', 'ENSP', 'SWISSPROT', 'TREMBL', 'UNIPARC', 'UNIPROT_ISOFORM',
       'GENE_PHENO', 'SIFT', 'PolyPhen', 'DOMAINS', 'miRNA', 'HGVS_OFFSET',
       'AF', 'AFR_AF', 'AMR_AF', 'EAS_AF', 'EUR_AF', 'SAS_AF',
       'gnomADe_AFR_AF', 'gnomADe_AMR_AF', 'gnomADe_ASJ_AF', 'gnomADe_EAS_AF',
       'gnomADe_FIN_AF', 'gnomADe_NFE_AF', 'gnomADe_OTH_AF', 'gnomADe_SAS_AF',
       'gnomADg_AFR_AF', 'gnomADg_AMI_AF', 'gnomADg_AMR_AF',
       'gnomADg_ASJ_AF', 'gnomADg_EAS_AF', 'gnomADg_FIN_AF', 'gnomADg_MID_AF',
       'gnomADg_NFE_AF', 'gnomADg_OTH_AF', 'gnomADg_SAS_AF', 'MAX_AF','MAX_AF_POPS', 'MOTIF_NAME',
       'MOTIF_POS', 'HIGH_INF_POS', 'MOTIF_SCORE_CHANGE',
       'TRANSCRIPTION_FACTORS']]
    Pathogenic(fam,person).to_csv(famname)


if __name__ == '__main__':

    #''' "./12.annotation_family1_bcftools.txt" ['PC03', 'PC04', 'PC05','wangqinglan'] 'PC01', 'PC03', 'PC04', 'PC05', 'shaoqi','wangqinglan',


    famcall("./12.annotation_family2_bcftools.txt", "family2.csv", ['PC08', 'PC11', 'PC13'],
            ['PC08', 'PC09', 'PC10', 'PC11', 'PC12', 'PC13'])

    famcall("./12.annotation_family3_bcftools.txt", "family3.csv", ['PC14', 'PC15',
                                                                    'PC16', 'PC17', 'PC18', 'PC19'],
            ['PC14', 'PC15', 'PC16', 'PC17', 'PC18', 'PC19', 'PC20', 'PC21'])