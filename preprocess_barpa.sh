#!/bin/bash
#
# Description: Preprocess BoM BARPA data
#             

function usage {
    echo "USAGE: bash $0 variable experiment"
    echo "   variable:   Variable to process (tasmax, tasmin, pr, rsds)"
    echo "   experiment: Experiment to process (evaluation, historical)" 
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

var=$1
exp=$2

if [ "${exp}" == "evaluation" ]; then
    parent_model=ECMWF-ERA5
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/ECMWF-ERA5/evaluation/r1i1p1f1/BOM-BARPA-R/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_19{8,9}*.nc ${indir}/${var}_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "historical" ]; then
    parent_model=CSIRO-ACCESS-ESM1-5
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/CSIRO-ACCESS-ESM1-5/historical/r6i1p1f1/BOM-BARPA-R/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-15_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_BOM-BARPA-R_v1_day_19{8,9}*.nc ${indir}/${var}_AUS-15_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_BOM-BARPA-R_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "ssp370" ]; then
    parent_model=CSIRO-ACCESS-ESM1-5
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/CSIRO-ACCESS-ESM1-5/ssp370/r6i1p1f1/BOM-BARPA-R/v1/day/${var}
    infiles=($(ls ${indir}/${var}_AUS-15_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_BOM-BARPA-R_v1_day_201*.nc ${indir}/${var}_AUS-15_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_BOM-BARPA-R_v1_day_20{8,9}*.nc))
fi

outdir=/g/data/ia39/npcp/data/${var}/${parent_model}/BOM-BARPA-R/raw
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for inpath in "${infiles[@]}"; do
    infile=`basename ${inpath}`
    outfile=`echo ${infile} | sed s:AUS-15:NPCP-20i:`
    command2="${python} ${script_dir}/preprocess.py ${inpath} ${var} ${outdir}/${outfile}"
    echo ${command2}    
    ${command2}
done

