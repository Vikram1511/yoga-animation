#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    ./a.exe $line "$2"
done < "$1"
