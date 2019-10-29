#!/user/bin/env python
# coding=utf-8

import xarray as xr
import datetime
import time
import numpy as np
import pandas as pd
import netCDF4
import os
import glob

input_directory='/data/models/391183ee-827e-11e1-a4f3-00219bfe5678/'
filenames = sorted(glob.glob(input_directory + '*.nc'))