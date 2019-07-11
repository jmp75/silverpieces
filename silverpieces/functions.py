import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta # $ pip install python-dateutil
from datetime import date
from Utility import Utility

def monthly_mean(args_file):
    """Calculates the monthly mean.

    Arguments:
        args_file {YAML python object} -- YAML object encapsulating the parameters passed to monthly_mean method
    Returns:
        xarray.DataArray
    """
    product, start_date, end_date, variable_name = Utility.read_yml_params(args_file)

    ds = xr.open_dataset(product)
    #The issue with groupby is that it will aggregate the complete dataset down to 12 months. So if you have 2 years
    #worth of data, you probably want to get 24 monthly means and not 12.
    #    result = ds.sel(time=slice(start_date, end_date))[variable_name].groupby('time.month').mean(dim='time')

    #resampling needs a dataset object to maintain the expected dimensions. we need to again
    #  'select' the variable before the result is returned to convert the dataset to dataarray.
    result = ds.sel(time=slice(start_date, end_date))[variable_name] \
                .to_dataset().resample(time='1M').mean()[variable_name]

    return result

def yearly_mean(args_file):
    """Calculates the yearly mean.

    Arguments:
        args_file {YAML python object} -- YAML object encapsulating the parameters passed to yearly_mean method
    Returns:
        xarray.DataArray
    """
    product, start_date, end_date, variable_name = Utility.read_yml_params(args_file)

    ds = xr.open_dataset(product)

    result = ds.sel(time=slice(start_date, end_date))[variable_name] \
                .to_dataset().resample(time='1y').mean()[variable_name]
    return result

def seasonal_mean(args_file):
    """Calculates the seasonal mean.

    Arguments:
        args_file {YAML python object} -- YAML object encapsulating the parameters passed to seasonal_mean method
    Returns:
        xarray.DataArray
    """
    product, start_date, end_date, variable_name = Utility.read_yml_params(args_file)

    ds = xr.open_dataset(product)

    result = ds.sel(time=slice(start_date, end_date))[variable_name] \
                .to_dataset().resample(time='Q-FEB').mean()[variable_name]
    return result

def mean_all_odc(product, timespan, spatial_extents, projection, resolution):
    '''
    get product from data cube with specified resolution and projection
    peform mean on specified spatial extents
    return xarray
    '''
    xarray_ds = None
    variable_name = None # from product somehow?
    start_date = timspan[0]
    end_date = timspan[1]

    # allthough xarray and (presumably) ODC maybe capable of cookie cutting directly based on polygon
    # in existing code masks are precomputed and I expect this to be the most performant approach so
    # some comprimise needs to be reached for structuring underlying queries to either work with 
    # arbitrary polygons or work efficiently with catchment masks
    catchment_mask_number = None 

    return mean_catchment_mask_number_xr(xarray_ds, start_date, end_date)

def mean_all_xr(ds, start_date, end_date, variable_name):
    '''
    get mean for entire dataset 
    '''
    result = ds[variable_name].sel(time=slice(pd.to_datetime(start_date), pd.to_datetime(end_date))).mean(dim=('time'))
    return result

def mean_catchment_mask_number_xr(ds, start_date, end_date, variable_name, catchment_mask_number):
   '''
   get mean for catchment_mask enabled dataset  
   '''
   result = ds[variable_name].sel(time=slice(pd.to_datetime(start_date), pd.to_datetime(end_date))).where(ds.mask == catchment_mask_number).mean(dim=('time'))
   return result


def to_datetime(*dts):
    """Vectorised wrapper to convert to pandas timestamps. Tuple returned.
    """
    return tuple([pd.to_datetime(x) for x in dts])

def get_first_period(start_record, end_record, start_period, end_period):
    """Given the starts/ends of a record and period, find the first period whose start is in this record, shifted yearly.
    """
    start_record, end_record, start_period, end_period = to_datetime(start_record, end_record, start_period, end_period)
    pspan = end_period - start_period
    delta_year = relativedelta(years=1)
    # what is the first day of year of the start of the period that fits the record?
    start_rec_year = start_record.year
    d = datetime(start_rec_year, start_period.month, start_period.day)
    if d < start_record:
        d = d + delta_year
    delta_years = start_period.year - d.year
    e = end_period + relativedelta(years=-delta_years)
    return (d, e)

def max_shifting_years(start_record, end_record, start_period, end_period):
    """Given the starts/ends of a record and period, what is the maximum yearly shift from the earliest period that would still fit in the record.
    """
    start_record, end_record, start_period, end_period = to_datetime(start_record, end_record, start_period, end_period)
    delta_year = relativedelta(years=1)
    # what is the first 'day of year' of the start of the period that fits the record?
    d, _ = get_first_period(start_record, end_record, start_period, end_period)
    # what is the last 'day of year' of the end of the period that fits the record?
    end_rec_year = end_record.year
    e = datetime(end_rec_year, end_period.month, end_period.day)
    if e > end_record:
        e = e - delta_year
    tspan = e - d
    pspan = end_period - start_period
    max_shift = tspan - pspan
    last_start_period = d + max_shift
    max_years_shift = last_start_period.year - d.year
    return max_years_shift

class SpatialTemporalDataDescriptor(object):
    """Parent class to facilitate mapping gridded spatial-temporal data dimensions and variable names.

    Mostly to cater for differences between e.g. 'lat' and 'latitude' in dimension names.

    Attributes:
        x_dimname (str):
        y_dimname (str):
        time_dimname (str):
    """
    def __init__(self, x_dimname='lon', y_dimname='lat', time_dimname='time'):
        """Define a map of dimension names for X-Y-T gridded data sets.

        Args:
            x_dimname (str):
            y_dimname (str):
            time_dimname (str):
        """
        self.x_dimname     = x_dimname
        self.y_dimname     = y_dimname
        self.time_dimname  = time_dimname


class SpatialTemporalDataArrayStat(SpatialTemporalDataDescriptor):
    """Class to facilitate stat operations by mapping gridded spatial-temporal data dimensions and variable names.

    Attributes:
    """
    def __init__(self, x_dimname='lon', y_dimname='lat', time_dimname='time'):
        super(SpatialTemporalDataArrayStat, self).__init__(x_dimname, y_dimname, time_dimname)
        """Define a map of dimension names for X-Y-T gridded data sets.
        
        Args:
            x_dimname (str):
            y_dimname (str):
            time_dimname (str):
        """
    def _extrema_time_dim(self, x):
        tdim = x[self.time_dimname].values
        return (tdim[0], tdim[-1])

    def _max_num_years_shift(self, x, start_time, end_time):
        tmin, tmax = self._extrema_time_dim(x)
        return max_shifting_years(tmin, tmax, start_time, end_time)

    def _apply_timeslice(self, x, start_time, end_time, func = np.sum):
        y = x.loc[{ self.time_dimname: slice(start_time, end_time) }]
        return xr.apply_ufunc(func, y,
                        input_core_dims=[[self.time_dimname]],
                        #kwargs={'axis': -1, 'skipna':False})
                        kwargs={'axis': -1})
        
    def periods_stat_yearly(self, x, start_time, end_time, func = np.sum, start_record = None, end_record = None): 
        """Statistical summary/summaries over periods within an X-Y-T data array. 
        
        Args:
            x (xr.DataArray): X-Y-T data array with dimension names compatible with this object
            start_time (valid type for pd.to_datetime): start time of a period of interest
            end_time (valid type for pd.to_datetime): end time of a period of interest
            func (callable): function callable with a signature similar to numpy.sum
            start_record (valid type for pd.to_datetime): optional, start time of 
                the window of record to use for statistics. Lower time bound of x if None.
            end_record (valid type for pd.to_datetime): optional, end time of the window 
                of record to use for statistics. Upper time bound of x if None.

        Examples:

            >>> x = create_daily_sp_cube('2001-01-01', '2009-12-31', nx=2, ny=3, fun_fill=fill_year)
            >>> s = SpatialTemporalDataArrayStat()
            >>> y = s.periods_stat_yearly(x, '2001-04-01', '2001-08-31')
            >>> y.name = 'southern autumn/winter sums'
            >>> x.shape
            (3287, 3, 2)
            >>> y.shape
            (9, 3, 2)

        """
        start_time, end_time = to_datetime(start_time, end_time)
        tmin, tmax = self._extrema_time_dim(x)
        # TODO more stringent input arg checks.
        if start_record is None:
            start_record = tmin
        if end_record is None:
            end_record = tmax
        max_years_shift = max_shifting_years(start_record, end_record, start_time, end_time) + 1
        td = x[self.time_dimname].values
        start_record = td[0]
        end_record = td[-1]
        d, e = get_first_period(start_record, end_record, start_time, end_time)    
        cumulated = [self._apply_timeslice(x, d + relativedelta(years=year), e + relativedelta(years=year), func) for year in range(max_years_shift)]
        y = xr.concat(cumulated, dim=self.time_dimname)
        # maybe an optional arg for the resulting time dimension (start or end of periods)
        y[self.time_dimname] = np.array([pd.to_datetime(e + relativedelta(years=year)) for year in range(max_years_shift)])
        return y

    def quantile_over_time_dim(self, x, q, interpolation = 'linear', keep_attrs=None):
        """Compute the qth quantile of the data along the Time dimension of an X-Y-T data array. 
        
        Args:
            x (xr.DataArray): X-Y-T data array with dimension names compatible with this object
            q (list of floats): probabilities, 0 to 1.
        """
        return x.quantile(q=q, dim=[self.time_dimname], interpolation=interpolation, keep_attrs=keep_attrs)            

    def searchsorted(self, q_values, x):
        """Find indices where elements should be inserted to maintain order. 
            Used to classify gridded values against gridded quantile values. 
        
        Args:
            q (xr.DataArray): X-Y-Q data array with Q quantile values.
            x (xr.DataArray): X-Y data array with dimension names compatible with this object
        """
        nlon = len(q_values[self.x_dimname])
        nlat = len(q_values[self.y_dimname])
        xresult = x.copy()
        result = np.empty_like(x, dtype=np.float32)
        # I could not figure out how to vectorise this
        # tried a variety of things like `v_searchsorted = np.vectorize(np.searchsorted, signature='(n,m),(n,m)->(n)')` but to no avail. 
        # TODO
        for lat in np.arange(nlat):
            for lon in np.arange(nlon):
                xv = x[lat, lon]
                if np.isnan(xv): # just in case - try without?
                    result[lat, lon] = np.nan
                else:
                    result[lat, lon] = np.searchsorted(q_values[:,lat, lon].values, xv)
        xresult.values = result
        return xresult

