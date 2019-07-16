import sys
import os
import time
import numpy as np
from netCDF4 import Dataset
from tempfile import NamedTemporaryFile
import hashlib

def create_file(d1, d1_name, d2, d2_name, d3, d3_name, val, varname, year=2010, **args):
    try:
        hash = hashlib.sha1()
        hash.update(str(time.time()).encode('utf-8'))

        root_dir = os.path.join(os.path.dirname(__file__),'testdata')
        filename = 'TestData_%s.nc' % hash.hexdigest()[:10]
        filename = os.path.join(root_dir,filename)

        with Dataset(filename, 'w', format='NETCDF4') as fw:
            fw.createDimension(d1_name, None)  # len(d1))
            dim_wrt = fw.createVariable(d1_name, d1.dtype, d1_name)
            dim_wrt.units = 'days since %s-01-01 00:00:00' % year
            dim_wrt.calendar = 'gregorian'
            dim_wrt[:] = d1

            fw.createDimension(d2_name, len(d2))
            dim_wrt = fw.createVariable(d2_name, d2.dtype, d2_name)
            dim_wrt.units = 'degree_north'
            dim_wrt[:] = d2

            fw.createDimension(d3_name, len(d3))
            dim_wrt = fw.createVariable(d3_name, d3.dtype, d3_name)
            dim_wrt.units = 'degree_east'
            dim_wrt[:] = d3

            var_wrt = fw.createVariable(varname, val.dtype, (d1_name, d2_name, d3_name), **args)
            var_wrt[:, :, :] = val

            fw.description = 'insignificant dummy data'
            fw.history = 'Created ' + time.ctime(time.time())
            fw.source = 'Stats unit test app'

        return filename
    except Exception as ex:
        print(ex)
        os.unlink(filename)
        raise


def get_data_src_random(nt=365, nx=100, ny=100):
    t = np.random.uniform(-1, 1, size=nt)
    x = np.random.uniform(-1, 1, size=nx)
    y = np.random.uniform(-1, 1, size=ny)
    #data=np.random.uniform(-1, 1, size=nt*ny*nx)
    data = np.random.randint(0, 100, size=(nt, nx, ny))
    return t, x, y, data


def get_data_src_seq(nt=365, nx=3, ny=2):
    t = np.arange(nt)
    x = np.arange(nx)
    y = np.arange(ny)
    data = np.arange(nt*nx*ny).reshape(nt, nx, ny)
    for i in range(nt):
        data[i] = np.linspace(i, i, num=nx*ny).reshape(nx, ny)
    return t, x, y, data


def get_spatial_data_src_seq(t, lat_start=0, lat_end=10, lat_size=11, lon_start=1, lon_end=10, lon_size=11):
    nt = len(t)
    x = np.linspace(lat_start, lat_end, num=lat_size)
    y = np.linspace(lon_start, lon_end, num=lon_size)
    nx = lat_size
    ny = lon_size
    data = np.arange(nt*nx*ny).reshape(nt, nx, ny)
    for i in range(nt):
        data[i] = np.linspace(i, i, num=nx*ny).reshape(nx, ny)
    return t, x, y, data


def read_var(filename, varname):
    with Dataset(filename, 'r', format='NETCDF4') as fr:
        out = fr[varname][:]
    return out


# def link_var(filename, varname):
#     fr = Dataset(filename, 'r', format='NETCDF4')
#     return fr[varname]

# t,x,y,src_data=get_data_src(nt=5,nx=3,ny=2)
# f=create_file1(t,'t',x,'latitude',y,'longitude',src_data,'band')
# suppose you want to generate 4 days worth of data. For each day, the values would be a 2 X 2 matrix
# a = np.arange(16).reshape(4, 2,2)
# for x in range(4):
#     a[x] = np.linspace(x,x,num=4).reshape(2,2)

# np.linspace(0,0,num=4)
