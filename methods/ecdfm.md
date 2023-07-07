# Equi-distant/ratio CDF matching (ECDFm)

## Method

This method of quantile mapping has been referred to in the literature as 
*equidistant CDF matching* (EDCDFm; in the case of additive bias correction; [Li et al, 2010](https://doi.org/10.1029/2009JD012882)) or
*equiratio CDF matching* (EQCDFm; in the case of multiplicative bias correction; [Wang and Chen, 2013](https://doi.org/10.1002/asl2.454)).

Following the notation in [Cannon et al. (2015)](https://doi.org/10.1175/JCLI-D-14-00754.1),
let $F_{m,p}$, $F_{m,h}$ and $F_{o,h}$ denote, respectively,
the CDF from model *m* in future period *p* (or actually any model period to be bias corrected),
the CDF from model *m* in the historical period *h* and
the CDF from the reference data *o* in the historical period *h*.
Let $x_{m,p}$ be a modelled future value at time *t*,
and let $x_{m,p}^a$ be the associated adjusted value for the same future date.
In addition, let $τ_{m,p}$ denote the non-exceedance probability associated with $x_{m,p}$,
such that $τ_{m,p} = F_{m,p}[x_{m,p}].F^{−1}$ represents the inverse CDF.
The adjusted value is defined as follows for an additive variable:
$$x_{m,p}^a(t) = x_{m,p}(t) + (F_{o,h}^{-1}[τ_{m,p}] - F_{m,h}^{-1}[τ_{m,p}])$$
In other words, the adjusted value is the original value plus the bias.
For a multiplicative variable such as precipitation,
the right hand side in those equations becomes multiplicative rather than additive.

## Code

### Location

https://github.com/climate-innovation-hub/qqscale

### Performance

TODO.
