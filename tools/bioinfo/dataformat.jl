using DataFrames
using CSV
data = CSV.File("/Users/soliva/Desktop/2_work/family_calling/family1.csv") |> DataFrame
print(data)