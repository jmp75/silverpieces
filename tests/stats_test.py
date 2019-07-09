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
import silverpieces.functions  
from utilities import *

class TestStatMethods(unittest.TestCase):

    def test_dummy(self):
        silverpieces.functions.test()        
        self.assertEqual(1, 1)

    def test_sum(self):        
        t,y,x,src_data = get_data_src(nt=2000,ny=100,nx=100)        
        # f=create_file(t,'t',y,'y',x,'x',src_data,'band')
        # print(f.name)
        self.assertEqual(t.size, 2000)

if __name__ == '__main__':
    # import numpy as np
    unittest.main()
    