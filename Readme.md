# Local wind regime induced by giant linear dunes: comparison of ERA5 re-analysis with surface measurements

This repository contains the codes used to process the data and make the figures present in the research article:

Local wind regime induced by giant linear dunes: comparison of ERA5 re-analysis with surface measurements

> **Note**:
 - the documentation can be found [here](https://cgadal.github.io/GiantDunes/)
 - the corresponding data are available here: <a href="https://doi.org/10.5281/zenodo.6343138"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.6343138.svg" alt="DOI"></a>


## Repository organisation

Briefly, the repository is organized as follow:

  - Paper: article source files (.tex + figures in .pdf)
  - Paper_figure: codes used to produce the paper figures
  - Processing: codes used to process the raw data, and generate the processed data used as input for the codes in `Paper_figure`.
  - python_codes: python codes functions used in the codes present in `Paper_figure` and `Processing`
  - docs: contain the documentation presenting all of this.

## If you want to have an overview of the article and associated codes

The best is to read the article, and then to have a look at the documentation of the repository. You can find it in `docs/_build/html`, or simply [here](https://cgadal.github.io/GiantDunes/).

## If you want to run the codes and re-do the analysis

1. clone/download the whole repository on your computer.
2. download the data here (will be uploaded soon), and unzip it in `static/` to have the following directory tree:

  ```
  static
  │
  └───data
  │   │ AUTHORS.txt
  │   │ ...
  │   │
  │   └───raw_data
  │   │   │   ...
  │   │
  │   └───processed_data
  │   │   │   ...
  │   │
  └───images
  │   ...
  │   ...
  ```
3. run any python codes you want directly from the repository where it is

> **Note**: You may need to install additional python libraries to do so.
