#!/bin/bash
#
# Description: Preprocess BoM BARPA data
#             

function usage {
    echo "USAGE: bash $0 variable experiment model"
    echo "   variable:   Variable to process (tasmax, tasmin, pr, rsds)"
    echo "   experiment: Experiment to process (evaluation, historical, ssp370)" 
    echo "   model:      Model to process (CSIRO-ACCESS-ESM1-5, EC-Earth-Consortium-EC-Earth3)"
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

var=$1
exp=$2
model=$3

if [ "${model}" == "CSIRO-ACCESS-ESM1-5" ]; then
    run=r6i1p1f1
else
    run=r1i1p1f1
fi

if [ "${exp}" == "evaluation" ]; then
    parent_model=ECMWF-ERA5
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/ECMWF-ERA5/evaluation/r1i1p1f1/BOM-BARPA-R/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_19{8,9}*.nc ${indir}/${var}_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "historical" ]; then
    parent_model=${model}
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/${model}/historical/${run}/BOM-BARPA-R/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-15_${model}_historical_${run}_BOM-BARPA-R_v1_day_19{6,7,8,9}*.nc ${indir}/${var}_AUS-15_${model}_historical_${run}_BOM-BARPA-R_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "ssp370" ]; then
    parent_model=${model}
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/${model}/ssp370/${run}/BOM-BARPA-R/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-15_${model}_ssp370_${run}_BOM-BARPA-R_v1_day_201*.nc ${indir}/${var}_AUS-15_${model}_ssp370_${run}_BOM-BARPA-R_v1_day_20{6,7,8,9}*.nc))
fi

outdir=/g/data/ia39/npcp/data/${var}/${parent_model}/BOM-BARPA-R/raw/task-reference
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for inpath in "${infiles[@]}"; do
    infile=`basename ${inpath}`
    outfile=`echo ${infile} | sed s:AUS-15:NPCP-20i:`
    outfile=`echo ${outfile} | sed s:12.nc:1231.nc:`
    outfile=`echo ${outfile} | sed s:01-:0101-:`
    command2="${python} ${script_dir}/preprocess.py ${inpath} ${var} ${outdir}/${outfile}"
    echo ${command2}    
    ${command2}
done

