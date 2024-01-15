#!/bin/bash
#
# Description: Preprocess CSIRO CCAM data
#             

function usage {
    echo "USAGE: bash $0 variable experiment model"
    echo "   variable:   Variable to process (tasmax, tasmin, pr, rsds)"
    echo "   experiment: Experiment to process (evaluation, historical, ssp370)"
    echo "   model:      Model to process (CSIRO-ACCESS-ESM1-5, EC-Earth-Consortium-EC-Earth3, NCAR-CESM2)" 
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

var=$1
exp=$2
model=$3

if [ "${model}" == "CSIRO-ACCESS-ESM1-5" ]; then
    model_short=access-esm1-5
    run=r6i1p1f1
    cordex_dir=CORDEX-CMIP6
elif [ "${model}" == "EC-Earth-Consortium-EC-Earth3" ]; then
    model_short=ec-earth3
    run=r1i1p1f1
    cordex_dir=CORDEX
elif [ "${model}" == "NCAR-CESM2" ]; then
    model_short=ncar-cesm2
    run=r11i1p1f1
    cordex_dir=CORDEX-CMIP6
fi

if [ "${exp}" == "evaluation" ]; then
    parent_model=ECMWF-ERA5
    indir=/g/data/xv83/mxt599/ccam_era5_evaluation_aus-10i_12km/drs_cordex/CORDEX/output/AUS-10i/CSIRO/ECMWF-ERA5/evaluation/r1i1p1f1/CSIRO-CCAM-2203/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-10i_ECMWF-ERA5_evaluation_r1i1p1f1_CSIRO-CCAM-2203_v1_day_19{8,9}*.nc ${indir}/${var}_AUS-10i_ECMWF-ERA5_evaluation_r1i1p1f1_CSIRO-CCAM-2203_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "historical" ]; then
    parent_model=${model}
    indir=/g/data/xv83/mxt599/ccam_${model_short}_historical_aus-10i_12km/drs_cordex/${cordex_dir}/output/AUS-10i/CSIRO/${model}/historical/${run}/CSIRO-CCAM-2203/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-10i_${model}_historical_${run}_CSIRO-CCAM-2203_v1_day_19{6,7,8,9}*.nc ${indir}/${var}_AUS-10i_${model}_historical_${run}_CSIRO-CCAM-2203_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "ssp370" ]; then
    parent_model=${model}
    indir=/g/data/xv83/mxt599/ccam_${model_short}_ssp370_aus-10i_12km/drs_cordex/${cordex_dir}/output/AUS-10i/CSIRO/${model}/ssp370/${run}/CSIRO-CCAM-2203/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-10i_${model}_ssp370_${run}_CSIRO-CCAM-2203_v1_day_201*.nc ${indir}/${var}_AUS-10i_${model}_ssp370_${run}_CSIRO-CCAM-2203_v1_day_20{6,7,8,9}*.nc))
fi

outdir=/g/data/ia39/npcp/data/${var}/${parent_model}/CSIRO-CCAM-2203/raw/task-reference
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for inpath in "${infiles[@]}"; do
    infile=`basename ${inpath}`
    outfile=`echo ${infile} | sed s:AUS-10i:NPCP-20i:`
    command2="${python} ${script_dir}/preprocess.py ${inpath} ${var} ${outdir}/${outfile}"
    echo ${command2}    
    ${command2}
done

