#!/bin/bash
#
# Description: Re-run NPCP notebooks
#
# Usage: bash run_notebooks.sh
# 

variables=(tasmin tasmax pr)

climatology_metrics=(mean_bias seasonal_cycle change_signal)
for metric in "${climatology_metrics[@]}"; do
  for var in "${variables[@]}"; do
    qsub -v notebook=${metric}_${var}.ipynb notebook_job.sh
done

variability_metrics=(interannual_variability multi-year_variability temp_autocorrelation_annual temp_autocorrelation_monthly)
for metric in "${variability_metrics[@]}"; do
  for var in "${variables[@]}"; do
    qsub -v notebook=${metric}_${var}.ipynb notebook_job.sh
done

extreme_metrics=(extreme_event percentiles)
for metric in "${extreme_metrics[@]}"; do
  for var in "${variables[@]}"; do
    qsub -v notebook=${metric}_${var}.ipynb notebook_job.sh
done

icclim_metrics=(R99pTOT R95pTOT R20mm R10mm FD WSDI CDSI wet_day_freq_annual PT_cross_correlation drought_intensity)
for metric in "${icclim_metrics[@]}"; do
    qsub -v notebook=${metric}.ipynb notebook_job.sh
done
