import os
import sys
import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

pkg_dir = os.path.join(os.path.dirname(__file__),'..')
sys.path.append(pkg_dir)

from silverpieces.functions import *

def create_daily_year(start_time, end_time, nx=2, ny=3):
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    tdim = pd.date_range(start=start_time, end=end_time, freq='D')
    xdim = np.arange(0, nx * 0.5 - 1e-2, 0.5)
    ydim = np.arange(0.25, 0.25 + ny * 0.5 - 1e-2, 0.5)
    x = np.empty([len(tdim), nx, ny]) # TODO: fill with?
    y = xr.DataArray(x, 
                coords=[tdim,xdim,ydim],
                dims=['time', 'lon', 'lat'],
                name='test_daily_data')
    return y

def test_num_year_detection():
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-01-01', '2001-12-31') == 2
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-01-01', '2001-10-31') == 2
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-03-01', '2001-12-31') == 2
    #
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-01-01', '2002-12-31') == 1
    assert max_shifting_years('2001-01-01', '2003-12-30', '2001-01-01', '2002-12-31') == 0

# test_num_year_detection()

# def test_rolling_years_stats():
#     start_time = pd.to_datetime('2001-01-01')
#     end_time = pd.to_datetime('2018-12-31')
#     x = create_daily_year('2001-01-01', '2009-12-31', nx=2, ny=3)
#     s = SpatialTemporalDataArrayStat()
#     y = s.rolling_years(x, '2001-01-01', '2002-12-31')
#     assert len(y.time) == (10 - 1)

# test_rolling_years_stats()
