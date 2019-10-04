# Exploratory notebooks and notes

To explore the notebooks in this folder you should do so using [Jupyter nbviewer](https://nbviewer.jupyter.org/github/jmp75/silverpieces/tree/master/notebooks) rather than github.

## Setup

per202 - an occasion to also recreate from scratch a conda env. Update documentation.

```bash
source ~/anaconda3/bin/activate
# conda update -n base -c defaults conda
my_env_name=DCX
conda env remove --name ${my_env_name}
conda create -c conda-forge --name ${my_env_name} python=3.7
conda activate ${my_env_name}
conda install -c conda-forge --name ${my_env_name} jupyterlab ipywidgets jupyter requests xarray dask matplotlib netCDF4 pytest seaborn siphon 

conda install -c oggm -c conda-forge --name ${my_env_name} salem  # may be slow to install FYI. Be patient.
# you do need `-c oggm -c conda-forge` otherwise if only oggm there may be a unsatisfied dependency kerfuffle
# optional?
conda install -c conda-forge --name ${my_env_name} rasterio geopandas

# optional? ipyleaflet trials
conda install -c conda-forge --name ${my_env_name} tqdm ipyleaflet

# nodejs already installed from debian repo
jupyter-labextension install @jupyter-widgets/jupyterlab-manager
jupyter-labextension install jupyter-leaflet

# python3 -m ipykernel install --user --name ${my_env_name} --display-name "Py3 (DCX)"
python3 -m ipykernel install --name ${my_env_name} --display-name "Py3 (DCX)"
```

## Experimental

I may have a student soon exploring [Voila](https://github.com/QuantStack/voila) 

`conda install -c conda-forge voila`

## start nbk

```bash
source ~/anaconda3/bin/activate
conda activate DCX
cd $HOME/src/csiro/stash/silverpieces/ # or...
jupyter-lab .
```

Idea: using [gmaps in notebooks](https://jupyter-gmaps.readthedocs.io/en/latest/install.html#installing-jupyter-gmaps-for-jupyterlab)
