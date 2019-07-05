#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
bash "$mainDir"/main/generateBVH.sh "processed_csv.txt" "../bvhFiles"