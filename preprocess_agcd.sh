#!/bin/bash
#
# Description: Preprocess AGCD data
#             

function usage {
    echo "USAGE: bash $0 variable"
    echo "   variable:   Variable to process (tmax, tmin or precip)"
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

var=$1
if [ "${var}" == "tmax" ]; then
    time_agg=mean
    cmor_var=tasmax
elif [ "${var}" == "tmin" ]; then
    time_agg=mean
    cmor_var=tasmin
elif [ "${var}" == "precip" ]; then
    time_agg=total
    cmor_var=pr
fi

indir=/g/data/zv2/agcd/v1-0-1/${var}/${time_agg}/r005/01day
infiles=($(ls ${indir}/agcd_v1-0-1_${var}_${time_agg}_r005_daily_19{6,7,8,9}*.nc ${indir}/agcd_v1-0-1_${var}_${time_agg}_r005_daily_20{0,1}*.nc))

outdir=/g/data/ia39/npcp/data/${cmor_var}/observations/AGCD/raw/task-reference
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for infile in "${infiles[@]}"; do
    year=`echo $infile | cut -d'.' -f 1 | rev | cut -d'_' -f 1 | rev`
    outfile=${outdir}/${cmor_var}_NPCP-20i_AGCD_v1-0-1_day_${year}0101-${year}1231.nc
    command2="${python} ${script_dir}/preprocess.py ${infile} ${var} ${outfile}"
    echo ${command2}    
    ${command2}
done

