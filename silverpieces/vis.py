# Temporary location for visualisation aids
# This depends on packages that silverpieces should not require. Will have to move out

import PIL
import numpy as np
from io import StringIO, BytesIO
from base64 import b64encode
import matplotlib.pyplot as plt

def to_embedded_png(xrgrid, cmap=plt.cm.bwr_r):
    '''Convert an xarray 2D Geogrid to URL png display for web browser.
    Derived from Numpy notebook under https://github.com/jupyter-widgets/ipyleaflet/tree/master/examples

    Args:
        xrgrid (xr.DataArray): X-Y data array with dims ('lat', 'lon')
        cmap (matplotlib colormap): colormap. Defaults to red-white-blue

    Returns:
        str: PNG embedded URL; base64
    '''
    web_grid = np.flip(xrgrid.values, 0)
    norm_values = web_grid - np.nanmin(web_grid)
    norm_values = norm_values / np.nanmax(norm_values)
    norm_values = np.where(np.isfinite(web_grid), norm_values, 0)
    web_im = PIL.Image.fromarray(np.uint8(cmap(norm_values)*255))
    acc_mask = np.where(np.isfinite(web_grid), 255, 0)
    mask = PIL.Image.fromarray(np.uint8(acc_mask), mode='L')
    im = PIL.Image.new('RGBA', norm_values.shape[::-1], color=None)
    im.paste(web_im, mask=mask)
    f = BytesIO()
    im.save(f, 'png')
    data = b64encode(f.getvalue())
    data = data.decode('ascii')
    imgurl = 'data:image/png;base64,' + data
    return imgurl

def make_bounds(xrgrid):
    '''Create bounding box definition for a lat/lon xarray grid

    Args:
        xrgrid (xr.DataArray): X-Y data array with dims ('lat', 'lon')

    Returns:
        str: PNG embedded URL; base64
    '''
    lon = xrgrid.lon.values # HACK: hard coded dims
    lat = xrgrid.lat.values
    bottom, left, top, right = (np.min(lat), np.min(lon), np.max(lat), np.max(lon))
    bounds = [(bottom, left), (top, right)]
    return bounds

def center_from_bounds(bounds):
    '''lat/lon center of a bounding box'''
    bottom_left = bounds[0]
    top_right =  bounds[1]
    return [(bottom_left[0]+top_right[0])/2, ((bottom_left[1]+top_right[1]))/2]

