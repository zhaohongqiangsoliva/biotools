#
n=3
wecho "
     bash 1.data.sh | bash
    !bash 1-1.getIndian.sh | pp -j $n
    !bash 1-2.combine.sh | pp -j $n
    !bash 1-3.QC.sh | pp -j $n
    !bash 1-4.mergeChr.sh | bash
    !bash 2-1.ldprune.sh | bash
    !bash 2-2.pcakin.plink.sh | bash
"
