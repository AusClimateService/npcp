"""Utilities for analysis of NPCP intercomparison data"""

import glob
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import xarray as xr

import geopandas as gpd
from shapely.geometry import mapping


def get_aus_shape():
    """Get shape for Australia"""
    
    aus_shape = gpd.read_file(
        '/g/data/ia39/aus-ref-clim-data-nci/shapefiles/data/australia/australia.shp',
        crs="epsg:4326"
    )

    return aus_shape
    

def get_nrm_super_cluster(supcluster_abbreviation):
    """Get shape for an NRM super cluster"""

    nrm_sub_clusters = gpd.read_file(
        '/g/data/ia39/aus-ref-clim-data-nci/shapefiles/data/nrm_regions/nrm_regions.shp',
        crs="epsg:4326"
    )
    nrm_super_clusters = nrm_sub_clusters.dissolve(by='SupClusNm', as_index=False)
    nrm_super_clusters = nrm_super_clusters.drop(columns=['SubClusNm', 'SubClusAb', 'ClusterNm', 'ClusterAb'])
    nrm_super_clusters = nrm_super_clusters[['SupClusNm', 'SupClusAb', 'geometry']]
    
    supcluster_shape = nrm_super_clusters[nrm_super_clusters['SupClusAb'] == supcluster_abbreviation]

    return supcluster_shape


def clip_data(data, shape):
    """Clip data"""

    data_prep = (
        data
        .rio.write_crs(4326, inplace=True)
        .rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
        .rio.write_coordinate_system(inplace=True)
    )
    
    data_clipped = data_prep.rio.clip(
        shape.geometry.apply(mapping),
        shape.crs,
        drop=False
    )
    
    return data_clipped


def get_npcp_data(
    variable,
    driving_model,
    downscaling_model,
    bias_correction_method,
    task,
    start_date,
    end_date,
    region=None,
): 
    """Get data that has been submitted to the NPCP intercomparison project"""
    
    assert variable in ['tasmax', 'tasmin', 'pr']
    assert driving_model in ['observations', 'CSIRO-ACCESS-ESM1-5', 'NCAR-CESM2', 'EC-Earth-Consortium-EC-Earth3', 'ECMWF-ERA5']
    assert downscaling_model in ['AGCD', 'BOM-BARPA-R', 'UQ-DES-CCAM-2105', 'CSIRO-CCAM-2203', 'GCM']
    assert bias_correction_method in ['raw', 'ecdfm', 'qme', 'qdc', 'mbcn', 'mrnbc']
    assert task in ['task-reference', 'task-projection', 'task-historical', 'task-xvalidation']
    assert region in [None, 'AU', 'NA', 'SA', 'EA', 'R']
    
    file_start = variable if bias_correction_method in ['raw', 'qme'] else f'{variable}_NPCP'
    file_end = '1231.nc' if bias_correction_method == 'ecdfm' else '.nc'
    search_dir = f'/g/data/ia39/npcp/data/{variable}/{driving_model}/{downscaling_model}/{bias_correction_method}/{task}'
    files = sorted(glob.glob(f'{search_dir}/{file_start}*{file_end}'))
    if not files:
        raise OSError(f'No files at {search_dir}')
    ds = xr.open_mfdataset(files).sel(time=slice(start_date, end_date))
    lats = np.round(np.arange(-44, -9.9, 0.2), decimals=1)
    if np.allclose(ds['lat'].values, lats, rtol=1e-05, atol=1e-08, equal_nan=True):
        lat_attrs = ds['lat'].attrs
        ds = ds.assign_coords({'lat': lats})
        ds.attrs = lat_attrs
    lons = np.round(np.arange(112, 154.01, 0.2), decimals=1)
    if np.allclose(ds['lon'].values, lons, rtol=1e-05, atol=1e-08, equal_nan=True):
        lon_attrs = ds['lon'].attrs
        ds = ds.assign_coords({'lon': lons})
        ds.attrs = lon_attrs
    
    if region == 'AU':
        shape = get_aus_shape()
        da = clip_data(ds[variable], shape)
    elif region:
        shape = get_nrm_super_cluster(region)
        da = clip_data(ds[variable], shape)
    else:
        da = ds[variable]
                   
    return da      


def get_pr_weights(gcm, task):
    """Get fraction of time steps influenced by precipitation obs"""
    
    if task == 'historical':
        start_year = '1980'
        end_year = '2019'
    elif (task == 'xvalidation') and (gcm in ['CSIRO-ACCESS-ESM1-5', 'NCAR-CESM2', 'EC-Earth-Consortium-EC-Earth3']):
        start_year = '1960'
        end_year = '1989'
    elif (task == 'xvalidation') and (gcm == 'ECMWF-ERA5'):
        start_year = '1980'
        end_year = '1999'
    else:
        raise ValueError('Invalid GCM / task combination')
    
    fraction_dir = '/g/data/ia39/npcp/data/pr/observations/AGCD/raw/task-reference/'
    fraction_file = f'ob-fractions_NPCP-20i_AGCD_v1-0-1_day_{start_year}0101-{end_year}1231.nc'
    ds = xr.open_dataset(fraction_dir+fraction_file)
    
    return ds['fraction']


def mask_by_pr_ob_fraction(da, da_fraction, threshold=0.9):
    """Mask data according to precip obs fraction"""
    
    da_selection = da_fraction > threshold 
    da = da.where(da_selection)
    
    return da
