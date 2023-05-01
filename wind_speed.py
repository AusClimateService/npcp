"""Command line program for calculating wind speed"""

import argparse

import numpy as np
import xarray as xr
import cmdline_provenance as cmdprov


def calc_wsp(u, v):
    """Calculate wind speed."""

    func = lambda u, v: np.sqrt(u**2 + v**2)

    return xr.apply_ufunc(func, u, v, keep_attrs=True)


def main(args):
    """Run the program."""
    
    eastward_ds = xr.open_dataset(args.eastward_wind_file)
    eastward_da = eastward_ds[args.eastward_wind_var]
    northward_ds = xr.open_dataset(args.northward_wind_file)
    northward_da = northward_ds[args.northward_wind_var]

    wsp_da = calc_wsp(eastward_da, northward_da)
    wsp_da.attrs['long_name'] = 'Daily Average 10m Wind Speed'
    wsp_da.attrs['standard_name'] = 'wind_speed'

    wsp_ds = wsp_da.to_dataset(name='wsp')
    wsp_ds.attrs = eastward_ds.attrs
    wsp_ds.attrs['history'] = cmdprov.new_log()
    wsp_ds.to_netcdf(args.wsp_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("eastward_wind_file", type=str, help="input eastward wind file")
    parser.add_argument("eastward_wind_var", type=str, help="input eastward wind variable")
    parser.add_argument("northward_wind_file", type=str, help="input northward wind file")
    parser.add_argument("northward_wind_var", type=str, help="input northward wind variable")
    parser.add_argument("wsp_file", type=str, help="output wind speed file")
    args = parser.parse_args()
    main(args)
