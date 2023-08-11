#!/usr/local/env bash

parallel -j 1 -q --colsep ' ' hrun "
l PCA.POP.pc
|wcut -f17,{1},{2}
|tail -n +2
|CategoryPlot2.py  -x PC{3} -y PC{4} -o projection.PC{3}{4}.html --lloc 5 --lm 50

" :::: <(echo -e '3 4 1 2\n5 6 3 4')