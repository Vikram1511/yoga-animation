python "write_rawjointsFiles.py"
bash main/generateCSV.sh "raw_csv.txt" "processedCSV/"
python "write_processedjointsFiles.py"
cd main
bash generateBVH.sh "../processed_csv.txt" "../../bvhFiles"
