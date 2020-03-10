# Exploratory notebooks and notes

To explore the notebooks in this folder you should do so using [Jupyter nbviewer](https://nbviewer.jupyter.org/github/jmp75/silverpieces/tree/master/notebooks) rather than github.

## Setup

### Linux 

You may need to activate conda using the following command if you did not let your .bahrc be modified by the conda installation

```bash
source ~/anaconda3/bin/activate
```

```bash
# conda update -n base -c defaults conda
my_env_name=sv
```

One off to create the conda environment:

```bash
# if need a clean slate:
# conda env remove --name ${my_env_name}
conda env create -f environment.yml
```

Assuming nodejs already installed from debian repo

```bash
jupyter-labextension install @jupyter-widgets/jupyterlab-manager
jupyter-labextension install jupyter-leaflet
# python3 -m ipykernel install --user --name ${my_env_name} --display-name "Py3 (sv)"
python3 -m ipykernel install --name ${my_env_name} --display-name "Py3 (sv)"
```

## Experimental

I may have a student soon exploring [Voila](https://github.com/QuantStack/voila) 

`conda install -c conda-forge voila`

## start nbk

```bash
conda activate sv
cd $HOME/src/github/silverpieces/ # or...
jupyter-lab .
```

Idea: using [gmaps in notebooks](https://jupyter-gmaps.readthedocs.io/en/latest/install.html#installing-jupyter-gmaps-for-jupyterlab)
