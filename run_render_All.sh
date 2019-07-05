#! /bin/bash

export mainDir="$(dirname "$(readlink -f "$0")")"
bvhDir="$mainDir"/bvhFiles
mhx2Dir="$mainDir"/characters
# echo $subjs

for mhx2 in "${mhx2Dir}/"*.mhx2
do
    for bvh in "${bvhDir}/"*.bvh
    do
        if [ "$#" -eq 6 ]
        then
            "C:\Program Files\Blender Foundation\Blender\blender" -b -P "${mainDir}"/render.py --  --bvhFile "${bvh}" --mhx2File "${mhx2}" $1 $2 $3 $4 $5 $6
        elif [ "$#" -eq 8 ]
        then
            "C:\Program Files\Blender Foundation\Blender\blender" -b -P "${mainDir}"/render.py --  --bvhFile "${bvh}" --mhx2File "${mhx2}" $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10}
        else
            echo "Provide Arguments are not proper"
            exit 2
        fi
    done
done

# for subj in ${subjs} ; do
#   asans=`(cd ${baseDir}/${subj}/; echo *asan*)`

#   for asan in $asans ; do
#     base=${baseDir}/${subj}/${asan} 
#     echo "python demo_video.py --input ${base}/color.avi --depth ${base}/depth_files/ --joints ${base}/joints.csv --output ${outdir}/${subj}_${asan}.csv"
#   done
# done