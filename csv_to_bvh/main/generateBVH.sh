#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
if [ $# > 2 ]; then
    "$mainDir"/a.exe "$1" "$2"
fi
