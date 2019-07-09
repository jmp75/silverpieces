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

    var_wrt = fw.createVariable(
        varname, val.dtype, (d1_name, d2_name, d3_name), **args)

    var_wrt = val

    fw.close()
    return tmp_file


def get_data_src_random(nt=365, nx=100, ny=100):
    t = np.random.uniform(-1, 1, size=nt)
    x = np.random.uniform(-1, 1, size=nx)
    y = np.random.uniform(-1, 1, size=ny)
    #data=np.random.uniform(-1, 1, size=nt*ny*nx)
    data = np.random.randint(0, 100, size=(nt, nx, ny))
    return t, x, y, data


def get_data_src(nt=365, nx=2, ny=2):
    t = np.arange(nt)
    x = np.arange(nx)
    y = np.arange(ny)
    data = np.arange(nt*nx*ny).reshape(nt, nx, ny)
    for i in range(nt):
        data[i] = np.linspace(i,i,num=nx*ny).reshape(nx, ny)
    return t, x, y, data

# t,y,x,src_data=get_data_src(nt=2000,ny=100,nx=100)
# f=create_file(t,'t',y,'y',x,'x',src_data,'band')
#suppose you want to generate 4 days worth of data. For each day, the values would be a 2 X 2 matrix
# a = np.arange(16).reshape(4, 2,2)
# for x in range(4):
#     a[x] = np.linspace(x,x,num=4).reshape(2,2)

# np.linspace(0,0,num=4)