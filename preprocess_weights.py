"""Command line program for AGCD precipitation weights processing.

Need to run https://github.com/climate-innovation-hub/agcd-masking/blob/master/agcd_weight_fraction.py first.

e.g. python preprocess_weights.py /g/data/ia39/npcp/data/pr/observations/AGCD/raw/task-reference/ob-fractions_r005_AGCD_v1-0-1_day_19800101-20191231.nc /g/data/ia39/npcp/data/pr/observations/AGCD/raw/task-reference/ob-fractions_NPCP-20i_AGCD_v1-0-1_day_19800101-20191231.nc
"""

import argparse

import numpy as np
import xcdat
import cmdline_provenance as cmdprov

import preprocess


def main(args):
    """Run the program."""

    input_ds = xcdat.open_mfdataset(args.infile)

    # NPCP-20i (0.2 degree) grid
    lats = np.round(np.arange(-44, -9.99, 0.2), decimals=1)
    lons = np.round(np.arange(112, 154.01, 0.2), decimals=1)
    npcp_grid = xcdat.create_grid(lats, lons)
   
    output_ds = input_ds.regridder.horizontal(
        'fraction',
        npcp_grid,
        tool='xesmf',
        method='conservative'
    )
    del output_ds['lat_bnds'].attrs['xcdat_bounds']
    del output_ds['lon_bnds'].attrs['xcdat_bounds']

    new_log = cmdprov.new_log(infile_logs={args.infile: input_ds.attrs['history']})
    output_ds.attrs['history'] = new_log 
    output_ds.to_netcdf(args.outfile)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("infile", type=str, help="input file")
    parser.add_argument("outfile", type=str, help="output file")
    args = parser.parse_args()
    main(args)
