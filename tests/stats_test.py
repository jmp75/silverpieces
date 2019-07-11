import logging
logging.getLogger().setLevel(logging.DEBUG)
logging.debug('hi from the logger!')

import unittest
import os
import sys
import yaml
#importing numpy causes debugging to stop working! Actually seems like any C based python packages causes the debugger to fail.
#import numpy as np
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'silverpieces'))
import functions  
from utilities import *

class TestStatMethods(unittest.TestCase):

    def test_dummy_data_shape(self):
        t,x,y,src_data=get_data_src_seq(nt=5,nx=3,ny=2)
        f=create_file(t,'t',x,'latitude',y,'longitude',src_data,'band')
        band=read_var(f.name,'band')
        self.assertEqual(band.shape, (5, 3, 2))

    def test_monthly_mean(self):
        print("current Directory is:",os.getcwd())
        with open("./tests/testArg.yaml", 'r') as stream:
            try:
                args_file = yaml.safe_load(stream)
                t,x,y,src_data=get_data_src_seq(nt=365,nx=3,ny=2)
                f=create_file(t,'time',x,'latitude',y,'longitude',src_data,'band')

                #replace the product name with filename with dummy data
                args_file['Args']['product'] = f.name
                result = functions.monthly_mean(args_file)
                jan_mean = np.arange(0,31).sum()/31
                feb_mean = np.arange(31,59).sum()/28
                
                self.assertEqual(result[0][0][0], jan_mean)
                self.assertEqual(result[1][0][0], feb_mean)
                self.assertEqual(result.shape, (2, 3, 2))

                #The time dimension changes to month only when we use groupby functionality
                #for calculating means.
                # self.assertEqual(result.dims[0], 'month')
            except yaml.YAMLError as exc:
                print(exc)

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
            t,x,y,src_data=get_data_src_seq(nt=730,nx=3,ny=2)
            f=create_file(t,'time',x,'latitude',y,'longitude',src_data,'band')

            #replace the product name with filename with dummy data
            args_file['Args']['product'] = f.name
            result = functions.monthly_mean(args_file)
            jan_mean = np.arange(0,31).sum()/31
            feb_mean = np.arange(31,59).sum()/28

            self.assertEqual(result[0][0][0], jan_mean)
            self.assertEqual(result[1][0][0], feb_mean)
            self.assertEqual(result.shape, (24, 3, 2))
            # self.assertEqual(result.dims[0], 'month')
        except yaml.YAMLError as exc:
            print(exc)

    def test_yearly_mean(self):
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
            result = functions.yearly_mean(args_file)
            yearly_2010_mean = np.arange(0,365).sum()/365
            yearly_2011_mean = np.arange(365,730).sum()/365
            
            
            self.assertEqual(result[0][0][0], yearly_2010_mean)
            self.assertEqual(result[1][0][0], yearly_2011_mean)
            self.assertEqual(result.shape, (2, 3, 2))          
            
            #The time dimension changes to year only when we use groupby functionality
            #for calculating means.
            #self.assertEqual(result.dims[0], 'year')
        except yaml.YAMLError as exc:
            print(exc)

if __name__ == '__main__':
    unittest.main()

