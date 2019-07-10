import xarray as xr
import numpy as np
import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta # $ pip install python-dateutil
from datetime import date

def monthly_mean(args_file):
   """Calculates the monthly mean.
   
   Arguments:
       args_file {[YAML python object]} -- [YAML object encapsulating the parameters passed to monthly_mean method]
   """
   product = args_file.get('Args').get('product')
   variable_name = args_file.get('Args').get('variablename')
   start_date = args_file.get('Args').get('timespan').get('startDate')
   end_date = args_file.get('Args').get('timespan').get('endDate')

   ds = xr.open_dataset(product)
   result = ds.sel(time=slice(start_date, end_date))[variable_name].groupby('time.month').mean(dim='time')

   return result

def yearly_mean(args_file):
   """Calculates the monthly mean.
   
   Arguments:
       args_file {[YAML python object]} -- [YAML object encapsulating the parameters passed to monthly_mean method]
   """
   product = args_file.get('Args').get('product')
   variable_name = args_file.get('Args').get('variablename')   
   start_date = args_file.get('Args').get('timespan').get('startDate')
   end_date = args_file.get('Args').get('timespan').get('endDate')

   ds = xr.open_dataset(product)
   result = ds.sel(time=slice(start_date, end_date))[variable_name].groupby('time.year').mean(dim='time')

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
    result = ds[variable_name].sel(time=slice(pd.to_datetime(start_date), pd.to_datetime(end_date))).where(ds.mask == catch_num).mean(dim=('time'))
    return result

def max_shifting_years(start_record, end_record, start_period, end_period):
    start_record = pd.to_datetime(start_record)
    end_record = pd.to_datetime(end_record)
    start_period = pd.to_datetime(start_period)
    end_period = pd.to_datetime(end_period)

    delta_year = relativedelta(years=1)

    # what is the first day of year of the start of the period that fits the record?
    start_rec_year = start_record.year
    d = datetime(start_rec_year, start_period.month, start_period.day)
    if d < start_record:
        d = d + delta_year
    # what is the last day of year of the end of the period that fits the record?
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
        """Define class names of interest in visualised data set, and color coding.

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
        """Define class names of interest in visualised data set, and color coding.
        
        Args:
        x_dimname (str):
        y_dimname (str):
        time_dimname (str):
        """
    def _max_num_years_extent(self, x, start_time, end_time):
        tdim = x[self.time_dimname].values
        return max_shifting_years(tdim[0], tdim[-1], start_time, end_time)

    def _apply_timeslice(self, x, start_time, end_time, func = np.sum):
        y = x.loc[{ self.time_dimname: slice(start_time, end_time) }]
        return xr.apply_ufunc(func, y,
                        input_core_dims=[[self.time_dimname]],
                        #kwargs={'axis': -1, 'skipna':False})
                        kwargs={'axis': -1})
        
    def rolling_years(self, x, start_time, end_time, n_years = None, func = np.sum):
        start_time = pd.to_datetime(start_time)
        end_time = pd.to_datetime(end_time)
        if n_years is None:
            n_years = self._max_num_years_extent(x, start_time, end_time)
        cumulated = [self._apply_timeslice(x, start_time + relativedelta(years=year), end_time + relativedelta(years=year), func) for year in range(n_years)]
        y = xr.concat(cumulated, dim=self.time_dimname)
        y[self.time_dimname] = np.array([pd.to_datetime(start_time + relativedelta(years=year)) for year in range(n_years)])
        return y

