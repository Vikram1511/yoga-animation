#!/bin/bash
export input="$(dirname "$(readlink -f "$0")")"
if [ $# -ge 2 ]
	then
		"$input"/a.exe "$1" "$2"
	fi