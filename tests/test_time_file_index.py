from summarize_netcdf import time_file_index
from datetime import datetime
from pandas import DataFrame


def test_time_file_index():

    tfi = time_file_index.time_file_index(
        "../tests_data/",
        "time",
        begin_date=datetime(2013, 1, 1, 0, 0),
        end_date=datetime(2013, 1, 5, 0, 0),
    )

    tfi.head()

    assert isinstance(tfi, DataFrame)
