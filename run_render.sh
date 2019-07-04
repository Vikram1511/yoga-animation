#! /bin/bash
bvhFileExt=$1
bvhFileInp=$2
mhx2FileExt=$3
mhx2File=$4
fpsExt=$5
fps=$6
videoFormatExt=$7
videoFormat=$8
dir=`pwd`
echo $dir
if [ "$#" -eq 10 ]
then
    "C:\Program Files\Blender Foundation\Blender\blender" -b -P "${dir}"/render.py --  $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10}
elif [ "$#" -eq 12 ]
then
        "C:\Program Files\Blender Foundation\Blender\blender" -b -P "${dir}"/render.py --  $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12}
else
    echo "Provide Arguments are not proper"
fi