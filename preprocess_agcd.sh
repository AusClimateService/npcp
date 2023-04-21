#!/bin/bash
#
# Description: Preprocess AGCD data
#             

function usage {
    echo "USAGE: bash $0 agcd_files"
    echo "   agcd_files:   Input AGCD files"
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

infiles=($@)
var=`echo $1 | cut -d'/' -f 7`
if [ "${var}" == "tmax" ]; then
    cmor_var=tasmax
elif [ "${var}" == "tmin" ]; then
    cmor_var=tasmin
elif [ "${var}" == "precip" ]; then
    cmor_var=pr
fi

for infile in "${infiles[@]}"; do
    year=`echo $infile | cut -d'.' -f 1 | rev | cut -d'_' -f 1 | rev`
    outfile=/g/data/ia39/npcp/input_data/${cmor_var}/observations/AGCD/${cmor_var}_NPCP-20i_AGCD_v1_day_${year}01-${year}12.nc
    directory=`dirname ${outfile}`
    command1="mkdir -p ${directory}" 
    command2="${python} ${script_dir}/preprocess.py ${infile} ${var} ${outfile}"
    echo ${command1}
    echo ${command2}
    ${command1}
    ${command2}
done

