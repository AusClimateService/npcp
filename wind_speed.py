"""Command line program for calculating wind speed"""

import argparse

import xarray as xr
import cmdline_provenance as cmdprov


def main(args):
    """Run the program."""
    
    eastward_ds = xr.open_dataset(args.eastward_wind_file)
    eastward_da = eastward_ds[args.eastward_wind_var]
    northward_ds = xr.open_dataset(args.northward_wind_file)
    northward_da = northward_ds[args.northward_wind_var]
    wsp_da = xr.ufuncs.sqrt(eastward_da ** 2 + northward_da ** 2) 
    wsp_ds = wsp_da.to_dataset()
    ## TODO: Fix attributes
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
