#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
python "$mainDir"/write_rawjointsFiles.py
bash "$mainDir"/main/generateCSV.sh "$mainDir""/raw_csv.txt" "$mainDir""/processedCSV/"
