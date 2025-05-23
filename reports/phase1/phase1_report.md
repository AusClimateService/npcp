_This report is currently in draft form and is not complete._

# Phase 1 Report

[1. Introduction](#1-introduction)  
[2. Participating bias correction methods](#2-participating-bias-correction-methods)  
&ensp; [2.1. ECDFm](#21-ecdfm)  
&ensp; [2.2. QME](#22-qme)  
&ensp; [2.3. QDC](#23-qdc)  
&ensp; [2.4. MBCn](#24-mbcn)  
&ensp; [2.5. MRNBC](#25-mrnbc)  
[3. Data](#3-data)  
[4. Assessment](#4-assessment)  
[5. Results](#5-results)  
&ensp; [5.1. Temperature climatology](#51-temperature-climatology)  
&ensp; [5.2. Temperature variability](#52-temperature-variability)  
&ensp; [5.3. Temperature extremes](#53-temperature-extremes)  
&ensp; [5.4. Temperature trends](#54-temperature-trends)  
&ensp; [5.5. Precipitation climatology](#55-precipitation-climatology)  
&ensp; [5.6. Precipitation variability](#56-precipitation-variability)  
&ensp; [5.7. Precipitation daily distribution](#57-precipitation-daily-distribution)  
&ensp; [5.8. Precipitation extremes](#58-precipitation-extremes)  
&ensp; [5.9. Precipitation trends](#59-precipitation-trends)   
[6. Discussion](#6-discussion)  

## 1. Introduction

The [Climate Projections Roadmap for Australia](https://www.dcceew.gov.au/climate-change/publications/climate-projections-roadmap-for-australia)
has been developed by the Department of Climate Change, Energy, the Environment and Water
through a collaborative effort of the Australian climate projections community.
The roadmap is a shared vision statement of this new partnership,
called the National Partnership for Climate Projections (NPCP),
that aims to develop a consistent approach to deliver comparable,
robust, fit-for-purpose future climate information
to assess climate risks and inform adaptation planning.
The roadmap identifies a number of priority areas of collaboration for the NPCP,
including the delivery of national and regional downscaled climate projections.
This involves model selection, downscaling and bias correction,
as well as secondary and next-level analysis (e.g., hazard modelling).

When it comes to bias correction there is no "one size fits all" solution.
Over the years, various different methods have been applied in Australia.
Each of these methods has its own pros and cons and is suitable for different applications.
The associated bias correction software also varies
from code that was written for a specific research application (and sometimes subsequently abandoned)
to code that is actively maintained by research software engineers and regularly re-used.

In order to deliver the projections data described in the Climate Projections Roadmap for Australia,
there was a clear need to establish an NPCP bias correction intercomparison project
to identify the most appropriate bias correction methods.
The first major initiative listed by the Roadmap is the production of
national-scale climate projections by the Australian Climate Service (ACS).
The first phase of the bias correction intercomparison was therefore
designed to support that initiative.

It focused on bias correction methods that were available to the ACS at the time
(i.e. with existing functional software that was sufficiently well documented)
and applied those methods to a subset of the multi-scenario, multi-model ensemble
of regional climate model (RCM) simulations produced by NPCP partner organisations.
The RCMs were forced by data from a selection
(described by [Grose et al 2023](https://doi.org/10.1016/j.cliser.2023.100368))
of global climate models (GCMs) participating in the
Coupled Model Intercomparsion Project phase 6
(CMIP6; [Eyring et al 2016](https://doi.org/10.5194/gmd-9-1937-2016))
and their output will ultimately be submitted to the
Coordinated Regional Climate Downscaling Experiment (CORDEX; https://cordex.org/).
The resulting CORDEX-CMIP6 dataset will form the basis for the ACS national projections
as well as much of the climate projection information delivered by other NPCP members.
Since existing bias correction assessments produced for Australia
only provide information on some of the available bias correction methods
for specific contexts such as the Queensland spatial domain
([Zhang et al 2024](https://doi.org/10.1002/met.2204))
or for national hydrological modelling
([Vogel et al 2023](https://doi.org/10.1016/j.jhydrol.2023.129693),
[Peter et al 2024](https://doi.org/10.5194/gmd-17-2755-2024)),
there was a need to produce a general Australia-wide assessment
of all the available bias correction methods.

This report documents the results of this first phase
of the NPCP bias correction intercomparison project.
Notable features of the study include the use of cross-validation
(i.e. validation on a segment of the observational record
that was not used for calibrating the bias correction methods)
and comparison of bias correction applied to downscaled CMIP6 data
(i.e. CORDEX-CMIP6) with bias correction applied directly
to CMIP6 data and to downscaled reanalysis data.


## 2. Participating bias correction methods

The first step in a typical bias correction procedure involves
establishing a statistical relationship or transfer function
between model outputs and observations over a calibration (i.e. historical/training) time period.
The established transfer function is then applied to the target model data
(e.g. future model projections) in order to produce a "bias corrected" model timeseries.
There are a wide variety of transfer functions / bias correction methodologies out there,
ranging from relatively simple methods that take a single variable as input
to more sophisticated multivariate approaches.

Through a series of NPCP meetings and workshops on the topic of bias correction,
five methods were identified as being available for use by the ACS at the time:
- Equi-distant/ratio Cumulative Density Function (CDF) matching (ECDFm; univariate)
- Quantile Matching for Extremes (QME; univariate)
- Quantile Delta Change (QDC; univariate)
- N-Dimensional Multi-Variate Bias Correction (MBCn; multivariate)
- Multivariate Recursive Nesting Bias Correction (MRNBC; multivariate)

Some of these methods have been used previously in major projects undertaken
by the Commonwealth Scientific and Industrial Research Organisation (CSIRO)
and/or the Bureau of Meteorology (who are working together on the ACS).
For instance, the QDC method was used to produce application-ready climate data 
for the Climate Change in Australia project
([CSIRO and Bureau of Meteorology, 2015](https://www.climatechangeinaustralia.gov.au/en/communication-resources/reports/)),
while the QME and MRNBC methods were used to produce the latest
national hydrological projections for Australia
([Peter et al 2024](https://doi.org/10.5194/gmd-17-2755-2024)).
The QME method has also been used by the National Environmental Science Program
(e.g. [Dowdy et al 2019](https://doi.org/10.1038/s41598-019-46362-x))
and the Energy Sector Climate Information project
(e.g. [Dowdy et al 2021](https://www.climatechangeinaustralia.gov.au/media/ccia/2.2/cms_page_media/799/ESCI%20Technical%20Report%20-%20Standardised%20Method_1.pdf)).
In contrast, the ECDFm and MBCn methods have not yet been used in a
major CSIRO or Bureau of Meteorology project,
but there was interest in determining their potential for future projects.

The simplest bias correction procedure is a mean correction,
where the difference or ratio between the mean model and observed value
over the calibration period (i.e. the mean bias)
is removed (via subtraction or division) from the target model data
in order to produce the bias corrected model timeseries.
Quantile-based methods are a popular and slightly more sophisticated approach,
where the bias is calculated for a series of quantiles (instead of just the mean)
and then removed from the corresponding quantiles of the target model data.
The ECDFm method is essentially the most basic quantile-based bias correction method available.
The QME method is slightly more complicated in that it involves scaling the data
before matching the model and observations by quantile
to help resolve detail in the tails of the distribution (Dowdy 2023).
Prior to removing the quantile biases from the target model,
the bias correction factors at the extreme ends of the distribution are also modified by the QME method
to reduce the risk of overfitting or an excessive influence of very rare events.

While it is technically a "delta change" method as opposed to a "bias correction" method,
the QDC method was also included in the assessment.
In contrast to bias correction,
delta change approaches establish a transfer function between baseline and future model outputs
(e.g. from an historical model experiment and future climate emission scenario experiment)
and then apply that transfer function to observations from the same baseline period
to create a future timeseries.
The QDC method is conceptually very similar to ECDFm
and is essentially the most basic quantile-based delta change method available.

Unlike the univariate approaches, multivariate techniques tend to be iterative,
whereby a bias correction method is applied repeatedly until convergence is reached
(i.e. until the biases are no longer getting smaller)
The MBCn method involves repeatedly applying a multivariate orthogonal rotation to the data,
correcting the rotated data via empirical quantile mapping each time
([Cannon 2018](https://doi.org/10.1007/s00382-017-3580-6)).
The MRNBC method is also quantile-based and attempts to address biases in serial dependence
by correcting the data for biases in the mean, standard deviation and lag-0 and lag-1 auto and cross correlations
at multiple timescales (daily, monthly, seasonal and annual;
[Mehrotra and Sharma 2015](https://doi.org/10.1016/j.jhydrol.2014.11.037)).

Each of the methods is described in more detail below,
including details of the implementation choices and custom settings used in this particular study.

### 2.1. ECDFm

#### 2.1.1. Method

In _equidistant cumulative density function matching_
([Li et al, 2010](https://doi.org/10.1029/2009JD012882)),
the transfer function represents the distance (i.e. arithmetic difference)
between the observations and model for each quantile of the calibration period.
Those differences are then added to the target model data
according to the quantile each target data point represents over the target period.
For instance, if a target temperature of $25^{\circ}$ Celsius corresponds to the 0.5 quantile
(i.e. the median) in the target data,
the difference between the median value in the observations and calibration model data
is added to the target value in order to obtain the bias adjusted value.
The underlying assumption is that the distance between the model and observed quantiles
during the calibration period
also applies to the target period, hence the name *equidistant*.
The reference to *CDF matching* is clear from the mathematical representation of the method:

$$x_{m-adjust} = x_{m,p} + F_{o,h}^{-1}(F_{m,p}(x_{m,p})) - F_{m,h}^{-1}(F_{m,p}(x_{m,p}))$$

where $F$ is the CDF of either the observations ($o$) or model ($m$)
for a historical calibration period ($h$) or target period ($p$).
That means $F_{o,h}^{-1}$ and $F_{m,h}^{-1}$ are the quantile functions (inverse CDF)
corresponding to the observations and model respectively.
Returning to our target median value of $25^{\circ}$ (i.e. $x_{m,p} = 25$),
the corresponding CDF would return a value of 0.5 (i.e. $F_{m,p}(25) = 0.5$).
The difference between the observed ( $F_{o,h}^{-1}(0.5)$ )
and calibration model ( $F_{m,h}^{-1}(0.5)$ ) median values
would then be added to the target value of $25^{\circ}$ to get a bias corrected value.

For precipitation, multiplicative as opposed to additive bias correction is preferred
to avoid the possibility of getting bias corrected values less than zero.
In this case, *equiratio CDF matching* ([Wang and Chen, 2013](https://doi.org/10.1002/asl2.454)) is used:

$$x_{m-adjust} = x_{m,p} \times (F_{o,h}^{-1}(F_{m,p}(x_{m,p})) \div F_{m,h}^{-1}(F_{m,p}(x_{m,p})))$$

#### 2.1.2. Software (and implementation choices)

The code used to implement the ECDFm method is maintained by the CSIRO
and is openly available on GitHub (https://github.com/AusClimateService/qqscale)
with snapshots archived on Zenodo (https://doi.org/10.5281/zenodo.12523625).
The code basically implements the [bias adjustment and downscaling](https://xclim.readthedocs.io/en/stable/sdba.html)
functionality available in the widely used open-source xclim library
([Bourgault et al, 2023](https://doi.org/10.21105/joss.05415)).

There are a number of decisions to make when implementing the ECDFm method:
- _Time grouping_:
  It is common calculate bias correction adjustment factors for individual seasons or months separately
  in order to avoid conflating different times of the year
  (e.g. spring and autumn temperatures often occupy the same annual quantile space but may be biased in different ways).
  For the NPCP intercomparsion, adjustment factors were calculated for each month.
- _Quantiles_:
  The software allows the user to specify the number of quantiles for which to calculate an adjustment factor.
  We aimed to have approximately 10-15 data values between each quantile.
  For the NPCP bias correction tasks (that train on 30 or 40 years of daily data),
  that meant 100 quantiles for each month.
- _Adjustment factor smoothing_:
  The bias correction applied to each target data point is the closest value from the array of adjustment factors.
  In this case, it is a 12 (months) by 100 (quantiles) array
  and linear interpolation/smoothing is applied along the month axis.
  That means the adjustment factor for a target data point from 29 July that corresponds to the 0.651 quantile
  will be a linear combination of the adjustment factors for the nearest quantile (0.65) from both July and August.
- _Singularity stochastic removal_ ([Vrac et al, 2016](https://doi.org/10.1002/2015JD024511))
  is used to avoid divide by zero errors in the analysis of precipitation data.
  All near-zero values (i.e. values less than a very small positive threshold value)
  are set to a small random non-zero value prior to data processing,
  and then after the bias correction process is complete any values less than the threshold are set to zero.

### 2.2. QME

#### 2.2.1. Method

The _quantile matching for extremes_ ([Dowdy 2023](http://www.bom.gov.au/research/publications/researchreports/BRR-087.pdf))
method involves clipping model and observed data to a valid range
and then scaling that clipped data to an integer value between 0 and 500 (typically)
before applying a quantile-based transfer function.
This scaling can be thought of as binning the data
(in this case, a histogram with 500 bins).

The default options for the QME method were used in this study.
Valid values ranged from -30C to 60C for daily maximum temperature (tasmax),
-45C to 50C for daily minimum temperature (tasmin),
or 0mm to 1250mm for daily precipitation (pr),
and the following scaling functions were applied: 
- (tasmax + 35) * 5
- (tasmin + 55) * 5
- alog(pr + 1) * 70, where alog is the natural logarithm 

For example, a small value of 0.1mm would have a scaled value of alog(0.1 + 1) * 70 = 6.7,
which is rounded to an integer value / bin number of 7.
Similarly, the largest valid rainfall amount of 1250mm
would have a scaled value of alog(1250 + 1 ) * 70 = 499.2 (rounded to 499).

Once the clipping and scaling has been performed (i.e. once the data has been binned), 
the quantile corresponding to each of the populated bins in the scaled model data is determined.
The transfer function represents the arithmetic difference
between each model bin value and the value of the same quantile in the scaled observations.
Those differences are then added to all the model data points in each bin, respectively.
Similar to ECDFm, there is the option to apply the transfer function in a multiplicative
rather than additive fashion,
but additive is the default for all variables (even precipitation).

To avoid potential overfitting or an excessive influence of very rare events,
before the adjustment factor for each bin is applied to the model data
the factors for the N most extreme high and extreme low bins (the default value of N=3 was used here)
are replaced by the value from the neighbouring histogram bin
(i.e., the histogram bin that is one place less extreme than the third highest value in the sample).
The reference to _extremes_ in the name of the method is a nod to these tweaks
to the bias adjustments in the tails of the distribution. 

#### 2.2.2. Software (and implementation choices) 

The code used to implement the QME method is maintained by the Bureau of Meteorology
and is openly available on GitHub ([Gammon 2025](https://doi.org/10.5281/zenodo.14635627)).

There are a number of decisions to make when implementing the QME method.
All of the general features described above are customisable, including the
valid range for data clipping,
scaling formula,
number of histogram bins,
and the N most extreme bins.
There are also additional options as follows:
- _Time grouping_:
  Similar to ECDFm, it is common to apply the QME method to individual seasons or months separately.
  Each month’s histogram can also use data from adjacent months to increase the sample size
  (i.e., providing a 3-month moving average).
  Monthly time grouping was used for the NPCP intercomparsion and adjacent months were included for precipitation.
- _Adjustment factor smoothing_:
  A moving (boxcar) average can be applied over the range of bias correction values (i.e. for bins 0 to 500).
  For the intercomparison, a 21-point moving average was used.
- _Adjustment limits_:
  The software allows the user to specify a maximum adjustment/correction. 
  The default setting for precipitation (used in the intercomparison)
  is for a maximum increase of 50% applied to values greater than or equal to 10mm.
  For instance, a model daily precipitation value of 20mm could potentially be bias corrected
  up to a maximum value of 30mm.
  For precipitation, there is an additional default option (which can be overridden)
  that values of 0 rainfall be left unchanged (i.e. no bias correction is applied). 
- _Trend matching_: The long-term trend in the data can be removed prior to applying the bias correction
  and then added back in afterwards to ensure that the bias correction
  does not substantially alter the model simulated trend.
  This option was applied for the temperature data in the projection assessment task (described below).

### 2.3. QDC

#### 2.3.1 Method

One of the most widely used methods for producing climate projection data
is the so-called "delta change" approach.
Rather than use the data from a model simulation of the future climate directly,
the delta change approach calculates the relative change
between a future and historical modelled time period.
That relative change is then applied to observed data from the same historical time period
in order to produce a timeseries for the future period.

While the simplest application of the delta change approach
is to apply the mean model change to the observed data,
a popular alternative is to calculate and apply the delta changes on a quantile by quantile basis
(i.e. to adjust the variance of the distribution as opposed to just the mean).
For instance, if an observed historical temperature of $25^{\circ}$ Celsius
corresponds to the 0.5 quantile (i.e. the median) in the observed data,
the difference between the median value in the future and historical model data
is added to that observed historical temperature
in order to obtain the projected future temperature.

This *quantile delta change* (QDC) approach
([Olsson et al 2009](https://doi.org/10.1016/j.atmosres.2009.01.015);
[Willems & Vrac 2011](https://doi.org/10.1016/j.jhydrol.2011.02.030))
is expressed mathematically as follows:

$$x_{o,p} = x_{o,h} + F_{m,p}^{-1}(F_{o,h}(x_{o,h})) - F_{m,h}^{-1}(F_{o,h}(x_{o,h}))$$

where $F$ is the CDF of either the observations ($o$) or model ($m$)
for an historic ($h$) or future/projection period ($p$).
That means $F_{m,p}^{-1}$ and $F_{m,h}^{-1}$ are the quantile functions (inverse CDF)
corresponding to the future and historical model simulations, respectively.
Returning to our observed median value of $25^{\circ}$ (i.e. $x_{o,h} = 25$),
the corresponding CDF would return a value of 0.5 (i.e. $F_{o,h}(25) = 0.5$).
The difference between the future ( $F_{m,p}^{-1}(0.5)$ ) and
historical model ( $F_{m,h}^{-1}(0.5)$ ) median values
would then be added to the observed value of $25^{\circ}$ to get the projected future temperature.

For variables like precipitation, multiplicative as opposed to additive mapping is preferred
to avoid the possibility of producing future values less than zero:

$$x_{o,p} = x_{o,h} \times (F_{m,p}^{-1}(F_{o,h}(x_{o,h})) \div F_{m,h}^{-1}(F_{o,h}(x_{o,h})))$$

#### 2.3.2. Software (and implementation choices)

Since both methods are conceptually very similar,
the QDC method is implemented using the same software as the ECDFm method
([Irving 2024](https://doi.org/10.5281/zenodo.12523625)).
The same implementation choices are made regarding
time grouping, quantiles and singularity stochastic removal.

Model biases in the simulated precipitation distribution can cause the QDC method
to produce unrealistically large adjustment factors under special circumstances
(when there is an increasing rainfall trend and a dry model bias at marginal rainfall values;
[Irving and Macadam 2024](https://doi.org/10.25919/03by-9y62)).
Following [Irving and Macadam (2024)](https://doi.org/10.25919/03by-9y62),
for the intercomparison we limited the adjustment factors to 5.0 or less
when applying the QDC method to precipitation data.
A common multiplicative scaling factor was also applied to every data
point to make sure the annual mean percentage change
in the QDC precipitation data matched the model.


### 2.4. MBCn

#### 2.4.1. Method

The N-dimensional Multivariate Bias Correction
(MBCn; [Cannon 2018](https://doi.org/10.1007/s00382-017-3580-6)) method
was developed from the N-pdft image processing algorithm,
which maps from a continuous N-dimensional multivariate source distribution
to a continuous target distribution of the same dimension
(Pitié et al. [2005](https://doi.org/10.1109/ICCV.2005.166),
[2007](https://doi.org/10.1016/j.cviu.2006.11.011)).
A random orthogonal rotation is applied to the source distributions,
and quantile mapping is then applied to the rotated distributions.
The rotation enables linear combinations of each of the variables to be constructed
and quantile mapping is applied to these to enable a multivariate quantile mapping,
rather than univariate mapping of the marginal distributions.
These steps are combined in sequence and repeated
until the source multivariate distribution matches the target distributions.
In brief, the algorithm consists of three steps:
(a) apply an orthogonal rotation to the source and target data;
(b) correct the marginal distributions of the rotated source data via empirical quantile mapping; and
(c) apply the inverse rotation to the resulting data.

#### 2.4.2. Software (and implementation choices)

The code used to implement the MBCn method is maintained by the Bureau of Meteorology
and is openly available on GitHub ([Gammon and Dao, 2025](https://doi.org/10.5281/zenodo.14708960)).
There are two main "tuneable" parameters:
the number of quantiles used for applying the quantile matching to the reference data set
and the number of iterations performed for convergence.
These were set at 100 quantiles spaced evenly along [0, 1.0] in 0.01 increments
and 50 iterations for algorithm convergence.


### 2.5. MRNBC

#### 2.5.1. Method

The Multivariate Recursive Nested Bias Correction (MRNBC) method
corrects multiple variables at the same time and preserves their interdependence at multiple time scales.
It was progressively developed from the nested bias correction
(NBC; [Johnson and Sharma, 2012](https://doi.org/10.1029/2011WR010464))
and recursive nested bias correction techniques
(RNBC; [Mehrotra and Sharma, 2012](https://doi.org/10.1029/2012WR012446)).
The NBC corrects the distribution (mean and standard deviation) and
persistence (lag 1 autocorrelation coefficient)
at monthly, seasonal, and annual timescales using a standard autoregressive lag 1 model
([Srikanthan and Pegram, 2009](https://doi.org/10.1016/j.jhydrol.2009.03.025)).
The MRNBC method is a multivariate version of the above RNBC method.
It simultaneously corrects many model variables,
using a multivariate first-order autoregressive model at daily, monthly, quarterly, and annual timescales
to impart observed distributional and persistence properties of the input fields
([Mehrotra and Sharma, 2015](https://doi.org/10.1016/j.jhydrol.2014.11.037)).


#### 2.5.2. Software (and implementation choices)

The code used to implement the MRNBC method is maintained by the Bureau of Meteorology
and is openly available on GitHub ([Gammon and Kapoor, 2025](https://doi.org/10.5281/zenodo.14641854)).
All three analysis variables (precipitation, daily maximum temperature and daily minimum temperature)
were corrected simultaneously and the input data were clipped
to realistic physical bounds
(0 to 1000 mm/day for precipitation and -20 to 65C for temperature) prior to use.


## 3. Data

The subset of the CORDEX-CMIP6 dataset used for the intercomparison
was daily timescale temperature and precipitation data
from RCM simulations forced by the ACCESS-ESM1-5, CESM2 and EC-Earth3 models
for the historical (available for the years 1960-2014) and SSP-3.70 (2015-2100) experiments.
Three different GCMs were selected in order to sample a range of different model biases
and projected changes driving the RCM simulations.
For instance, the ACCESS-ESM1-5 model simulates a strong drying trend over Australia,
EC-Earth3 a strong increase in rainfall and
CESM2 a mix of increasing and decreasing rainfall trends across the country
(see [Grose et al 2023](https://doi.org/10.1016/j.cliser.2023.100368) for a detailed comparison). 
Similarly, data from three different RCM modelling groups was assessed
in order to sample a range of different RCM biases: 
a `BARPA-R` submission from the Bureau of Meteorology
([Howard et al 2024](https://doi.org/10.5194/gmd-17-731-2024),
[NCI 2024a](https://dx.doi.org/10.25914/gjzx-kr91))
produced by running the Bureau of Meteorology Atmospheric Regional Projections for Australia
(BARPA; [Su et al, 2022](http://www.bom.gov.au/research/publications/researchreports/BRR-069.pdf)) RCM,
a `CCAM-v2203-SN` submission from CSIRO
([Schroeter et al 2024](https://doi.org/10.1175/JAMC-D-24-0004.1),
[NCI 2024b](https://dx.doi.org/10.25914/rd73-4m38))
produced by running the Conformal Cubic Atmospheric Model
(CCAM; [McGregor and Dix 2008](https://doi.org/10.1007/978-0-387-49791-4_4)) RCM,
and a `CCAM-v2105` submission from the
University of Queensland and the Queensland Department of Energy and Climate
([Chapman et al, 2023](https://doi.org/10.1029/2023EF003548),
[NCI 2024c](https://dx.doi.org/10.25914/h0bx-be42))
produced by running a different configuration of CCAM.
Data from the New South Wales and Australian Regional Climate Modelling (NARCliM2.0)
submission to CORDEX-CMIP6 ([Di Virgilio et al, 2025](https://doi.org/10.5194/gmd-18-671-2025))
was not available at the time the intercomparison was conducted.
Each modelling group also ran their RCM with forcing from the
fifth generation European Centre for Medium-Range Weather Forecasts atmospheric reanalysis of the global climate
(ERA5; [Hersbach et al 2020](https://doi.org/10.1002/qj.3803)),
These downscaled ERA5 data are available for the years 1980-2020
and were also included in the intercomparison.
  
The daily timescale observational / reference data was version 1.0.1 of the
Australian Gridded Climate Data (AGCD) dataset
([Australian Bureau of Meteorology 2023](https://dx.doi.org/10.25914/hjqj-0x55),
[Evans et al 2020](http://www.bom.gov.au/research/publications/researchreports/BRR-041.pdf),
[Jones et al 2009](http://www.bom.gov.au/jshess/docs/2009/jones.pdf)).
In addition to daily maximum temperature, daily minimum temperature and daily precipitation,
the AGCD precipitation weights-data were used to mask land areas
where the precipitation values are unreliable due to weather station sparsity.
The weights indicate if observations (i.e. from weather stations)
influenced the analysed value in the AGCD dataset at every grid point and time step.
In some remote locations such as central Australia
there is little or no influence from observations at most or all time steps.
For precipitation-related metrics, we masked all grid points
that were not influenced by observations on 90% or more days over the 1960-2019 period.

The spatial resolution of the datasets ranged from 0.05 degrees of latitude and longitude for AGCD
to native model grids of approximately 0.10 to 0.15 degrees
for the BARPA-R, CCAM-v2203-SN and CCAM-v2105 models over the entire landmass of Australia. 
When comparing RCM data against observations of higher spatial resolution,
differences can arise not only from model bias/errors (which bias correction seeks to remove),
but also from the resolution (or scale) gap between the datasets.
The latter discrepancy — which is not a model error —
is known as the representativeness problem
([Zwiers et al 2013](https://doi.org/10.1007/978-94-007-6692-1_13)).
In order to avoid this problem in the intercomparison,
all data were regridded to the standard CORDEX grid that is used for making comparisons across models
(the 0.2 degree AUS-20i grid) using conservative remapping.

## 4. Assessment

Three tasks were completed for each of the bias correction methods (for each GCM/RCM combination):
- **Task 1 (Calibration)**: Produce bias corrected data for the 1980-2019 period, using 1980-2019 as a training period.
- **Task 2 (cross-validation)**: Produce bias corrected data for the 1990-2019 period, using 1960-1989 as a training period.
- **Task 3 (Projection)**: Produce bias corrected data for the 2060-2099 period, using 1980-2019 as a training period.

The rationale for the calibration task was to assess how well the bias correction methods perform
when they train on exactly the same data that they correct.
This is the most basic test of a bias correction method -
if a method cannot adequately correct the very data it was trained upon,
it is unlikely to be a useful method.
Conversely, if a method performs too well on the calibration task,
this might be an indication of over-fitting.
In other words,
validating a bias correction method on the same data that was used to calibrate the method
can give the impression that the method is more skilful than it actually is.

The rationale for the cross-validation task was to avoid the impression of artificial skill
by validating the bias correction methods on data that was not used for calibration.
It also allowed for the QDC method to be directly compared to the bias correction methods,
because on the calibration task the QDC method simply reproduces the original observations.
cross-validation is the gold standard for weather forecast verification,
because temporal synchronicity is expected between the forecast data and observations.
In the context of bias correction validation,
the value of cross-validation is limited by internal climate variability
(i.e. temporal synchronicity is not expected between the RCM data and observations;
[Maraun 2016](https://doi.org/10.1007/s40641-016-0050-x),
[Maraun et al 2017](https://doi.org/10.1038/nclimate3418)),
but it is still a widely used approach.
Performing both a calibration and cross-validation task
allowed for the comparison of results from two approaches with different, non-overlapping limitations
(i.e. artificial skill versus internal variability).
Given that downscaled data is only available back to 1980 for ERA5,
the cross-validation task for that dataset was modified to
produce bias corrected data for the 2000-2019 period using 1980-1999 as a training period.
Finally, the projection task was included to see if the bias correction methods
substantially modify the trend simulated by the models.
Trend modification is a problem for many bias correction methods
(e.g. [Zhang et al 2024](https://doi.org/10.1002/met.2204)).

Since the ensemble of GCMs selected for dynamical downscaling by NPCP partner organisations
is only a subset of the full CMIP6 ensemble,
some scientists and institutions participating in the NPCP
are also interested in applying bias correction directly to GCM output.
In order to better understand how GCM outputs that have been
dynamically downscaled and then bias corrected
compare to GCM outputs that are directly bias corrected,
the three assessment tasks were also completed on GCM output
using the ECDFm and QDC methods.

The data arising from each bias correction method was compared on a number of metrics
relating to the ability to capture the observed
climatology, variability, distribution (precipitation only), extremes and trends (Table 1).
To aid cross-study comparability,
we employed metrics that were used by previous bias correction assessments for Australia
(e.g. [Vogel et al 2023](https://doi.org/10.1016/j.jhydrol.2023.129693))
and/or selected from the widely used list of climate indices
recommended by the Expert Team on Climate Change Detection and Indices
(ETCCDI; e.g. [Alexander et al 2006](https://doi.org/10.1029/2005JD006290)).
The complete results for each variable and metric are available in a series of supplementary files
([GitHub link](https://github.com/AusClimateService/npcp/tree/master/reports/phase1/supplementary)
to be replaced with Zenodo DOI);
Table 1 indicates which supplementary files correspond to each metric.

| Category | Metric | Description | Supplementary file number/s |
| ---      | ---    | ---         | ---                |
| Climatology | Annual mean | Annual mean value. | 1-3 | 
| Climatology | Seasonal cycle | Mean value for each month. (Bias is calculated as the sum of the absolute value of the difference between the model and observed mean value for each month.) | 4-6 |
| Variability | Interannual variability (std(1yr)) | Standard deviation of the annual mean timeseries. | 7-9 |
| Variability (temperature) | Cold-spell duration index (CSDI) | Number of days where, in intervals of at least 6 consecutive days, daily Tmin < 10th percentile calculated for a 5-day window centred on each calendar day. | 10 |
| Variability (temperature) | Warm-spell duration index (WSDI) | Number of days where, in intervals of at least 6 consecutive days, daily Tmax > 90th percentile calculated for a 5-day window centred on each calendar day. | 11 |
| Daily distribution (precipitation) | Wet day frequency | Number of wet days (precipitation > 1mm) expressed as a fraction (%) of all days. | 12 |
| Daily distribution (precipitation) | R10mm, R20mm | Annual number of heavy precipitation days (precipitation ≥ 10 mm or 20mm). | 13, 14 |
| Daily distribution (precipitation) | R95pTOT, R99pTOT | Fraction of total annual precipitation that falls on very wet days (> 95th or 99th percentile). | 15, 16 |
| Extremes | 99th or 1st percentile (pct99, pct01) | 99th percentile of precipitation and daily maximum temperature. 1st percentile of daily minimum temperature. | 17-19 |
| Extremes | 1-in-10 year event | Percentile corresponding to an annual return interval of 10 years. | 20-22 |
| Trends | Change signal | Change in the climatological mean (future period minus the historical period). | 23-25 |

_Table 1: Metrics calculated at each grid point across Australia._


## 5. Results

To provide an overview of the performance of each bias correction method,
the results were condensed into summary tables
for the calibration (Figure 1) and cross-validation (Figure 2) tasks.
The tables show the bias in each metric averaged (using the mean absolute error/bias)
over all grid points and all CMIP6 GCM/RCM combinations (left column)
or all ERA5/RCM combinations (right column).

<p align="center">
    <img src="figures/hist_CMIP6-ERA5_summary.png" width=100% height=100%>
    <br>
    <em>
      Figure 1: Mean absolute error/bias across all grid points
      and all CMIP6 GCM/RCM (left column) or ERA5/RCM (right column) combinations
      for the calibration assessment task.
      The metrics corresponding to each row label are defined in Table 1.
      The number in each cell corresponds to the mean absolute error/bias
      (with units of Celsius, mm or days, depending on the metric),
      while the colour is that bias value expressed as a percentage change
      relative to the RCM value.
    </em>
</p>

<p align="center">
    <img src="figures/xval_CMIP6-ERA5_summary.png" width=100% height=100%>
    <br>
    <em>
      Figure 2: As per Figure 1 but for the cross-validation assessment task.
    </em>
</p>

After a bias correction method has been applied,
any residual bias on the calibration task
(i.e. an in-sample test where the training and target data are the same)
may be attributed to the method doing an imperfect job of quantifying and removing the model error.
Since historical CMIP6 simulations do not match the observed phasing of climate variability,
this "error" consists of both true model error and also a component related to
the mismatch in climate variability between the model and observations.
On the cross-validation task (an out-of-sample test),
the residual bias is typically larger than for the calibration task
because the variability mismatch makes the training less accurate and
the mismatch exists over the target time period as well.
Any time-varying component of the model error
can also lead to a higher residual bias on cross-validation,
as does the fact that the training period is finite and thus unable to sample
all possible weather/climate states that can occur (in both the model and observations)
outside of that period.

The ERA5-based data used in the intercomparison is unique
in the sense that its climate variability does match observations,
so it was presented separately in Figure 1 and 2.
The magnitude of the residual bias and the relative performance of each of the bias correction methods
was similar for both the ERA5 and CMIP6-based data,
which suggests that any mismatch in climate variability between the CMIP6 historical data
and observations was a minor factor
(one reason for using long 30-40 year periods for each task
was to reduce the influence of any climate variability mismatch).
We therefore focus the remaining presentation and discussion of results on the CMIP6-based data.

The results for each variable and assessment category are discussed in the sections below,
with maps showing the results for all grid points for a representative RCM/GCM combination as required.
See the supplementary materials for the map
for every metric and RCM/GCM combination that was assessed
([GitHub link](https://github.com/AusClimateService/npcp/tree/master/reports/phase1/supplementary)
to be replaced with Zenodo DOI).
In addition to showing the results for bias corrected RCM and GCM data,
the maps for the cross-validation task also show an "AGCD (training data)" result.
This result is derived from a simple replication of the AGCD training data
rather than applying a bias correction method.


### 5.1. Temperature climatology

When bias correction was applied to RCM output
following the calibration assessment task protocol
(i.e. with an overlapping training and correction period),
biases in the temperature annual mean and seasonal cycle
were typically almost completely eliminated (Figure 1a,b; e.g. Figure 3b,d,e,g).
The exception was the MBCn method,
which showed a consistent warm bias over the entire continent
for all GCM/RCM combinations (Figure 1a,b; e.g. Figure 3f).
Biases in the RCM output were also greatly reduced
(but not completely eliminated) on the cross-validation task.
The MBCn method was again the worst-performing on cross-validation,
but unlike for the calibration task it did reduce the RCM bias (Figure 2a,b; e.g. Figure 4i).
The residual bias after applying the ECDFm and QDC methods
to RCM and GCM outputs was very similar (e.g. Figures 3b,d and 4b,c,e,g).
This suggests that in the context of the temperature annual mean and seasonal cycle, 
it does not appear to make much difference
whether GCM data are dynamically downscaled or not prior to applying bias correction.

<p align="center">
    <img src="figures/tasmax_mean-bias_task-historical_CSIRO-ACCESS-ESM1-5_BOM-BARPA-R.png" width=60% height=60%>
    <br>
    <em>
      Figure 3: Bias in annual mean daily maximum temperature (relative to the AGCD dataset)
      for the "calibration" assessment task.
      Results are shown for the ACCESS-ESM1-5 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel c),
      and various bias correction methods applied to those
      GCM (panel b) and RCM (panels d-g) data.
      (MAE = mean absolute error.)
    </em>
</p>

<p align="center">
    <img src="figures/tasmax_mean-bias_task-xvalidation_CSIRO-ACCESS-ESM1-5_BOM-BARPA-R.png">
    <br>
    <em>
      Figure 4: Bias in annual mean daily maximum temperature (relative to the AGCD dataset)
      for the "cross-validation" assessment task.
      Results are shown for the ACCESS-ESM1-5 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel d),
      and various bias correction methods applied to those
      GCM (panels b and c) and RCM (panels e, f, g, i and j) data.
      A reference case where the AGCD training data (1960-1989)
      was simply duplicated for the assessment period (1990-2019) is also shown (panel h).
      (MAE = mean absolute error.)
    </em>
</p>

### 5.2. Temperature variability

GCM biases in interannual temperature variability were relatively small
and were not substantially modified by dynamical downscaling
or by most of the bias correction methods (Figure 1a,b and 2a,b; e.g. Figure 5).
The exception was the MRNBC method,
which unlike the other methods does attempt to explicitly correct for
biases in variability at multiple timescales (Section 2.5.1).
The MRNBC method was able to reduce biases in interannual temperature variability
on the calibration task (Figure 1a,b; e.g. Figure 5g)
but actually inflated those biases on cross-validation (Figure 2a,b; Figure 6j).
This may suggest a degree of overfitting by the MRNBC method.

<p align="center">
    <img src="figures/tasmax_interannual-variability-bias_task-historical_CSIRO-ACCESS-ESM1-5_UQ-DES-CCAM-2105.png" width=60% height=60%>
    <br>
    <em>
      Figure 5: Bias in the interannual variability of annual mean daily maximum temperature (relative to the AGCD dataset)
      for the "calibration" assessment task.
      Results are shown for the ACCESS-ESM1-5 GCM (panel a),
      the CCAM-v2105 RCM forced by that GCM (panel c),
      and various bias correction methods applied to those
      GCM (panel b) and RCM (panels d-g) data.
      (MAE = mean absolute error.)
    </em>
</p>

<p align="center">
    <img src="figures/tasmax_interannual-variability-bias_task-xvalidation_CSIRO-ACCESS-ESM1-5_UQ-DES-CCAM-2105.png">
    <br>
    <em>
      Figure 6: Bias in the interannual variability of annual mean daily maximum temperature (relative to the AGCD dataset)
      for the "cross-validation" assessment task.
      Results are shown for the ACCESS-ESM1-5 GCM (panel a),
      the CCAM-v2105 RCM forced by that GCM (panel d),
      and various bias correction methods applied to those
      GCM (panels b and c) and RCM (panels e, f, g, i and j) data.
      A reference case where the AGCD training data (1960-1989)
      was simply duplicated for the assessment period (1990-2019) is also shown (panel h).
      (MAE = mean absolute error.)
    </em>
</p>

With respect to sub-annual variability,
extended periods of persistent hot or cold weather were captured by the WSDI and CSDI, respectively.
These indices count the annual number of days that are part of a streak of six or more days
above the 90th percentile (WSDI) or below the 10th percentile (CSDI). 
Both indices show higher values in northern Australia
(where the weather tends to be more persistent / less variable from day to day)
and lower values in the south.

The GCM output tended to overestimate the WSDI and CSDI.
Dynamical downscaling acted to reduce this overestimation,
but bias correction of the RCM output made no difference (Figure 1a,b and 2a,b; e.g. Figure 7).
In contrast, the QDC method was associated with smaller biases than the RCM data.
This is presumably related to the fact that the QDC (delta change) method
perturbs the observed training data
(which did a good job of representing the WSDI and CSDI; e.g. Figure 7h),
whereas the bias correction methods act on the model data.

<p align="center">
    <img src="figures/tasmax_WSDI-bias_task-xvalidation_CSIRO-ACCESS-ESM1-5_BOM-BARPA-R.png">
    <br>
    <em>
      Figure 7: Bias in the WSDI (relative to the AGCD dataset)
      for the "cross-validation" assessment task.
      Results are shown for the ACCESS-ESM1-5 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel d),
      and various bias correction methods applied to those
      GCM (panels b and c) and RCM (panels e, f, g, i and j) data.
      A reference case where the AGCD training data (1960-1989)
      was simply duplicated for the assessment period (1990-2019) is also shown (panel h).
      (MAE = mean absolute error.)
    </em>
</p>

### 5.3. Temperature extremes

For extremes indices related to daily minimum temperature
(i.e. the 1-in-10-year low temperature and the 1st percentile),
RCM output was generally associated with smaller biases than corresponding GCM output
(Figure 1a and 2a).
In contrast, for daily maximum temperature
(i.e. the 1-in-10-year high temperature and the 99th percentile)
RCM output was only associated with smaller biases
for some RCM/GCM combinations but higher biases for others
(Figure 1b and 2b; e.g. Figure 8).

When bias correction was applied to RCM output,
the bias was greatly reduced on the calibration task (Figure 1a,b)
and also reduced (but to a lesser extent) on cross-validation (Figure 2a,b).
The MBCn method performed substantially worse than the other methods
on daily maximum temperature extremes for the calibration task (Figure 1b)
due to a warm bias across the entire continent (e.g. Figure 8f).
The MRNBC method performed similarly to ECDFm and QME over most of the continent,
but displayed substantial cool biases in minimum temperature extremes
over high elevation areas in central Tasmania and along the Great Dividing Range
(e.g. Figure 8g).

As with the temperature climatology metrics,
it did not appear to make much difference for these temperature extremes metrics
whether GCM data were dynamically downscaled or not prior to bias correction.

<p align="center">
    <img src="figures/tasmin_1-in-10yr-bias_task-historical_EC-Earth-Consortium-EC-Earth3_BOM-BARPA-R.png" width=60% height=60%>
    <br>
    <em>
      Figure 8: Bias in the 1-in-10 year low daily minimum temperature (relative to the AGCD dataset)
      for the "calibration" assessment task.
      Results are shown for the EC-Earth3 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel c),
      and various bias correction methods applied to those
      GCM (panel b) and RCM (panels d-g) data.
      (MAE = mean absolute error.)
    </em>
</p>

### 5.4. Temperature trends

With respect to the simulated projected trend in annual mean daily maximum or minimum temperature,
none of the methods substantially altered the model simulated trend (e.g. Figure 9).
In fact, dynamical downscaling modified the model trend much more than bias correction.

<p align="center">
    <img src="figures/tasmax_trend_task-projection_CSIRO-ACCESS-ESM1-5_BOM-BARPA-R.png" width=80% height=80%>
    <br>
    <em>
      Figure 9: Change in annual mean daily maximum temperature
      between 1980-2019 and 2060-2099 for the "projection" assessment task.
      Results are shown for the ACCESS-ESM1-5 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel b)
      and various bias correction methods applied to those RCM data (panels c-g).
    </em>
</p>

### 5.5. Precipitation climatology

Similar to the temperature results,
RCM output was generally (but not always) associated with smaller biases in
the annual precipitation climatology and seasonal cycle than corresponding GCM output,
but some bias still persisted and could have its own unique spatial characteristics.
When bias correction was applied to RCM output for the calibration task,
those biases were typically dramatically reduced,
especially for the MRNBC method (Figure 1c).
The exception was the MBCn method,
which showed a consistently large wet bias over the entire continent
for all GCM/RCM combinations.
Biases in the RCM output were also reduced on the cross-validation task,
but to a lesser extent than for the calibration task (Figure 2c; e.g. Figure 10).
The MRNBC method was no longer the stand out method,
but the MBCn method was again the worst-performing on cross-validation
due to a consistent wet bias (e.g. Figure 10i). 
On cross-validation,
biases also tended to be (but were not always) lower if the GCM data
were not dynamically downscaled prior to applying bias correction (e.g. Figure 10b,c).

<p align="center">
    <img src="figures/pr_mean-bias_task-xvalidation_CSIRO-ACCESS-ESM1-5_BOM-BARPA-R.png">
    <br>
    <em>
      Figure 10: Bias in annual mean precipitation (relative to the AGCD dataset)
      for the "cross-validation" assessment task.
      Results are shown for the ACCESS-ESM1-5 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel d),
      and various bias correction methods applied to those
      GCM (panels b and c) and RCM (panels e, f, g, i and j) data.
      A reference case where the AGCD training data (1960-1989)
      was simply duplicated for the assessment period (1990-2019) is also shown (panel h).
      Land areas where the AGCD data are unreliable due to weather station sparsity
      have been masked in white. 
      (MAE = mean absolute error.)
    </em>
</p>

### 5.6. Precipitation variability

RCM output was generally associated with similar or slightly reduced bias
in interannual precipitation variability relative to corresponding GCM output
(Figure 1c; e.g. Figure 11a,d and 12a,d).
When bias correction was applied to RCM output for the calibration task,
those biases were typically reduced, especially for the MRNBC method (Figure 1c).
The exception was the MBCn method,
which was consistently associated with larger biases than the RCM data.
On cross-validation, none of the bias correction methods
were consistently associated with lower biases than the RCM data (Figure 2c).
The MBCn method was associated with consistently increased biases,
while the ECDFm method differed greatly between GCMs;
it maintained or reduced the mean absolute bias for
dynamically downscaled ACCESS-ESM5-1 or EC-Earth3 data (e.g. Figure 11e),
but was associated with very large biases for CESM2 (e.g. Figure 12e).
In contrast to the bias correction methods,
the QDC method was associated with consistently lower biases on cross-validation
(Figure 2c; e.g. Figure 11g and 12g).
This is likely due to the fact that a simple replication of the training data clearly
outperformed all methods on cross-validation (e.g. Figure 11h and 12h),
and the QDC method effectively just applies a small perturbation to the training data.

<p align="center">
    <img src="figures/pr_interannual-variability-bias_task-xvalidation_EC-Earth-Consortium-EC-Earth3_CSIRO-CCAM-2203.png">
    <br>
    <em>
      Figure 11: Bias in the interannual variability of annual mean precipitation (relative to the AGCD dataset)
      for the "cross-validation" assessment task.
      Results are shown for the EC-Earth GCM (panel a),
      the CCAM-v2203-SN RCM forced by that GCM (panel d),
      and various bias correction methods applied to those
      GCM (panels b and c) and RCM (panels e, f, g, i and j) data.
      A reference case where the AGCD training data (1960-1989)
      was simply duplicated for the assessment period (1990-2019) is also shown (panel h).
      Land areas where the AGCD data are unreliable due to weather station sparsity
      have been masked in white.
      (MAE = mean absolute error.)
    </em>
</p>

<p align="center">
    <img src="figures/pr_interannual-variability-bias_task-xvalidation_NCAR-CESM2_BOM-BARPA-R.png">
    <br>
    <em>
      Figure 12: As per Figure 11 but for the CESM2 GCM and BARPA-R RCM.
    </em>
</p>

### 5.7. Precipitation daily distribution

The lower end of the daily precipitation distribution was assessed
by considering the wet day frequency (or, conversely, the annual number of relatively dry days),
while the upper end was captured by a series of metrics that used absolute (r10mm and r20mm)
or relative (R95pTOT and R99pTOT) thresholds.

Dynamical downscaling tended to reduce GCM bias
at the lower end of the precipitation distribution (wet day frequency and r10mm)
but increase GCM bias at the upper end (R95pTOT and R99pTOT) (Figure 1c and 2c).
Bias correction (and the QDC method) tended to reduce model bias,
with each method performing similarly. 
The exception was again the MBCn method,
for which biases either remained relatively unchanged or increased.

### 5.8. Precipitation extremes

The extreme precipitation results differed depending on the severity of the extreme.

For a less extreme metric like the 99th percentile
(i.e. an event that happens a few times a year),
dynamical downscaling was associated with a similar mean absolute bias
as the corresponding GCM output (Figure 1c).
With the exception of the MBCn method,
all methods reduced the bias in the RCM output on both the calibration (Figure 1c)
and (to a lesser extent) cross-validation tasks (Figure 2c).
It was difficult to separate the methods as they all performed similarly.

For a more extreme metric like the 1-in-10-year event,
dynamical downscaling was associated with a larger mean absolute bias than
the corresponding GCM output (Figure 1c; e.g. Figure 13a,d).
On the calibration task the various methods could be easily distinguished,
with the MRNBC method reducing the RCM bias to the greatest degree,
followed by the QME and then ECDFm methods (Figure 1c; e.g. Figure 13).
On cross-validation,
the QDC method outperformed all the bias correction methods (Figure 2c).
The MRNBC and QME methods performed similarly (a modest reduction in bias),
while the ECDFm method tended not to reduce the RCM bias.

<p align="center">
    <img src="figures/pr_1-in-10yr-bias_task-xvalidation_EC-Earth-Consortium-EC-Earth3_BOM-BARPA-R.png">
    <br>
    <em>
      Figure 13: Bias in the 1-in-10-year high daily precipitation (relative to the AGCD dataset)
      for the "cross-validation" assessment task.
      Results are shown for the EC-Earth3 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel d),
      and various bias correction methods applied to those
      GCM (panels b and c) and RCM (panels e, f, g, i and j) data.
      A reference case where the AGCD training data (1960-1989)
      was simply duplicated for the assessment period (1990-2019) is also shown (panel h).
      Land areas where the AGCD data are unreliable due to weather station sparsity
      have been masked in white.
      (MAE = mean absolute error.)
    </em>
</p>

### 5.9. Precipitation trends

Bias correction tended to slightly alter the model simulated rainfall trends (e.g. Figure 14).
The grid point differences in percentage change in annual mean precipitation from 1980-2019 to 2060-2099
between the original RCM data and the ECDFm, QME, MBCn and MRNBC bias corrected data
had a mean absolute error across all RCM/GCM combinations of 3.4%, 2.4%, 9.5% and 4.2%, respectively.
For all RCM/GCM combinations, dynamical downscaling modified the model trend more than bias correction.

<p align="center">
    <img src="figures/pr_trend_task-projection_NCAR-CESM2_BOM-BARPA-R.png" width=90% height=90%>
    <br>
    <em>
      Figure 14: Change in annual mean precipitation
      between 1980-2019 and 2060-2099 for the "projection" assessment task.
      Results are shown for the CESM2 GCM (panel a),
      the BARPA-R RCM forced by that GCM (panel b)
      and various bias correction methods applied to those RCM data (panels c-g).
    </em>
</p>


## 6. Discussion

The first major initiative on the Climate Projections Roadmap for Australia
is the production of next-generation national-scale climate projections.
A primary data source for those projections is the CMIP6 ensemble,
but that dataset does not provide regional-scale or unbiased information.
For many applications (e.g. regional impact modelling, metrics that involve absolute thresholds),
that means some form of downscaling and bias correction is required.
A number of modelling groups have used RCMs to dynamically downscale CMIP6 data over Australia,
but the resulting CORDEX-CMIP6 dataset still has substantial biases
(partly inherited from the driving GCMs).
In order to help select the most appropriate methods for bias correction,
the NPCP established a bias correction intercomparison project.
This paper presents the results of the first phase of that intercomparison,
which focused on assessing the methods available to the ACS
for producing a general-purpose bias corrected version of the CORDEX-CMIP6 Australasia dataset.

The intercomparison involved validating the various bias correction methods
against the same observational data that was used to calibrate the methods (the "calibration" task)
and then against different observational data
by calibrating on the first half of the observational record
and then validating on the second half (the "cross-validation" task).
These two validation tasks each have their have own limitations,
so results that were consistent across both were considered more robust. 
Indeed, aside from an obvious difference in the magnitude of the residual bias after bias correction
(cross-validation is associated with higher biases)
the relative performance of the bias correction methods
and whether or not they provided any substantial benefit
was mostly similar between the two tasks.
That meant a clear hierarchy between the methods could be identified.

The best-performing bias correction methods were QME and MRNBC
for univariate and multivariate approaches, respectively.
Both methods were effective in reducing model bias for most but not quite all of the assessment metrics.
To understand why bias correction is not equally effective on all metrics,
it is useful to consider the climate system as a multivariate distribution
having marginal, temporal, spatial, and inter-variable aspects
([Maraun et al 2015](https://doi.org/10.1002/2014EF000259).
As non-parametric quantile-based univariate methods applied to each month separately,
the QME and ECDFm methods directly modify the marginal aspects of the distribution
(e.g., the univariate mean and variance) and also some temporal aspects
(e.g., amplitude of the seasonal cycle, number of threshold exceedances),
but do not directly modify some other temporal aspects
(e.g., weather sequencing, interannual or multi-year variability)
or any spatial or inter-variable aspects.
It was therefore not surprising that the QME and ECDFm methods had little impact
on model bias for the metrics relating to weather sequencing (CSDI and WSDI),
which relate to temporal aspects that are not likely to be substantially modified by those methods. 

The MRNBC method is specifically designed to modify temporal variability,
so its performance on the interannual variability metric
was particularly interesting.
It tended to reduce model bias on the calibration task
but increased it on the cross-validation task,
suggesting a degree of overfitting by the method.
(Due to internal climate variability,
to be more certain of an overfitting problem the
cross-validation would need to be repeated for multiple different
calibration and assessment periods,
which was beyond the scope of this study.)
The impact of the multivariate MRNBC method on the inter-variable aspects of the distribution
was difficult to assess with the simple metrics employed in our analysis.
For instance, bias in the cross-correlation between the monthly mean anomaly timeseries
of precipitation and daily maximum temperature
(a metric we ultimately decided not to include in the paper)
showed little change with dynamical downscaling or bias correction of any kind.
Having said that,
when multiple variables are bias corrected for input into a hydrological model
(i.e. a much more sophisticated inter-variable assessment)
it has been shown on assessments similar to our calibration task 
that the MRNBC method outperforms univariate alternatives over Australia
when the hydrological model outputs are compared to observations
([Vogel et al 2023](https://doi.org/10.1016/j.jhydrol.2023.129693)),
noting that cross-validation was not used in that study.
 
For most assessment metrics, the ECDFm method performed similarly to QME and MRNBC.
An exception was the metrics relating to precipitation variability,
for which the ECDFm method ranged from reducing to dramatically increasing the model bias
depending on which RCM/GCM combination was assessed.
The other exception was very extreme precipitation (i.e. the 1-in-10-year event),
for which ECDFm tended to have little effect on the model bias.
In contrast, the QME method (i.e. the other option for univariate bias correction)
essentially "did no harm" in the sense that it did not dramatically inflate the model bias
for particular metrics and RCM/GCM combinations.
A detailed analysis of why the QME and ECDFm methods performed differently in
specific instances despite some methodological similarities
was beyond the scope of this paper,
but we hypothesise that it could be related to the data transform that the QME method
implements before any quantile matching is performed,
as well as the modifications it makes to adjustment factors
at the extreme ends of the distribution.

The QDC method compared very favourably to the bias correction methods.
On any given metric it generally performed as well as the best performing bias correction method,
and much better on metrics like CSDI and WSDI where weather sequencing is important.
The method essentially represents a (relatively small) perturbation to the observational record,
so it naturally produces very realistic output.
There are some practical limitations to using the QDC method
(e.g. you can generally only produce 20-40 year time slices as opposed to a continuous timeseries
and you are stuck with the observed sequence of weather events;
[Irving and Macadam 2024](https://doi.org/10.25919/03by-9y62)),
but if those are not a barrier then it appears to be a good option
for producing projections data.

The MBCn method was clearly the worst performing method,
dramatically increasing the bias on a number of metrics.
Given that it is a widely used method that has been applied in many different contexts
without displaying such dramatically poor performance
(including in Australia; [Weeding et al 2024](https://doi.org/10.1007/s00484-024-02622-8)),
future work is for the authors to investigate how the method was implemented
including whether performance can be improved by modifying the various input parameters
(e.g. limits on the number of iterations to convergence, the number of quantiles).

A final observation from this first phase of the NPCP bias correction intercomparison
is that directly bias correcting GCM data
(i.e. without using an RCM to dynamically downscale the GCM data first)
tended to result in similar (for temperature) or better (for precipitation)
bias reductions for most of the metrics that we assessed.
This result is consistent with a previous analysis of precipitation
across the United Kingdom
([Eden et al 2014](https://doi.org/10.1002/2014JD021732)).
An exception was the metrics related to weather sequencing (the CSDI and WSDI),
which were improved by dynamical downscaling but not bias correction.
It could therefore be the case that metrics relating to
temporal, spatial or inter-variable aspects of the climate system that we did not assess
would highlight the benefits of dynamical downscaling prior to bias correction.

On the basis of these results,
the ACS went ahead and bias corrected
the entire CORDEX-CMIP6 Australasia archive (for selected variables)
using the QME and MRBNC methods ([NCI 2025](https://doi.org/10.25914/xeca-pw53)).
A QDC-CMIP6 dataset was also produced by applying the QDC method to daily GCM data
for selected CMIP6 models and variables
([Irving and Macadam 2024](https://doi.org/10.25919/03by-9y62); dataset DOI to come).
Future phases of the NPCP bias correction intercomparison may focus on topics such as
bias correction of sub-daily timescale data.
