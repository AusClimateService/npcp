# Equi-distant/ratio CDF matching (ECDFm)

## Method

The first step in any bias correction prodcedure involves establishing a statistical relationship or transfer function between model outputs and observations over a reference (i.e. historical/training) time period.
The established transfer function is then applied to the target model data (e.g. future model projections) in order to produce a "bias corrected" model time series.

Many bias correction procudures are quantile based,
meaning the model data are corrected on a quantile by quantile basis.
In *equidistant cumulative density function matching* (EDCFm; [Li et al, 2010](https://doi.org/10.1029/2009JD012882)),
the transfer function represents the distance (i.e. arithmetic difference)
between the observations and model for each quantile of the training period.
Those differences are then added to the target model data
according to the quantile each target data point represents over the target period.
For instance, if a target value of 25 degrees Celsius corresponds to the 0.1 quantile in the target data,
the difference between the 0.1 quantile value in the observations and reference model data
is added to the target value in order to obtain the bias adjusted value.
The underlying assumption is that the distance between the model and observed quantiles during the training period
also applies to the target period, hence the name "equidistant."

The reference to "CDF matching" is clear from the mathematical representation of the method:
$$x_{m-adjust} = x_{m,p} + F_{o,h}^{-1}(F_{m,p}(x_{m,p})) - F_{m,h}^{-1}(F_{m,p}(x_{m,p}))$$

where $F$ is the CDF of either the observations ($o$) or model ($m$) for a historic training period ($h$) or target period ($p$).
That means $F_{o,h}^{-1}$ and $F_{m,h}^{-1}$ are the quantile functions (inverse CDF) corresponding to the observations and model respectively.
Given that a quantile of a random variable is a real number $x_p$ satisfying $F(x_p) = p$ ($p$ is probability in this case),
a quantile function expresses the quantile values as a function of probabilities.

For variables like precipitation, multiplicative as opposed to additive bias correction is preferred
to avoid the possibility of getting bias corrected values less than zero.
In this case, *equiratio CDF matching* (EQCDFm; [Wang and Chen, 2013](https://doi.org/10.1002/asl2.454))
is used:

$$x_{m-adjust} = x_{m,p} \times (F_{o,h}^{-1}(F_{m,p}(x_{m,p})) \div F_{m,h}^{-1}(F_{m,p}(x_{m,p})))$$

## Code

### Location

https://github.com/climate-innovation-hub/qqscale

### Performance

TODO.
