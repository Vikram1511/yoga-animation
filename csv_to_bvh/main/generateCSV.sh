#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    python ../csv_to_bvh/main/parseCSV.py $line "$2"
done < "$1"
