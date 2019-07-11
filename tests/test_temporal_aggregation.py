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
    x = np.empty([len(tdim), ny, nx])
    fun_fill(x)
    y = xr.DataArray(x, 
                coords=[tdim,ydim,xdim],
                dims=['time', 'lat', 'lon'],
                name='test_daily_data')
    return y

def test_num_year_detection():
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-01-01', '2001-12-31') == 2
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-01-01', '2001-10-31') == 2
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-03-01', '2001-12-31') == 2
    #
    assert max_shifting_years('2001-01-01', '2003-12-31', '2001-01-01', '2002-12-31') == 1
    assert max_shifting_years('2001-01-01', '2003-12-30', '2001-01-01', '2002-12-31') == 0
    # If the windows is less than a calendar year, it should still find the right max shift
    assert max_shifting_years('2007-01-01', '2018-12-31', '2001-01-01', '2001-12-31') == 11
    # 2016 a leap year...
    assert max_shifting_years('2007-01-01', '2018-12-31', '2016-01-01', '2016-12-31') == 11


def test_periods_stat_yearly_stats():
    start_time = pd.to_datetime('2001-01-01')
    end_time = pd.to_datetime('2002-12-31')
    x = create_daily_sp_cube('2001-01-01', '2009-12-31', nx=2, ny=3, fun_fill=fill_year)
    s = SpatialTemporalDataArrayStat()
    y = s.periods_stat_yearly(x, '2001-01-01', '2002-12-31')
    assert len(y.time) == (9 - 2 + 1)
    tdim = y[s.time_dimname].values
    assert pd.to_datetime(tdim[0] ) == end_time
    assert pd.to_datetime(tdim[-1]) == pd.to_datetime('2009-12-31')
    assert np.all(y[0,:,:] == 365 * 1.0)
    assert np.all(y[1,:,:] == 365 * (1.0 + 2.0))
    y = s.periods_stat_yearly(x, '2001-01-01', '2002-12-31', func = np.mean)
    assert np.all(y[0,:,:] == 0.5)
    assert np.all(y[1,:,:] == 1.5)

    y = s.periods_stat_yearly(x, '2004-01-01', '2005-12-31')
    assert len(y.time) == (9 - 2 + 1)
    tdim = y[s.time_dimname].values
    assert pd.to_datetime(tdim[0] ) == end_time


def test_periods_stat_yearly_stats_leap_years():
    # Noticed a bug in a notebook. Had to happen with leap yr.
    x = create_daily_sp_cube('2007-01-01', '2018-12-31', nx=2, ny=3, fun_fill=fill_year)
    s = SpatialTemporalDataArrayStat()
    y = s.periods_stat_yearly(x, '2016-01-01', '2016-12-31')
    assert len(y.time) == 12
    tdim = y[s.time_dimname].values
    assert pd.to_datetime(tdim[0]) == pd.to_datetime('2007-12-31')
    assert pd.to_datetime(tdim[-1]) == pd.to_datetime('2018-12-31')

def test_quantiles_dc():
    start_time = pd.to_datetime('2001-01-01')
    end_time = pd.to_datetime('2002-12-31')
    x = create_daily_sp_cube('2001-01-01', '2009-12-31', nx=2, ny=3, fun_fill=fill_year)
    s = SpatialTemporalDataArrayStat()
    y = s.periods_stat_yearly(x, '2001-01-01', '2002-12-31')
    q = np.array([.1, .5, .9])
    qs = s.quantile_over_time_dim(y, q)
    z = y[0,:,:].copy()
    # z[]
    z[0,:] = 10.0
    z[1,:] = 1000.0
    z[2,:] = 3000.0
    cat_q = s.searchsorted(qs, z)
    assert cat_q.shape == (3, 2)
    assert np.all(cat_q[0,:] == 0)
    assert np.all(cat_q[1,:] == 1)
    assert np.all(cat_q[2,:] == 2)

# test_num_year_detection()
# test_periods_stat_yearly_stats()
# test_quantiles_dc()
test_periods_stat_yearly_stats_leap_years()