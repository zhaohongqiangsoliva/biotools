#awk -f script.awk GCST90132314_buildGRCh37_format.tsv|bcftools view -O z -o GCST90132314_buildGRCh37_format.vcf.gz


BEGIN   {
    FS="\t";
    }
/^CHROM/ {
    printf("##fileformat=VCFv4.2\n");
    printf("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n");
    printf("##INFO=<ID=AA,Number=1,Type=String,Description=\"TODO\">\n");
    printf("##INFO=<ID=AN,Number=1,Type=String,Description=\"TODO\">\n");
    printf("##INFO=<ID=AD,Number=1,Type=String,Description=\"TODO\">\n");
    printf("##INFO=<ID=SING,Number=0,Type=Flag,Description=\"TODO\">\n");
    printf("##INFO=<ID=SING,Number=0,Type=Flag,Description=\"TODO\">\n");
    printf("##contig=<ID=10,length=135534747,assembly=human_g1k_v37>\n");
    printf("#%s\n",$0);
    next;
    }
    {
    print;
    }
