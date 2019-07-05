#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
python "write_rawjointsFiles.py"
bash "$mainDir"/main/generateCSV.sh "raw_csv.txt" "processedCSV/"
python "write_processedjointsFiles.py"
bash "$mainDir"/main/generateBVH.sh "processed_csv.txt" "../bvhFiles"
