"""Command line program for converting 2m wind speed to 10m.

Original code: https://git.nci.org.au/vd5822/transform-wind-grids
"""

import argparse

import numpy as np
import h5py
import xarray as xr
import cmdline_provenance as cmdprov


def main(args):
    """Run the program."""
    
    wind_profile = h5py.File(args.wind_profile_file, 'r')
    z0 = wind_profile['parameters/z0_masked'][:]
    zd = 0.5
    k = np.log((10 - zd)/z0) / np.log((2 - zd)/z0)

    wsp2m_ds = xr.open_dataset(args.wsp2m_file)
    wsp10m_da = k * wsp2m_ds[args.wsp_var]

    wsp10m_ds = wsp10m_da.to_dataset()
    wsp10m_ds.attrs = wsp2m_ds.attrs
    wsp10m_ds.attrs['history'] = cmdprov.new_log()
    wsp10m_ds.to_netcdf(args.wsp10m_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("wsp2m_file", type=str, help="input 2m wind speed data file")
    parser.add_argument("wsp_var", type=str, help="wind speed variable")
    parser.add_argument("wind_profile_file", type=str, help="vertical wind profile data file")
    parser.add_argument("wsp10m_file", type=str, help="output 10m wind speed data file")

    args = parser.parse_args()
    main(args)
