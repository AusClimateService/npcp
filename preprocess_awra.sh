#!/bin/bash
#
# Description: Preprocess AWRA data
#             

function usage {
    echo "USAGE: bash $0 variable"
    echo "   variable:   Variable to process (wind, solar_exposure_day)"
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

var=$1
if [ "${var}" == "wind" ]; then
    cmor_var=wsp
elif [ "${var}" == "solar_exposure_day" ]; then
    cmor_var=rsds
fi

indir=/g/data/fj8/BoM/AWRA/DATA/CLIMATE/${var}
infiles=($(ls ${indir}/${var}_19{8,9}*.nc ${indir}/${var}_20{0,1}*.nc))

outdir=/g/data/ia39/npcp/data/${cmor_var}/observations/AWRA/raw
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for infile in "${infiles[@]}"; do
    year=`echo $infile | cut -d'.' -f 1 | rev | cut -d'_' -f 1 | rev`
    outfile=${outdir}/${cmor_var}_NPCP-20i_AWRA_day_${year}01-${year}12.nc
    if [ "${var}" == "wind" ]; then
        profile=${script_dir}/davenport-vertical-wind-profile-parameters-0.05-mean.h5
        temp_file=${outdir}/${var}-10m_gn_AWRA_day_${year}01-${year}12.nc
        command2="${python} ${script_dir}/wind_2m_to_10m.py ${infile} ${var} ${profile} ${temp_file}"
        echo ${command2}
        ${command2}

        command3="${python} ${script_dir}/preprocess.py ${temp_file} ${var} ${outfile}"
        echo ${command3}    
        ${command3}
    
        command4="rm ${temp_file}"
        echo ${command4}
        ${command4}
    else
        command2="${python} ${script_dir}/preprocess.py ${infile} ${var} ${outfile}"
        echo ${command2}    
        ${command2}
    fi
done

