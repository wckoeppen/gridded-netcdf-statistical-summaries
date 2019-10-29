import glob
import os

from datetime import datetime
import netCDF4
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from tqdm import trange


def time_file_index(
    base_dir,
    time_var,
    begin_date=datetime(2013, 1, 1, 0, 0),
    end_date=datetime(2013, 1, 5, 0, 0),
    filenames=None,
):
    """Index a set of files and generate a pandas data frame of time (index) and
    filename. 

    Parameters
    ----------
    base_dir : str
        Index a set of files and generate a pandas data frame of time (index) and 
        filename.

    time_var : str
        The title of the time variable in the netCDF files.

    begin_date : datetime.datetime, optional
        The minimum date from which to include files.

    end_date : datetime.datetime, optional
        The maximum date from which to include files.

    filenames : list, default: None
        A list of filenames, if you found them some other way.

    Returns
    -------
    pandas.Dataframe
        A pandas dataframe with a DateTimeIndex constructed from the files,
        and columns of filename and t_index. The latter represents the
        numerical index value of the time slice in the named file.
    """

    if filenames is None:
        filenames = find_files(base_dir, begin_date, end_date)

    nfiles = len(filenames)

    # Build a tuple with dates and filenames the file contains for every file in the index
    time_file = []

    for i in trange(nfiles):

        with netCDF4.Dataset(filenames[i]) as netcdf:
            # extract the time, turn it into a date

            time_dat = netcdf.variables[time_var]
            times = np.array(time_dat)

            # some have calendar, some don't
            try:
                times = netCDF4.num2date(times, time_dat.units, time_dat.calendar)
            except:
                times = netCDF4.num2date(times, time_dat.units)

        for j in range(len(times)):
            time_file.append((times[j], filenames[i], j))

    result = pd.DataFrame(time_file, columns=["date", "file", "t_index"])
    result = result.set_index("date")

    # check for duplicates
    dupes = result.index.duplicated(keep="first")

    if dupes.sum() > 0:
        #       print('Found duplicate times, using first one found.')
        result = result[~dupes]

    return result


def get_var(file, variable_name):
    with netCDF4.Dataset(file) as netcdf:
        return netcdf[variable_name][:]


def get_file(file_index, row):
    index = file_index.index.get_loc(row.name, method="nearest")
    return file_index["file"].iloc[index]


def get_t_index(file_index, row):
    index = file_index.index.get_loc(row.name, method="nearest")
    return file_index["t_index"].iloc[index]


def find_files(base_dir, begin_date, end_date):

    search_dirs = []

    stop_date = begin_date

    while stop_date < (end_date + relativedelta(months=+1)):
        search_dirs.append(stop_date.strftime("%Y/%Y_%m"))

        stop_date += relativedelta(months=+1)

    print("search directories")
    print(search_dirs)

    filenames = []

    for search_dir in search_dirs:
        filenames += sorted(glob.glob(os.path.join(base_dir, search_dir, "*.nc")))

    return filenames
