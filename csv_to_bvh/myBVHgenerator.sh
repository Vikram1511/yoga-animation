#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
python "$mainDir"/write_processedjointsFiles.py
bash "$mainDir"/main/generateBVH.sh "processed_csv.txt" "../bvhFiles"