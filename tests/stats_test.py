import logging
logging.getLogger().setLevel(logging.DEBUG)
logging.debug('hi from the logger!')

import unittest
import os
import sys
import yaml
import xarray as xr

root_pkg_dir = os.path.join(os.path.dirname(__file__),'..')
sys.path.append(root_pkg_dir)

from silverpieces.functions import *
from utilities import *

class TestStatMethods(unittest.TestCase):

    def test_dummy_data_shape(self):
        try:
            t, x, y, src_data = get_data_src_seq(nt=5, nx=3, ny=2)
            f = create_file(t, 't', x, 'latitude', y, 'longitude', src_data, 'band')
            band = read_var(f, 'band')
            self.assertEqual(band.shape, (5, 3, 2))
        except Exception as ex:
            print(ex)
        finally:
            os.unlink(f)
    
    def test_dummy_xarray_read(self):
        from calendar import monthrange 
        try:
            year = 2011
            day_offsets = [0]
            for i in range(2, 12):
                day_offsets.append(day_offsets[-1] + monthrange(year, i)[1])
            day_offsets = np.array(day_offsets)
            t,x,y,src_data=get_spatial_data_src_seq(t=day_offsets, lat_start=-10.0, lat_end=-44.0, lat_size=681, lon_start=112.0, lon_end=154.0, lon_size=841)
            f=create_file(t,'time',x,'latitude',y,'longitude',src_data,'band', year)
            with xr.open_dataset(f) as ds:
                self.assertAlmostEqual(ds.latitude.values.min(), -44.0)
                self.assertAlmostEqual(ds.latitude.values.max(), -10.0)
                self.assertAlmostEqual(ds.longitude.values.min(), 112.0)
                self.assertAlmostEqual(ds.longitude.values.max(), 154.0)
                self.assertEqual(len(ds.latitude), 681)
                self.assertEqual(len(ds.longitude), 841)
        except Exception as ex:
            print(ex)
        finally:
            os.unlink(f)
    
    def test_monthly_mean(self):
        print("current Directory is:", os.getcwd())
        with open("./tests/testArg.yaml", 'r') as stream:
            try:
                args_file = yaml.safe_load(stream)
                t, x, y, src_data = get_data_src_seq(nt=365, nx=3, ny=2)
                f = create_file(t, 'time', x, 'latitude', y, 'longitude', src_data, 'band')

                #replace the product name with filename with dummy data
                args_file['Args']['product'] = f.name
                result = monthly_mean(args_file)
                jan_mean = np.arange(0, 31).sum()/31
                feb_mean = np.arange(31, 59).sum()/28

                self.assertEqual(result[0][0][0], jan_mean)
                self.assertEqual(result[1][0][0], feb_mean)
                self.assertEqual(result.shape, (2, 3, 2))

                #The time dimension changes to month only when we use groupby functionality
                #for calculating means.
                # self.assertEqual(result.dims[0], 'month')
            except Exception as ex:
                print(ex)
            finally:
                os.unlink(f)

    def test_monthly_mean_over_multiple_years(self):
        print("current Directory is:", os.getcwd())
        try:
            ymlStr = """Args: 
                        product: 'AWRA' #fill in the name of the test file created with dummy data
                        timespan:
                            startDate:  
                            endDate:  
                        variablename: 'band'"""

            args_file = yaml.safe_load(ymlStr)
            t, x, y, src_data = get_data_src_seq(nt=730, nx=3, ny=2)
            f = create_file(t, 'time', x, 'latitude', y, 'longitude', src_data, 'band')

            #replace the product name with filename with dummy data
            args_file['Args']['product'] = f.name
            result = monthly_mean(args_file)
            jan_mean = np.arange(0, 31).sum()/31
            feb_mean = np.arange(31, 59).sum()/28

            self.assertEqual(result[0][0][0], jan_mean)
            self.assertEqual(result[1][0][0], feb_mean)
            self.assertEqual(result.shape, (24, 3, 2))
            # self.assertEqual(result.dims[0], 'month')
        except Exception as ex:
            print(ex)
        finally:
            os.unlink(f)

    def test_yearly_mean(self):
        print("current Directory is:", os.getcwd())
        try:
            ymlStr = """Args: 
                            product: 'AWRA' #fill in the name of the test file created with dummy data
                            timespan:
                                startDate:  
                                endDate:  
                            variablename: 'band'"""
            args_file = yaml.safe_load(ymlStr)
            t, x, y, src_data = get_data_src_seq(nt=730, nx=3, ny=2)
            f = create_file(t, 'time', x, 'latitude', y, 'longitude', src_data, 'band')

            #replace the product name with filename with dummy data
            args_file['Args']['product'] = f.name
            result = yearly_mean(args_file)
            yearly_2010_mean = np.arange(0, 365).sum()/365
            yearly_2011_mean = np.arange(365, 730).sum()/365

            self.assertEqual(result[0][0][0], yearly_2010_mean)
            self.assertEqual(result[1][0][0], yearly_2011_mean)
            self.assertEqual(result.shape, (2, 3, 2))

            #The time dimension changes to year only when we use groupby functionality
            #for calculating means.
            #self.assertEqual(result.dims[0], 'year')
        except Exception as ex:
            print(ex)
        finally:
            os.unlink(f)

    def test_seasonal_mean(self):
        print("current Directory is:",os.getcwd())    
        try:
            ymlStr = """Args: 
                            product: 'AWRA' #fill in the name of the test file created with dummy data
                            timespan:
                                startDate:  
                                endDate:  
                            variablename: 'band'"""
            args_file = yaml.safe_load(ymlStr)
            t,x,y,src_data=get_data_src_seq(nt=730,nx=3,ny=2)
            f=create_file(t,'time',x,'latitude',y,'longitude',src_data,'band')

            #replace the product name with filename with dummy data
            args_file['Args']['product'] = f.name
            result = seasonal_mean(args_file)
            seasonal_2010_feb_mean = np.arange(0,59).sum()/(31+28)
            seasonal_2010_may_mean = np.arange(59,59+31+30+31).sum()/(31+30+31)
            #for the last period, it jumps over to feb/2012 even when we have data till dec/2011
            #but for averaging it only considers the days when we have data
            seasonal_2012_feb_mean = np.arange(699,730).sum()/31
            
            
            self.assertEqual(result[0][0][0], seasonal_2010_feb_mean)
            self.assertEqual(result[1][0][0], seasonal_2010_may_mean)
            self.assertEqual(result[8][0][0], seasonal_2012_feb_mean)
            self.assertEqual(result.shape, (9, 3, 2))          
            
            #The time dimension changes to year only when we use groupby functionality
            #for calculating means.
            #self.assertEqual(result.dims[0], 'year')
        except Exception as ex:
            print(ex)
        finally:
            os.unlink(f)

    def test_seasonal_mean_partial_dataset1(self):
        print("current Directory is:", os.getcwd())
        try:
            ymlStr = """Args: 
                            product: 'AWRA' #fill in the name of the test file created with dummy data
                            timespan:
                                startDate:  
                                endDate:  2010-12-31
                            variablename: 'band'"""
            args_file = yaml.safe_load(ymlStr)
            t, x, y, src_data = get_data_src_seq(nt=730, nx=3, ny=2)
            f = create_file(t, 'time', x, 'latitude', y, 'longitude', src_data, 'band')

            #replace the product name with filename with dummy data
            args_file['Args']['product'] = f.name
            result = seasonal_mean(args_file)
            seasonal_2010_feb_mean = np.arange(0, 59).sum()/(31+28)
            seasonal_2010_may_mean = np.arange(
                59, 59+31+30+31).sum()/(31+30+31)
            #for the last period, it jumps over to feb/2011 as the time boundary even when we have requested till dec/2011.
            #But for averaging it only considers the days falling in the date bounds.
            seasonal_2011_feb_mean = np.arange(334, 365).sum()/31

            self.assertEqual(result[0][0][0], seasonal_2010_feb_mean)
            self.assertEqual(result[1][0][0], seasonal_2010_may_mean)
            self.assertEqual(result[4][0][0], seasonal_2011_feb_mean)
            self.assertEqual(result.shape, (5, 3, 2))

            #The time dimension changes to year only when we use groupby functionality
            #for calculating means.
            #self.assertEqual(result.dims[0], 'year')
        except Exception as ex:
            print(ex)
        finally:
            os.unlink(f)

    def test_seasonal_mean_partial_dataset2(self):
        print("current Directory is:", os.getcwd())
        try:
            ymlStr = """Args: 
                            product: 'AWRA' #fill in the name of the test file created with dummy data
                            timespan:
                                startDate:  
                                endDate:  2010-12-30
                            variablename: 'band'"""
            args_file = yaml.safe_load(ymlStr)
            t, x, y, src_data = get_data_src_seq(nt=730, nx=3, ny=2)
            f = create_file(t, 'time', x, 'latitude', y, 'longitude', src_data, 'band')

            #replace the product name with filename with dummy data
            args_file['Args']['product'] = f.name
            result = seasonal_mean(args_file)
            seasonal_2010_feb_mean = np.arange(0, 59).sum()/(31+28)
            seasonal_2010_may_mean = np.arange(
                59, 59+31+30+31).sum()/(31+30+31)
            #for the last period, it jumps over to feb/2011 as the time boundary even when we have requested till dec/2011.
            #But for averaging it only considers the days falling in the date bounds.
            seasonal_2011_feb_mean = np.arange(334, 364).sum()/30

            self.assertEqual(result[0][0][0], seasonal_2010_feb_mean)
            self.assertEqual(result[1][0][0], seasonal_2010_may_mean)
            self.assertEqual(result[4][0][0], seasonal_2011_feb_mean)
            self.assertEqual(result.shape, (5, 3, 2))

            #The time dimension changes to year only when we use groupby functionality
            #for calculating means.
            #self.assertEqual(result.dims[0], 'year')
        except Exception as ex:
            print(ex)
        finally:
            os.unlink(f)


if __name__ == '__main__':
    unittest.main()
