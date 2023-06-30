#!/bin/bash
#
# Description: Preprocess UQ-DES CCAM data
#             

function usage {
    echo "USAGE: bash $0 variable experiment"
    echo "   variable:   Variable to process (tasmax, tasmin, pr, rsds, sfcWind)"
    echo "   experiment: Experiment to process (evaluation, historical, ssp370)" 
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

var=$1
exp=$2

if [ "${var}" == "sfcWind" ]; then
    cmor_var="wsp"
else
    cmor_var=${var}
fi

if [ "${exp}" == "evaluation" ]; then
    parent_model=ECMWF-ERA5
    indir=/g/data/xv83/jis554/UQ-DES/${parent_model}/${var}
    infiles=($(ls ${indir}/${var}_AUS-20i_ECMWF-ERA5_historical_evaluation_UQ-DES-CCAM_v1_day_19{8,9}*.nc ${indir}/${var}_AUS-20i_ECMWF-ERA5_historical_evaluation_UQ-DES-CCAM_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "historical" ]; then
    parent_model=CSIRO-ACCESS-ESM1-5
    indir=/g/data/xv83/jis554/UQ-DES/CSIRO-ACCESS-ESM1-5/historical/r6i1p1f1/UQ-DES-CCAM/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-20i_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_UQ-DES-CCAM_v1_day_19{8,9}*.nc ${indir}/${var}_AUS-20i_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_UQ-DES-CCAM_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "ssp370" ]; then
    parent_model=CSIRO-ACCESS-ESM1-5
    indir=/g/data/xv83/jis554/UQ-DES/CSIRO-ACCESS-ESM1-5/ssp370/r6i1p1f1/UQ-DES-CCAM/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_UQ-DES-CCAM_v1_day_201*.nc ${indir}/${var}_AUS-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_UQ-DES-CCAM_v1_day_20{8,9}*.nc))
fi

outdir=/g/data/ia39/npcp/data/${cmor_var}/${parent_model}/UQ-DES-CCAM-2105/raw/task-reference
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for inpath in "${infiles[@]}"; do
    infile=`basename ${inpath}`
    outfile=`echo ${infile} | sed s:AUS-20i:NPCP-20i:`
    outfile=`echo ${outfile} | sed s:CCAM:CCAM-2105:`
    outfile=`echo ${outfile} | sed s:historical_evaluation:evaluation_r1i1p1f1:`
    outfile=`echo ${outfile} | sed s:${var}:${cmor_var}:`
    command2="${python} ${script_dir}/preprocess.py ${inpath} ${var} ${outdir}/${outfile}"
    echo ${command2}    
    ${command2}
done

