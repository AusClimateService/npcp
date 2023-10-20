"""Command line program for ERA5 data pre-processing."""

import glob
import argparse

import numpy as np
import xcdat
import cmdline_provenance as cmdprov

import preprocess


def main(args):
    """Run the program."""

    cmor_var = preprocess.var_to_cmor_name[args.var]
    outdir = f'/g/data/ia39/npcp/data/{cmor_var}/ECMWF-ERA5/GCM/raw/task-reference'
    new_log = cmdprov.new_log()

    lats = np.round(np.arange(-44, -9.99, 0.2), decimals=1)
    lons = np.round(np.arange(112, 154.01, 0.2), decimals=1)
    npcp_grid = xcdat.create_grid(lats, lons)
    
    for year in np.arange(1980, 2020):
        infiles = sorted(glob.glob(f'/g/data/rt52/era5/single-levels/reanalysis/{args.var}/{year}/*.nc'))
        if not infiles:
            raise OSError(f'No input files for variable {args.var} and year {year}')

        input_ds = xcdat.open_mfdataset(infiles)
        if args.var == 'mx2t':
            input_ds = input_ds.resample(time='D').max('time', keep_attrs=True)
        elif args.var == 'mn2t':
            input_ds = input_ds.resample(time='D').min('time', keep_attrs=True)
        elif args.var == 'tp':
            input_ds = input_ds.resample(time='D').sum('time', keep_attrs=True)
            assert input_ds[args.var].attrs['units'] == 'm'
            input_ds[args.var].attrs['units'] = 'm d-1'
        else:
            raise ValueError(f'Unsupported variable {args.var}')
       
        output_ds = input_ds.regridder.horizontal(
            args.var,
            npcp_grid,
            tool='xesmf',
            method='bilinear'
        )
        output_ds[args.var] = preprocess.convert_units(output_ds[args.var], preprocess.output_units[cmor_var])
        output_ds = preprocess.fix_metadata(output_ds, args.var)
        output_ds.attrs['history'] = new_log

        outpath = f'{outdir}/{cmor_var}_NPCP-20i_ECMWF-ERA5_evaluation_day_{year}0101-{year}1231.nc'
        print(outpath)
        output_ds.to_netcdf(outpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument(
        "var",
        type=str,
        choices=('mx2t', 'mn2t', 'tp'),
        help="input variable"
    )
    args = parser.parse_args()
    main(args)
