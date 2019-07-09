#!/bin/bash
export input="$(dirname "$(readlink -f "$0")")"
backdir=`(dirname "$input")`
python "$input"/write_processedjointsFiles.py
bash "$input"/main/generateBVH.sh "$input"/processed_csv.txt "$backdir"/bvhFiles
