# Exploratory notebooks and notes

## Setup

per202 - an occasion to also recreate from scratch a conda env. Update documentation.

```bash
source ~/anaconda3/bin/activate
# conda update -n base -c defaults conda
my_env_name=DCX
conda create --name ${my_env_name} python=3.7
conda activate ${my_env_name}
conda install --name ${my_env_name} requests xarray dask matplotlib netCDF4 
conda install --name ${my_env_name} seaborn
pip install siphon # not in conda, and wary to tap conda-forge
conda install --name ${my_env_name} jupyterlab ipywidgets jupyter

# nodejs already installed from debian repo
jupyter-labextension install @jupyter-widgets/jupyterlab-manager
#jupyter-labextension install jupyter-threejs

python3 -m ipykernel install --user --name ${my_env_name} --display-name "Py3 (DCX)"
```

## start nbk

```bash
source ~/anaconda3/bin/activate
conda activate DCX
cd $HOME/src/csiro/stash/silverpieces/ # or...
jupyter-lab .
```

Idea: using [gmaps in notebooks](https://jupyter-gmaps.readthedocs.io/en/latest/install.html#installing-jupyter-gmaps-for-jupyterlab)