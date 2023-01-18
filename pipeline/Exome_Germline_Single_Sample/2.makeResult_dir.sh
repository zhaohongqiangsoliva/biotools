# sh 2.makeResult_dir.sh <input dir>
# creat cromwell result project dir
mkdir -vp $1/cromwell/{outputs,wf_logs,call_logs}
# copy template input json for input dir
cp /work/share/ac7m4df1o5/bin/cromwell/6_json/1.germline/hg38/temp_hg38_input.json $1

cp /work/share/ac7m4df1o5/bin/cromwell/6_json/0.option/options.json $1

sed -i "s#/Users/michael_scott/#$1/#g" options.json
