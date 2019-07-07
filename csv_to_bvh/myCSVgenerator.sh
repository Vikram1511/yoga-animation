#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
python "$mainDir"/write_rawjointsFiles.py
bash "$mainDir"/main/generateCSV.sh "raw_csv.txt" "processedCSV/"