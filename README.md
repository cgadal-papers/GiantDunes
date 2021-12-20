# Giant_dunes

This GitHub repository contains the data and code used in < > by the authors. This has been set-up to provide a fully reproducible scientific article, and is thus organized in the following way:

- `static/input_data` contains the raw data used in the sudy.
- they are processed by the codes present in `Processing`, and the ouput is saved in `static/output_data`.
- these data are read by the codes in `Paper_figure`, that saves the figures in `Paper/Figures`.
- the .tex of the article is in `Paper`, and directly uses the figures present in `Paper/Figures`.

All codes are documented and annotated, and the ouput is nicely rendered in the form of a html documentation in `docs/_build/html`. To view it, you can simply click here, or clone this repositoy and open docs/_build/html/index.html` (it should open directly in your web brower).
