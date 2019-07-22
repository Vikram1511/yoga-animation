#! /bin/bash

export mainDir="$(dirname "$(readlink -f "$0")")"
bvhDir="$mainDir"/bvhFiles
mhx2Dir="$mainDir"/characters
# echo $subjs
for mhx2 in "${mhx2Dir}/"*.mhx2
do
    for bvh in "${bvhDir}/"*.bvh
    do
        if [ "$#" -ge 6 ]
        then
            blender -b -P "${mainDir}"/render.py --  --bvhFile "${bvh}" --mhx2File "${mhx2}" "$@"
        else
            echo "Provide Arguments are not proper"
            exit 2
        fi
    done
done
