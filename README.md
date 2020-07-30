# Silverpieces

![status](https://img.shields.io/badge/status-alpha-red.svg)

Silverpieces is the codename for a general purpose library for processing N-dimensional arrays of data. The primary use case as of 2019-07 is to extract statistical information from multivariate spatial-temporal grids (lat/lon/time), building on top of `xarray`. Silverpieces subscribes to the goals of the [Pangeo](http://pangeo.io) community.

## License

MIT-derived (see [License.txt](./LICENSE.txt))

## Installation

*DRAFT*

In line with the stated intent of major Python scientific libraries, Silverpieces will only aim to run on Python 3.
 
Set up using conda, or

If using pip:

```sh
pip install -r requirements.txt
python setup.py install
```

If using manual method:
```sh
Pull latest version from the repository:
https://github.com/jmp75/silverpieces.git

in \silverpieces, run:
>conda env create -f=./environment.yml

Activate the environment:
>conda activate sv
(where is ‘sv’ is the name configured in ‘environment.yml’)

Then create the wheel:
python setup.py sdist bdist_wheel

The change to the ‘dist’ directory, where the file ‘silverpieces-0.2.0-py2.py3-none-any.whl’ should now be ready:
>pip install silverpieces-0.2.0-py2.py3-none-any.whl


Drop back to ‘silverpieces’ and run:
>jupyter-labextension install @jupyter-widgets/jupyterlab-manager

An error will occur if ‘Node.js’ is not installed.
If so, run:
>conda install -c conda-forge nodejs
(see ‘https://anaconda.org/conda-forge/nodejs’)

Install the manager:
>jupyter-labextension install @jupyter-widgets/jupyterlab-manager

Install the kernel:
>python -m ipykernel install --user --name sv --display-name "Py3 Silverpieces"

And to run notebooks:
>jupyter lab

```
## Documentation

### Example

[Notebooks](./notebooks) provide some examples of usage. You can use:

* Docker, running `docker-compose up` will create a docker container running on jupyter port 8199 containing the examples.
* or manually set up a conda environment in [the notebook readme](./notebooks/Readme.md)

## Related work

Silverpieces started to cater for operations on data cubes that go beyond `xarray` current built-in options. Possibly related work includes:

* [Data Cube Statistics](https://github.com/opendatacube/datacube-stats)
* [Climate Change Initiative (CCI) toolbox](https://cci-tools.github.io/)
* [Earth System Data Cube](https://cablab.readthedocs.io/en/latest/)
* [MetPy](https://unidata.github.io/MetPy/latest/index.html)

