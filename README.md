# SCIViewer: Single-cell Interactive Viewer (development version)

This is very experimental code, which will eventually replace the current SCIViewer prototype [here](https://github.com/colabobio/sciviewer).

## How to use

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

