import xarray as xr
import pandas as pd
import netCDF4
import os
import glob

def time_file_index_dask(search_string, time_var):
    """Index a set of files and generate a pandas data frame of time
    (index) and filename. 
    
    Arguments:
        search_string {str} -- A search string including the
            directory, wildcards, and extensions to index.
        time_var {str} -- The title of the time variable in the
            netCDF files.
    
    Returns:
        pandas.DataFrame -- a pandas dataframe object. The DateTimeIndex
            is from the times in the files, and columns are filenames. 
    """

    filenames = sorted(glob.glob(search_string))
    data = xr.open_mfdataset(filenames, parallel=True)
    
    time_file = pd.DataFrame({'filename': filenames}, index = data[time_var].values)
    time_file = time_file[~time_file.index.duplicated(keep='first')]
    
    return time_file