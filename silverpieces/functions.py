def test():
   print("Hello World")

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
