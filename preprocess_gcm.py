"""Command line program for CMIP6 GCM pre-processing."""

import glob
import argparse

import numpy as np
import xcdat
import cmdline_provenance as cmdprov

import preprocess


def main(args):
    """Run the program."""
    
    if args.cordex_model == 'CSIRO-ACCESS-ESM1-5':
        institution = 'CSIRO'
        model = 'ACCESS-ESM1-5'
        run = 'r6i1p1f1'
        grid = 'gn'
        hist_version = 'latest'
        ssp_version = 'latest'
        cmip_dir = 'fs38/publications'
    elif args.cordex_model == 'EC-Earth-Consortium-EC-Earth3':
        institution = 'EC-Earth-Consortium'
        model = 'EC-Earth3'
        run = 'r1i1p1f1'
        grid = 'gr'
        hist_version = 'v20200310'
        ssp_version = 'v20200310'
        cmip_dir = 'oi10/replicas'
    elif args.cordex_model == 'NCAR-CESM2':
        institution = 'NCAR'
        model = 'CESM2'
        run = 'r11i1p1f1'
        grid = 'gn'
        hist_version = 'v20190514'
        ssp_version = 'v20200528'
        cmip_dir = 'oi10/replicas'
    else:
        raise ValueError('Unrecognised CODREX model')

    hist_dir = f'/g/data/{cmip_dir}/CMIP6/CMIP/{institution}/{model}/historical/{run}/day/{args.var}/{grid}/{hist_version}/' 
    hist_files = sorted(glob.glob(f'{hist_dir}/*.nc'))
    if not hist_files:
        raise OSError(f'No files at {hist_dir}')
    ssp_dir = f'/g/data/{cmip_dir}/CMIP6/ScenarioMIP/{institution}/{model}/ssp370/{run}/day/{args.var}/{grid}/{ssp_version}/' 
    ssp_files = sorted(glob.glob(f'{ssp_dir}/*.nc'))
    if not ssp_files:
        raise OSError(f'No files at {ssp_dir}')

    input_ds = xcdat.open_mfdataset(hist_files + ssp_files)
    input_ds = input_ds.drop_duplicates('time')
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
    
    outdir = f'/g/data/ia39/npcp/data/{args.var}/{args.cordex_model}/GCM/raw/task-reference'
    hist_path = f'{outdir}/{args.var}_NPCP-20i_{args.cordex_model}_ssp370_{run}_GCM_latest_day_19600101-20191231.nc'
    proj_path = f'{outdir}/{args.var}_NPCP-20i_{args.cordex_model}_ssp370_{run}_GCM_latest_day_20600101-20991231.nc'
 
    ds_hist.to_netcdf(hist_path)
    ds_proj.to_netcdf(proj_path)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("var", type=str, help="variable to process")
    parser.add_argument(
        "cordex_model",
        type=str,
        choices=('CSIRO-ACCESS-ESM1-5', 'EC-Earth-Consortium-EC-Earth3', 'NCAR-CESM2'),
        help="model to process"
    )
    args = parser.parse_args()
    main(args)
