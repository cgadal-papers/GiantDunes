# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# cleaning directories form auto summary and sphinx-gallery
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf _autosummary
	rm -rf gen_modules

# cleaning directories form auto summary and sphinx-gallery
clean_hard:
	rm -rf $(BUILDDIR)/*
	rm -rf Paper_figure/
	rm -rf Processing/
	rm -rf _autosummary
	rm -rf gen_modules
	# rm -rf ../static/processed_data/*

# build documentation also for github pages
github:
	@make html
	@cp -a _build/html/. ../docs
