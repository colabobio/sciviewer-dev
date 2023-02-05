# SCIViewer: Single-cell Interactive Viewer (development version)

This is very experimental code, which will eventually replace the current SCIViewer prototype [here](https://github.com/colabobio/sciviewer).

## How to install

First, make sure the following requirements are met:
* A working installation of Python 3.8 (or later), if you dont have one consider installing [Miniconda](http://conda.pydata.org/miniconda.html).
* An installation of OpenJDK 17, preferrable Eclipse Temurin from [Adoptium](https://adoptium.net/).

Then, follow the next steps:

1. Clone the repo: 

```git clone https://github.com/colabobio/sciviewer-dev.git```

2. Prepare and activate the conda environment containing dependencies for sciviewer-dev:

```
conda env create -n sciviewer-dev -f sciviewer-dev-env.yml 
conda activate sciviewer-dev
```

You should be all set! Use your preferred code editor to develop SCIViewer, you can run the Jupyter notebooks in the test subfolder to debug your changes. These notebook use the autoreload IPython extension to reload modules as you change the code to make the development process easier.

To install the sciviewer-dev package globally on your development computer, please run:

```pip install -e .```

## Quick start

Sciviewer is executed from a Jupyter notebook such as in the examples directory. It is run by initializing a opening the interacive viewer window with some data as input and then embeding the viewer into the notebook (this step should not be required in the future). E.g.

```
import sciviewer as sci
pbmc = sci.datasets.pbmc68k_reduced()
sci.view(pbmc, 500)
sci.embed()
```

Click the video link below for a 50 second demo demonstrating the notebook embedding:
[![Watch the video](https://img.youtube.com/vi/Gir8V1SK7gw/maxresdefault.jpg)](https://youtu.be/Gir8V1SK7gw)

## Packaging SCIViewer

We are following [scVelo](https://github.com/theislab/scvelo/)'s architecture to package SCIViewer as a tool that integrates well with the scanpy ecosystem. Some additional resources on creating Python packages below:

* [Python Packaging User Guide](https://packaging.python.org/en/latest/overview/)
* [Understanding setup.py, setup.cfg and pyproject.toml in Python](https://ianhopkinson.org.uk/2022/02/understanding-setup-py-setup-cfg-and-pyproject-toml-in-python/)
* [What the heck is pyproject.toml?](https://snarky.ca/what-the-heck-is-pyproject-toml/)