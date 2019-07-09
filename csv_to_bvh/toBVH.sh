#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
bash "$mainDir"/myCSVgenerator.sh "$1"
bash "$mainDir"/myBVHgenerator.sh
#python3 "$mainDir"/write_rawjointsFiles.py
#bash "$mainDir"/main/generateCSV.sh "$mainDir"/raw_csv.txt "$mainDir"/processedCSV/
#python3 "$mainDir"/write_processedjointsFiles.py
#bash "$mainDir"/main/generateBVH.sh "$mainDir"/processed_csv.txt "$mainDir"/bvhFiles
