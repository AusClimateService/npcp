#!/bin/bash
#
# Description: Re-run NPCP notebooks
#
# Usage: bash run_notebooks.sh
# 

notebooks=($(ls *.ipynb))
for notebook in "${notebooks[@]}"; do
#  sed -i -e 's/save_outfile=True/save_outfile=False/g' ${notebook}
#  sed -i -e 's/sys.path.append/#sys.path.append/g' ${notebook}
#  sed -i -e 's/Python \[conda env:analysis3-23.04\]/Python 3 (ipykernel)/g' ${notebook}
#  sed -i -e 's/Python \[conda env:analysis3-24.04\]/Python 3 (ipykernel)/g' ${notebook}
#  sed -i -e 's/Python \[conda env:analysis3-24.07\]/Python 3 (ipykernel)/g' ${notebook}
#  sed -i -e 's/Python \[conda env:analysis3\]/Python 3 (ipykernel)/g' ${notebook}
#  sed -i -e 's/conda-env-analysis3-23.04-py/python3/g' ${notebook}
#  sed -i -e 's/conda-env-analysis3-24.04-py/python3/g' ${notebook}
#  sed -i -e 's/conda-env-analysis3-24.07-py/python3/g' ${notebook}
#  sed -i -e 's/conda-env-analysis3-py/python3/g' ${notebook}
  qsub -v notebook=${notebook} notebook_job.sh
done

