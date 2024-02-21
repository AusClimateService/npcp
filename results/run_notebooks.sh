#!/bin/bash
#
# Description: Re-run NPCP notebooks
#
# Usage: bash run_notebooks.sh
# 

notebooks=($(ls *.ipynb))
for notebook in "${notebooks[@]}"; do
  qsub -v notebook=${notebook} notebook_job.sh
done

