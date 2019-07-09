#!/bin/bash
export mainDir="$(dirname "$(readlink -f "$0")")"
backdir=`(dirname "$mainDir")`
bash "$mainDir"/csv_to_bvh/toBVH.sh
bash "$mainDir"/run_render_All.sh --fps 15 --videoFormat FFMPEG --Animation True

