FROM continuumio/miniconda
ADD . /app/
WORKDIR /app
RUN curl https://cloudstor.aarnet.edu.au/plus/s/nj2RevvD1EUD77n/download --output tassie_silo_rain.nc
RUN conda env create -f environment.yml
#RUN jupyter-labextension install @jupyter-widgets/jupyterlab-manager
