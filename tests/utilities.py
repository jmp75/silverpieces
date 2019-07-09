import sys
import os
import numpy as np
from netCDF4 import Dataset
from tempfile import NamedTemporaryFile


def create_file(d1, d1_name, d2, d2_name, d3, d3_name, val, varname, **args):
    global tmp_file

    try: 
        if os.path.exists(tmp_file.name):
            tmp_file.close()
            os.unlink(tmp_file.name)
    except:
        print(" ")

    tmp_file = NamedTemporaryFile(delete=False)
    fname = tmp_file.name

    # Open the NetCDF file to write
    fw = Dataset(fname, 'w', format='NETCDF4')

    # Create the one-dimension named 'd1_name' and the associated variable
    fw.createDimension(d1_name, len(d1))
    dim_wrt = fw.createVariable(d1_name, d1.dtype, d1_name)
    dim_wrt[:] = d1

    # Create the one-dimension named 'd2_name' and the associated variable
    fw.createDimension(d2_name, len(d2))
    dim_wrt = fw.createVariable(d2_name, d2.dtype, d2_name)
    dim_wrt[:] = d2

    # Create the one-dimension named 'd3_name' and the associated variable
    fw.createDimension(d3_name, len(d3))
    dim_wrt = fw.createVariable(d3_name, d3.dtype, d3_name)
    dim_wrt[:] = d3

    var_wrt = fw.createVariable(varname, val.dtype, (d1_name, d2_name, d3_name), **args)  

    var_wrt = val

    fw.close()
    return tmp_file


def get_data_src(nt=100, ny=100, nx=100):
    t = np.random.uniform(-1, 1, size=nt)
    y = np.random.uniform(-1, 1, size=ny)
    x = np.random.uniform(-1, 1, size=nx)
    #data=np.random.uniform(-1, 1, size=nt*ny*nx)
    data = np.random.randint(0, 100, size=(nt, ny, nx))
    return t, y, x, data

# t,y,x,src_data=get_data_src(nt=2000,ny=100,nx=100)
# f=create_file(t,'t',y,'y',x,'x',src_data,'band')
