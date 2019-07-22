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
if [ "$#" -ge 10 ]
then
    blender -b -P "${dir}"/render.py --  "$@" 
else
    echo "Provide Arguments are not proper"
fi
