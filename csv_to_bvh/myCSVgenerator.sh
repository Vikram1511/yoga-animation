#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
bash "$mainDir"/main/generateCSV.sh "raw_csv.txt" "processedCSV/"