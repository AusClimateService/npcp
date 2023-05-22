#!/bin/bash
#
# Description: Preprocess BoM BARPA wind data
#             

function usage {
    echo "USAGE: bash $0 experiment"
    echo "   experiment: Experiment to process (evaluation, historical, ssp370)" 
    exit 1
}

python=/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/python
script_dir=/g/data/ia39/npcp/code

exp=$1

if [ "${exp}" == "evaluation" ]; then
    parent_model=ECMWF-ERA5
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/ECMWF-ERA5/evaluation/r1i1p1f1/BOM-BARPA-R/v1/day
    ufiles=($(ls ${indir}/uas/uas_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_19{8,9}*.nc ${indir}/uas/uas_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_20{0,1}*.nc))
    vfiles=($(ls ${indir}/vas/vas_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_19{8,9}*.nc ${indir}/vas/vas_AUS-15_ECMWF-ERA5_evaluation_r1i1p1f1_BOM-BARPA-R_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "historical" ]; then
    parent_model=CSIRO-ACCESS-ESM1-5
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/CSIRO-ACCESS-ESM1-5/historical/r6i1p1f1/BOM-BARPA-R/v1/day
    ufiles=($(ls ${indir}/uas/uas_AUS-15_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_BOM-BARPA-R_v1_day_19{8,9}*.nc ${indir}/uas/uas_AUS-15_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_BOM-BARPA-R_v1_day_20{0,1}*.nc))
    vfiles=($(ls ${indir}/vas/vas_AUS-15_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_BOM-BARPA-R_v1_day_19{8,9}*.nc ${indir}/vas/vas_AUS-15_CSIRO-ACCESS-ESM1-5_historical_r6i1p1f1_BOM-BARPA-R_v1_day_20{0,1}*.nc))
elif [ "${exp}" == "ssp370" ]; then
    parent_model=CSIRO-ACCESS-ESM1-5
    indir=/g/data/ia39/australian-climate-service/release/CORDEX-CMIP6/output/AUS-15/BOM/CSIRO-ACCESS-ESM1-5/ssp370/r6i1p1f1/BOM-BARPA-R/v1/day
    ufiles=($(ls ${indir}/uas/uas_AUS-15_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_BOM-BARPA-R_v1_day_201*.nc ${indir}/uas/uas_AUS-15_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_BOM-BARPA-R_v1_day_20{8,9}*.nc))
    vfiles=($(ls ${indir}/vas/vas_AUS-15_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_BOM-BARPA-R_v1_day_201*.nc ${indir}/vas/vas_AUS-15_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_BOM-BARPA-R_v1_day_20{8,9}*.nc))
fi

outdir=/g/data/ia39/npcp/data/wsp/${parent_model}/BOM-BARPA-R/raw
command1="mkdir -p ${outdir}"
echo ${command1}
${command1}

for (( i=0; i<${#ufiles[*]}; ++i)); do
    upath="${ufiles[$i]}"
    vpath="${vfiles[$i]}"
    ufile=`basename ${upath}`
    temp_file=`echo ${ufile} | sed s:uas:wsp:`
    outfile=`echo ${temp_file} | sed s:AUS-15:NPCP-20i:`
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

