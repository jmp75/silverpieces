def test():
   print("Hello World")

def mean_all(ds, start_date, end_date, variable_name):
   '''
   get mean for entire dataset 
   '''
   result = ds[variable_name].sel(time=slice(pd.to_datetime(start_date), pd.to_datetime(end_date))).mean(dim=('time'))
   return result



def mean_catchment_mask_number(ds, start_date, end_date, variable_name, catchment_mask_number):
   '''
   get mean for catchment_mask enabled dataset  
   '''
   result = ds[variable_name].sel(time=slice(pd.to_datetime(start_date), pd.to_datetime(end_date))).where(ds.mask == catch_num).mean(dim=('time'))
   return result
