
dir="data"
inf="$dir/no.outliers.pop.all.pca.gz"
base="no.outliers"
out="$dir/$base.pc12"
myecho "
    zcat $inf | mycut -f1,3,4
    | python3 ~/python/CategoryPlot2.py -x pc1 -y pc2 -o $out.pdf.html --lloc 5 --lm 50
    &&
        phantomjs ~/scripts/js/rasterize.js $out.pdf.html $out.pdf 6in*4in
    &&  rm $out.pdf.html"

out="$dir/$base.pc13"
myecho "
    zcat $inf | mycut -f1,3,5
    | python3 ~/python/CategoryPlot2.py -x pc1 -y pc3 -o $out.pdf.html --lloc 5 --lm 50
    &&
        phantomjs ~/scripts/js/rasterize.js $out.pdf.html $out.pdf 6in*4in
    &&  rm $out.pdf.html"

out="$dir/$base.pc32"
myecho "
    zcat $inf | mycut -f1,5,4
    | python3 ~/python/CategoryPlot2.py -x pc3 -y pc2 -o $out.pdf.html --lloc 5 --lm 50
    &&
        phantomjs ~/scripts/js/rasterize.js $out.pdf.html $out.pdf 6in*4in
    &&  rm $out.pdf.html"
