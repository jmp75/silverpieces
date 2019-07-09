import logging
logging.getLogger().setLevel(logging.DEBUG)
logging.debug('hi from the logger!')

import unittest
import os
import sys
#importing numpy causes debugging to stop working! Actually seems like any C based python packages causes the debugger to fail.
#import numpy as np
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'silverpieces'))
import functions  
from utilities import *

class TestStatMethods(unittest.TestCase):

    def test_dummy(self):
        functions.test()        
        self.assertEqual(1, 1)

    def test_sum(self):        
        time,lat,lon,src_data = get_data_src() 
        f=create_file(time,'time',lat,'lat', lon,'lon',src_data,'band')
        band=read_var(f.name,'band')
        #band=link_var(f.name,'band')
        self.assertEqual(time.size, 365)

if __name__ == '__main__':
    unittest.main()
    