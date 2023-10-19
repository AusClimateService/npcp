"""Command line program for CMIP6 GCM pre-processing."""

import glob
import argparse

import numpy as np
import xcdat
import cmdline_provenance as cmdprov

import preprocess


def main(args):
    """Run the program."""
    
    hist_dir = f'/g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r6i1p1f1/day/{args.var}/gn/latest/' 
    hist_files = sorted(glob.glob(f'{hist_dir}/*.nc'))
    if not hist_files:
        raise OSError(f'No files at {hist_dir}')
    ssp_dir = f'/g/data/fs38/publications/CMIP6/ScenarioMIP/CSIRO/ACCESS-ESM1-5/ssp370/r6i1p1f1/day/{args.var}/gn/latest/' 
    ssp_files = sorted(glob.glob(f'{ssp_dir}/*.nc'))
    if not ssp_files:
        raise OSError(f'No files at {ssp_dir}')

    input_ds = xcdat.open_mfdataset(hist_files + ssp_files)
    input_ds_hist = input_ds.sel(time=slice('1960-01-01', '2019-12-31'))
    input_ds_proj = input_ds.sel(time=slice('2060-01-01', '2099-12-31'))

    # NPCP-20i (0.2 degree) grid
    lats = np.round(np.arange(-44, -9.99, 0.2), decimals=1)
    lons = np.round(np.arange(112, 154.01, 0.2), decimals=1)
    npcp_grid = xcdat.create_grid(lats, lons)
   
    ds_hist = input_ds_hist.regridder.horizontal(
        args.var,
        npcp_grid,
        tool='xesmf',
        method='bilinear'
    )
    ds_proj = input_ds_proj.regridder.horizontal(
        args.var,
        npcp_grid,
        tool='xesmf',
        method='bilinear'
    )

    ds_hist[args.var] = preprocess.convert_units(
        ds_hist[args.var], preprocess.output_units[args.var]
    )
    ds_proj[args.var] = preprocess.convert_units(
        ds_proj[args.var], preprocess.output_units[args.var]
    )

    new_log = cmdprov.new_log()
    ds_hist.attrs['history'] = new_log
    ds_proj.attrs['history'] = new_log
    
    outdir = f'/g/data/ia39/npcp/data/{args.var}/CSIRO-ACCESS-ESM1-5/GCM/raw/task-reference'
    hist_path = f'{outdir}/{args.var}_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_GCM_latest_day_19600101-20191231.nc'
    proj_path = f'{outdir}/{args.var}_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_GCM_latest_day_20600101-20991231.nc'
 
    ds_hist.to_netcdf(hist_path)
    ds_proj.to_netcdf(proj_path)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("var", type=str, help="input variable")
    args = parser.parse_args()
    main(args)
