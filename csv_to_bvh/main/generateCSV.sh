#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
while IFS='' read -r line || [[ -n "$line" ]]; do
    python "$mainDir"/parseCSV.py "$line" "$2"
done < "$1"
