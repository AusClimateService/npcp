# NPCP bias correction intercomparison

This repository contains code and information relating to the
National Partnership for Climate Projections (NPCP) bias correction intercomparison project.

## Results

See the draft [Phase 1 Report](https://github.com/AusClimateService/npcp/blob/master/reports/phase1/phase1_report.md)
to read a summary of the results so far.

For more detail than that covered in the report,
see the [`results/`](https://github.com/AusClimateService/npcp/tree/master/results) directory
for analysis notebooks that can be clicked on and viewed.

## Data

### Data access

Input data used in the bias correction process (i.e. model outputs and observational data products) and
output data produced by the various bias correction methods used in the study
are being hosted by project ia39 on NCI. 

Researchers participating in the intercomparison project can request access to ia39 at:  
https://my.nci.org.au/mancini/project/ia39

### Data reference syntax

The data is archived using the following directoruy structure:  
```
/g/data/ia39/npcp/data/{variable}/{driving-model}/{downscaling-model}/{bias-correction-method}/{task}
```

Naming conventions follow CORDEX wherever possible and can take the following values:  
- `{variable}`  
  - `pr`: precipitation
  - `rsds`: surface downwelling shortwave
  - `tasmax`: daily maximum surface air temperature
  - `tasmin`: daily minimum surface air temperature
  - `wsp`: surface (10m) wind speed
- `{driving-model}`  
  - `CSIRO-ACCESS-ESM1-5`: ACCESS-ESM1-5 CMIP6 submission
  - `EC-Earth-Consortium-EC-Earth3`: EC-Earth3 CMIP6 submission
  - `ECMWF-ERA5`: ERA5 reanalysis
  - `NCAR-CESM2`: CESM2 CMIP6 submission
  - `observations`: Australian gridded observations
- `{downscaling-model}`  
  - `BOM-BARPA-R`: Bureau of Meteorology Atmospheric Regional Projections for Australia (BARPA), run by BoM
  - `CSIRO-CCAM-2203`: Conformal Cubic Atmospheric Model (CCAM), run by CSIRO
  - `UQ-DES-CCAM-2105` Conformal Cubic Atmospheric Model (CCAM), run by UQ and the QLD Department of Environment and Science
  - `NARCLIM-WRF`: Weather Research and Forecasting (WRF) model, run by NARCLiM (NSW Australian Regional Climate Modelling)
  - `AGCD`: Australian Gridded Climate Data
  - `AWRA`: Australian Water Resource Assessment
- `{bias-correction-method}`  
  - `raw`: No bias correction applied (i.e. input data for bias correction)
  - `ecdfm`: Equi-distant/ratio CDF matching (Damien Irving; [method description](https://github.com/climate-innovation-hub/qqscale/blob/master/docs/method_ecdfm.md))
  - `qdc`: Quantile Delta Change (Damien Irving; [method description](https://github.com/climate-innovation-hub/qqscale/blob/master/docs/method_qdc.md))
  - `qme`: Quantile Matching for Extremes (Andrew Dowdy & Andrew Gammon; [Dowdy 2020](https://doi.org/10.1071/ES20001))
  - `mrnbc`: Multivariate Recursive Nesting Bias Correction (Arpit Kapoor; [Mehrotra & Sharma 2015](https://doi.org/10.1016/j.jhydrol.2014.11.037))
  - `mbcn`: N-Dimensional Multi-Variate Bias Correction (Thi Lan Dao; [Cannon 2018](https://doi.org/10.1007/s00382-017-3580-6))
  - `mbcp`: Multi-Variate Bias Correction (using Pearman correlation) (Ralph Trancoso; [Cannon 2016](https://doi.org/10.1175/JCLI-D-15-0679.1))
  - `3dbc`: Three Dimensional Bias Correction (Fei Ji; [Mehrotra & Sharma 2019](https://doi.org/10.1029/2018WR023270))
  - `tqm`: Triple Quantile Mapping
- `{task}`
  - `task-historical`: See "historical" bias correction task defined below
  - `task-projection`: See "projection" bias correction task defined below
  - `task-xvalidation`: See "cross validation" bias correction task defined below
  - `task-reference`: Reference data for bias correction tasks 

### Input data specifications (time periods, spatial grid, etc)

Daily timescale input data is provided for the 1960-2019 and 2060-2099 periods.
Model data corresponds to the CMIP6 historical experiment from 1960-2014 and ssp370 for 2015 onwards. 

Each input data file has been pre-processed (using the `preprocess.py` script in this repository)
in order to ensure common:
- File metadata (e.g. variable names)
- Data units
- Spatial grid (`NPCP-20i`) 

The `NPCP-20i` grid is a 0.2 degree lat/lon grid
with the same spatial extent as the AWRA data (44S-10S, 112E-154E),
which is the input dataset with the smallest spatial extent.
The `preprocess.py` script uses [xESMF](https://xesmf.readthedocs.io/en/latest/index.html) 
conservative regridding, which is the
[recommended method](https://xesmf.readthedocs.io/en/latest/notebooks/Compare_algorithms.html)
when upscaling from higher to lower horizontal resolution
(the original observational and downscaled model data is all higher resolution than 0.2 degrees).

### Input data availability

Unless otherwise stated, the traffic lights in the following table
summarise the availability of `pr`, `tasmax` and `tasmin` data.

| driving model | downscaling model | 1960-2019* | 2060-2099 |
| ---           | ---               | :-:       | :-:       |
| Observations | AGCD | :green_circle: | N/A |
| ERA5 | BOM-BARPA | :green_circle: | N/A |
| | CSIRO-CCAM | :green_circle: | N/A |
| | UQ-DES-CCAM | :green_circle: | N/A |
| | NARCLIM-WRF | :white_circle: | N/A |
| ACCESS-ESM1-5 | BOM-BARPA | :green_circle: | :green_circle: |
| | CSIRO-CCAM  | :green_circle: | :green_circle: |
| | UQ-DES-CCAM | :green_circle: | :green_circle: |
| | NARCLIM-WRF | :white_circle: | :white_circle: |
| CESM2 | BOM-BARPA | :green_circle: | :green_circle: |
| | CSIRO-CCAM  | :green_circle: | :green_circle: |
| EC-Earth3 | BOM-BARPA | :green_circle: | :green_circle: |
| | CSIRO-CCAM  | :green_circle: | :green_circle: |

*The ERA5 data is only available from 1979 onwards.  

## Bias correction tasks

Researchers who are interested in participting in the intercomparison project
(i.e. by applying their bias correction method/code)
are required to complete the tasks described below.

In order write your bias corrected data files to `/g/data/ia39/npcp/data/`
(following the data reference syntax described above),
you'll need to apply for access to the
NCI project ia39 writers group (ia39_w) at the following link:  
https://my.nci.org.au/mancini/project/ia39_w

### Phase 1

Phase 1 of the intercomparison will focus on daily timescale
`tasmax`, `tasmin` and `pr` data on the `NPCP-20i` grid.
For each variable and downscaling model there are 5 tasks to complete...

For the downscaled CMIP6 data (ACCESS-ESM1-5, CESM2 and EC-Earth3) the tasks are:  
- **Task 1 (Historical)**: Produce bias corrected data for the 1980-2019 period, using 1980-2019 as a training period.
- **Task 2 (Projection)**: Produce bias corrected data for the 2060-2099 period, using 1980-2019 as a training period.
- **Task 3 (Cross validation)**: Produce bias corrected data for the 1990-2019 period, using 1960-1989 as a training period.

For the downscaled ERA5 data the tasks are:  
- **Task 4 (Historical)**: Produce bias corrected data for the 1980-2019 period, using 1980-2019 as a training period.
- **Task 5 (Cross validation)**: Produce bias corrected data for the 2000-2019 period, using 1980-1999 as a training period.

An additional **documentation** task involves submitting a pull request to this repo
to add a summary of how your bias correction method works
and the details/location of code used to implement it to the [methods](https://github.com/AusClimateService/npcp/tree/master/methods) subdirectory. 

The training data for each variable is archived at `/g/data/ia39/npcp/data/`
following the data reference syntax described above.
For example, to complete tasks 1-3 for ACCESS-ESM1-5 data downscaled using BARPA
the observational and model data you'll need is at:
```
/g/data/ia39/npcp/data/pr/observations/AGCD/raw/task-reference/
/g/data/ia39/npcp/data/pr/CSIRO-ACCESS-ESM1-5/BOM-BARPA-R/raw/task-reference/
```

The model data requiring bias correction is the dynamically downscaled
BOM-BARPA-R, CSIRO-CCAM-2203, UQ-DES-CCAM-2105 and NARCLIM-WRF data
for the ECMWF-ERA5 and various CMIP6
(i.e. CSIRO-ACCESS-ESM1-5, NCAR-CESM2 and EC-Earth-Consortium-EC-Earth3) parent models.
Check the input data availability table above for an indication of
which combinations of downscaling and parent models are available.

Bias corrected data files written to `ia39` for each task should look something like the following examples:
1. `/g/data/ia39/npcp/data/tasmax/CSIRO-ACCESS-ESM1-5/UQ-DES-CCAM-2105/ecdfm/task-historical/tasmax_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_UQ-DES-CCAM-2105_v1_day_19800101-20191231_ecdfm-AGCD-19800101-20191231.nc`
2. `/g/data/ia39/npcp/data/tasmax/CSIRO-ACCESS-ESM1-5/UQ-DES-CCAM-2105/ecdfm/task-projection/tasmax_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_UQ-DES-CCAM-2105_v1_day_20600101-20991231_ecdfm-AGCD-19800101-20191231.nc`
3. `/g/data/ia39/npcp/data/tasmax/CSIRO-ACCESS-ESM1-5/UQ-DES-CCAM-2105/ecdfm/task-xvalidation/tasmax_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_UQ-DES-CCAM-2105_v1_day_19900101-20191231_ecdfm-AGCD-19600101-19891231.nc`
4. `/g/data/ia39/npcp/data/tasmax/ECMWF-ERA5/UQ-DES-CCAM-2105/ecdfm/task-historical/tasmax_NPCP-20i_ECMWF-ERA5_evaluation_r1i1p1f1_UQ-DES-CCAM-2105_v1_day_19800101-20191231_ecdfm-AGCD-19800101-20191231.nc`
5. `/g/data/ia39/npcp/data/tasmax/ECMWF-ERA5/UQ-DES-CCAM-2105/ecdfm/task-xvalidation/tasmax_NPCP-20i_ECMWF-ERA5_evaluation_r1i1p1f1_UQ-DES-CCAM-2105_v1_day_20000101-20191231_ecdfm-AGCD-19800101-19991231.nc`

The files have the same reference syntax as the input files with an additional field
after the final `_` indicating the bias correction method, observational dataset
and the start and end time for the training period.

### Phase 2

There might be an opportunity for a second phase of the intercomparison.
Ideas for that phase are being collected at https://github.com/AusClimateService/npcp/issues/3.
