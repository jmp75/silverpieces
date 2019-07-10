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


def fill_time_index(nd_array):
    td = nd_array.shape[0]
    for i in range(td):
        nd_array[i,:,:] = i

def fill_year(nd_array):
    start_time = datetime(2001,1,1)
    td = nd_array.shape[0]
    for i in range(td):
        nd_array[i,:,:] = (start_time + relativedelta(days=i)).year - start_time.year

def create_daily_sp_cube(start_time, end_time, nx=2, ny=3, fun_fill=fill_time_index):
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    tdim = pd.date_range(start=start_time, end=end_time, freq='D')
    xdim = np.arange(0, nx * 0.5 - 1e-2, 0.5)
    ydim = np.arange(0.25, 0.25 + ny * 0.5 - 1e-2, 0.5)
    x = np.empty([len(tdim), nx, ny])
    fun_fill(x)
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


def test_rolling_years_stats():
    start_time = pd.to_datetime('2001-01-01')
    end_time = pd.to_datetime('2018-12-31')
    x = create_daily_sp_cube('2001-01-01', '2009-12-31', nx=2, ny=3, fun_fill=fill_year)
    s = SpatialTemporalDataArrayStat()
    y = s.rolling_years(x, '2001-01-01', '2002-12-31')
    assert len(y.time) == (9 - 2)
    tdim = y[s.time_dimname].values
    assert pd.to_datetime(tdim[0] ) == start_time
    assert pd.to_datetime(tdim[-1]) == pd.to_datetime('2007-01-01')
    assert np.all(y[0,:,:] == 365 * 1.0)
    assert np.all(y[1,:,:] == 365 * (1.0 + 2.0))
    y = s.rolling_years(x, '2001-01-01', '2002-12-31', n_years = None, func = np.mean)
    assert np.all(y[0,:,:] == 0.5)
    assert np.all(y[1,:,:] == 1.5)

def test_quantiles_dc():
    pass

# test_num_year_detection()
test_rolling_years_stats()
