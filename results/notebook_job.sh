#!/bin/bash
#PBS -P xv83
#PBS -q normal
#PBS -l walltime=2:00:00
#PBS -l mem=40GB
#PBS -l storage=gdata/xv83+gdata/ia39
#PBS -l wd
#PBS -v notebook

# Example:
#   qsub -v notebook=mean_bias_tasmax.ipynb notebook_job.sh


command="/g/data/xv83/dbi599/miniconda3/envs/npcp/bin/papermill ${notebook} ${notebook}"
echo ${command}
${command}
