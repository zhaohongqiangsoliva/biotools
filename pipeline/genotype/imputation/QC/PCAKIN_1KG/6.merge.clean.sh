# Merge cleaned data.

# convert to jpg.
pp -j 1 -q wecho "
    convert -density 600 results/{}  results/temp.{.}.jpg
    #convert results/temp.no.outliers.pc12.jpg -quality 100 -density 600 -gravity East -chop 1000x0 results/crop.no.outliers.pc12.jpg
" ::: no.outliers.pc12.pdf no.outliers.pc13.pdf no.outliers.pc32.pdf

# crop file.
# *** Direct crop from pdf to jpg will lose quality.
pp -j 1 -q wecho "
    convert results/temp.{.}.jpg -quality 100 -density 600 -gravity East -chop 1000x0 results/crop.{.}.jpg
" ::: no.outliers.pc12.pdf no.outliers.pc13.pdf

# Combine data together.
wecho "
    convert -density 600
        results/crop.no.outliers.pc12.jpg
        results/crop.no.outliers.pc13.jpg
        results/temp.no.outliers.pc32.jpg
        +append results/all.no.outliers.jpg
"
wecho "
    rm results/temp.*.jpg results/crop.*.jpg
"
