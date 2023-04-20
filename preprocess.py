"""Command line program for NPCP intercomparison data pre-processing."""

import argparse

import numpy as np
import xcdat
import xclim
import cmdline_provenance as cmdprov


var_names = {
    'tmax': 'tasmax',
    'tmin': 'tasmin'
    'precip': 'pr',
}

var_attrs = {
    'tasmax': {
        'long_name': 'Daily Maximum Near-Surface Air Temperature',
        'standard_name': 'air_temperature',
        'units': 'K',
    },
    'tasmin': {
        'long_name': 'Daily Minimum Near-Surface Air Temperature',
        'standard_name': 'air_temperature',
        'units': 'K',
    },
}

output_units = {
    'tasmax': 'degC',
    'tasmin': 'degC',
    'pr': 'mm d-1',
}


def convert_units(da, target_units):
    """Convert units.

    Parameters
    ----------
    da : xarray DataArray
        Input array containing a units attribute
    target_units : str
        Units to convert to

    Returns
    -------
    da : xarray DataArray
       Array with converted units
    """

    xclim_unit_check = {
        "deg_k": "degK",
        "kg/m2/s": "kg m-2 s-1",
    }

    if da.attrs["units"] in xclim_unit_check:
        da.attrs["units"] = xclim_unit_check[da.units]

    try:
        da = xclim.units.convert_units_to(da, target_units)
    except Exception as e:
        in_precip_kg = da.attrs["units"] == "kg m-2 s-1"
        out_precip_mm = target_units in ["mm d-1", "mm day-1"]
        if in_precip_kg and out_precip_mm:
            da = da * 86400
            da.attrs["units"] = target_units
        else:
            raise e

    return da


def fix_metadata(ds, var):
    "Apply metadata fixes."""

    if var in var_name_fixes:
        cmor_var = var_names[var]
        ds = ds.rename({var: cmor_var})
    else:
        cmor_var = var

    ds[cmor_var].attrs = var_attrs[cmor_var]

    return ds, cmor_var
    

def main(args):
    """Run the program."""
    
    input_ds = xcdat.open_dataset(args.infile)

    # 20i (0.2 degree) grid with AWRA bounds
    lats = np.arange(-44, -9.99, 0.2)
    lons = np.arange(112, 154.01, 0.2)
    npcp_grid = xcdat.create_grid(lats, lons)
    
    output_ds = input_ds.regridder.horizontal(
        args.var,
        npcp_grid,
        tool='xesmf',
        method='conservative'
    )
    output_ds, cmor_var = fix_metadata(output_ds, args.var)
    output_ds[cmor_var] = convert_units(output_ds[cmor_var], output_units[cmor_var])
    output_ds.attrs['geospatial_lat_min'] = lats[0]
    output_ds.attrs['geospatial_lat_max'] = lats[-1]
    output_ds.attrs['geospatial_lon_min'] = lons[0]
    output_ds.attrs['geospatial_lon_max'] = lons[-1]
    output_ds.attrs['history'] = cmdprov.new_log()
    output_ds.to_netcdf(args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("infile", type=str, help="input file")
    parser.add_argument("var", type=str, help="input variable")
    parser.add_argument("outfile", type=str, help="output file")

    args = parser.parse_args()
    main(args)
