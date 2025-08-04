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

# Custom targets for AGT Server documentation
clean:
	rm -rf $(BUILDDIR)/*

html: clean
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

serve: html
	cd $(BUILDDIR)/html && python -m http.server 8000
	@echo "Documentation served at http://localhost:8000"

pdf: clean
	$(SPHINXBUILD) -b latex $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check finished. Look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

spelling:
	$(SPHINXBUILD) -b spelling $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/spelling
	@echo
	@echo "Spell check finished. Look for any errors in the above output " \
	      "or in $(BUILDDIR)/spelling/output.txt."

# Development helpers
dev: html
	@echo "Starting development server..."
	cd $(BUILDDIR)/html && python -m http.server 8000

watch: html
	@echo "Watching for changes..."
	fswatch -o . | xargs -n1 -I {} make html

# ReadTheDocs specific
rtd: html
	@echo "Documentation built for ReadTheDocs" 