#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    python parseCSV.py $line
done < "$1"
