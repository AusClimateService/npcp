# NPCP bias correction intercomparison

This repository contains code and information relating to the
National Partnership for Climate Projections (NPCP) bias correction intercomparison project.

Input data used in the bias correction process (i.e. RCM outputs and observational data products) and
output data produced by the various bias correction methods used in the study
are being hosted by project ia39 on NCI. 

Researchers participating in the intercomparison project can request access to ia39 at:  
https://my.nci.org.au/mancini/project/ia39

## Input data

Input data is located at:  
```
/g/data/ia39/npcp/input_data/{variable}/{driving-model}/{rcm-model}/
```

Naming conventions follow CORDEX and can take the following values:  
`{variable}`  
- `pr`: precipitation
- `rsds`: surface downwelling shortwave
- `tasmax`: daily maximum surface air temperature
- `tasmin`: daily minimum surface air temperature
- `wsp`: surface (10m) wind speed
- TODO [humidty related variable still to be defined]

`{driving-model}`  
- `CSIRO-BOM-ACCESS-ESM1-5`: ACCESS-ESM1-5 CMIP6 submission
- `ECMWF-ERA5`: ERA5 reanalysis
- `observations`: Australian gridded observations

`{rcm-model}`  
- `BOM-BARPA-R`: Bureau of Meteorology Atmospheric Regional Projections for Australia
- `CSIRO-CCAM-2203`: Conformal Cubic Atmospheric Model (run by CSIRO)
- TODO [CCAM run by QLD Department of Environment and Science]
- TODO [WRF run by NSW Department of Planning and Environment]
- `AGCD`: Australian Gridded Climate Data
- `AWRA`: Australian Water Resource Assessment

Input data is provided for the training (1980-1999), assessment (2000-2019) and
projection (2080-2099; excluding observational data) periods. 
