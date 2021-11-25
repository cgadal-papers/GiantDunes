Processing
==================

Below is the gallery presenting the scripts used to process the data. In each of them, the output data are saved,
and then loaded by the figure scripts to generate the figures of the paper and supplementary information.

.. note::
  As (most) of the scripts store data into the same dictionary, they have to be run in the following order:
    #. Preprocessing of the wind data
    #. Analysis of the DEMs
    #. Calibration of the hydrodynamic roughness
    #. Processing the meteorological data
    #. Time series of the hydrodynamic coefficients

  Note that this is automatically done when building the documentation.
