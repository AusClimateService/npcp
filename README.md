# NPCP bias correction intercomparison

This repository contains code and information relating to the
National Partnership for Climate Projections (NPCP) bias correction intercomparison project.

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
/g/data/ia39/npcp/data/{variable}/{driving-model}/{downscaling-model}/{bias-correction-method}/
```

Naming conventions follow CORDEX wherever possible and can take the following values:  
- `{variable}`  
  - `pr`: precipitation
  - `rsds`: surface downwelling shortwave
  - `tasmax`: daily maximum surface air temperature
  - `tasmin`: daily minimum surface air temperature
  - `wsp`: surface (10m) wind speed
  - [humidity related variable still to be defined]
- `{driving-model}`  
  - `CSIRO-ACCESS-ESM1-5`: ACCESS-ESM1-5 CMIP6 submission
  - `ECMWF-ERA5`: ERA5 reanalysis
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
  - `ecdfm`: Equi-distant/ratio CDF matching (Damien Irving; [Li et al 2010](https://doi.org/10.1029/2009JD012882), [Wang and Chen 2013](https://doi.org/10.1002/asl2.454))
  - `qme`: Quantile Matching for Extremes (Andrew Dowdy & Justin Peter; [Dowdy 2020](https://doi.org/10.1071/ES20001))
  - `mrnbc`: Multivariate Recursive Nesting Bias Correction (Arpit Kapoor; [Mehrotra & Sharma 2015](https://doi.org/10.1016/j.jhydrol.2014.11.037))
  - `mbcn-bom`: N-Dimensional Multi-Variate Bias Correction, run by BoM using Python/xclim (Thi Lan Dao; [Cannon 2018](https://doi.org/10.1007/s00382-017-3580-6))
  - `mbcn-qld`: N-Dimensional Multi-Variate Bias Correction, run by UQ-DES using R (Ralph Trancoso; [Cannon 2018](https://doi.org/10.1007/s00382-017-3580-6))
  - `3dbc`: Three Dimensional Bias Correction (Fei Ji; [Mehrotra & Sharma 2019](https://doi.org/10.1029/2018WR023270))

### Data specifications (time periods, spatial grid, etc)

Daily timescale input data is provided for the
training (1980-1999), assessment (2000-2019) and projection (2080-2099; excluding observational data) periods.
Model data corresponds to the CMIP6 historical experiment from 1980-2014 and ssp370 for 2015 onwards. 

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

Bias corrected daily data is ultimately produced for the 2000-2019 and 2080-2099 time periods
on the common `NPCP-20i` grid.

### Input data availability

Unless otherwise stated, the traffic lights in the following table
summarise the availability of `pr`, `rsds`, `tasmax`, `tasmin` and `wsp` data.
An appropriate humidity related variable still to be defined and thus isn't covered by this table yet.

| driving model | downscaling model | training (1980-1999) | assessment (2000-2019) | projection (2080-2099) |
| ---           | ---               | :-:                  | :-:                    | :-:                    |
| Observations | AGCD or AWRA | :green_circle: | :green_circle: | N/A |
| ERA5 | BOM-BARPA | :green_circle: | :green_circle: | N/A |
| | CSIRO-CCAM | :green_circle: | :green_circle: | N/A |
| | UQ-DES-CCAM | :green_circle: | :green_circle: | N/A |
| | NARCLIM-WRF | Available Aug 2023 | Available Aug 2023 | N/A |
| ACCESS-ESM1-5 | BOM-BARPA | :green_circle: | :green_circle: | :green_circle: |
| | CSIRO-CCAM | :white_circle: | :white_circle: | :white_circle: |
| | UQ-DES-CCAM | :green_circle: | :green_circle: | :green_circle: |
| | NARCLIM-WRF | Available Aug 2023 | Available Aug 2023 | Available Aug 2023 |

