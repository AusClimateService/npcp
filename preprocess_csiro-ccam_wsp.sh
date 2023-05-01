#!/bin/bash
#
# Description: Preprocess CSIRO CCAM wind data
#             

function usage {
    echo "USAGE: bash $0"
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

indir=/g/data/xv83/mxt599/ccam_era5_evaluation_aus-10i_12km/drs_cordex/CORDEX/output/AUS-10i/CSIRO/ECMWF-ERA5/evaluation/r1i1p1f1/CSIRO-CCAM-2203/v1/day
ufiles=($(ls ${indir}/uas/uas_AUS-10i_ECMWF-ERA5_evaluation_r1i1p1f1_CSIRO-CCAM-2203_v1_day_19{8,9}*.nc ${indir}/uas/uas_AUS-10i_ECMWF-ERA5_evaluation_r1i1p1f1_CSIRO-CCAM-2203_v1_day_20{0,1}*.nc))
vfiles=($(ls ${indir}/vas/vas_AUS-10i_ECMWF-ERA5_evaluation_r1i1p1f1_CSIRO-CCAM-2203_v1_day_19{8,9}*.nc ${indir}/vas/vas_AUS-10i_ECMWF-ERA5_evaluation_r1i1p1f1_CSIRO-CCAM-2203_v1_day_20{0,1}*.nc))

outdir=/g/data/ia39/npcp/input_data/wsp/ECMWF-ERA5/CSIRO-CCAM-2203
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for (( i=0; i<${#ufiles[*]}; ++i)); do
    upath="${ufiles[$i]}"
    vpath="${vfiles[$i]}"
    ufile=`basename ${upath}`
    temp_file=`echo ${ufile} | sed s:uas:wsp:`
    outfile=`echo ${temp_file} | sed s:AUS-10i:NPCP-20i:`
    temp_path=${outdir}/${temp_file}
    outpath=${outdir}/${outfile}

    command2="${python} ${script_dir}/wind_speed.py ${upath} uas ${vpath} vas ${temp_path}"
    echo ${command2}
    ${command2}

    command3="${python} ${script_dir}/preprocess.py ${temp_path} wsp ${outpath}"
    echo ${command3}    
    ${command3}

    command4="rm ${temp_path}"
    echo ${command4}
    ${command4}
done

