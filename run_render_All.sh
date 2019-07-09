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
            "C:\Program Files\Blender Foundation\Blender\blender" -b -P "${mainDir}"/render.py --  --bvhFile "${bvh}" --mhx2File "${mhx2}" $1 $2 $3 $4 $5 $6 $7 $8
        elif [ "$#" -ge 8 ]
        then
            "C:\Program Files\Blender Foundation\Blender\blender" -b -P "${mainDir}"/render.py --  --bvhFile "${bvh}" --mhx2File "${mhx2}" $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10}
        else
            echo "Provide Arguments are not proper"
            exit 2
        fi
    done
done