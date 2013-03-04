SHELL = /bin/sh
PAPER = problemstatement
FIGURES = 
LATEXSRC = problemstatement
LATEX = latex
PDFLATEX = pdflatex
BIBTEX = bibtex
LATEXSW = 
DATADIR = data
FIGDIR = figs
GNUPLOT = gnuplot
CP = cp
PLOTICUS = /usr/local/bin/ploticus -eps -tightcrop
DOT = /usr/local/bin/dot -Tps
MV = mv
BIBS = 
AUXFILES =	aux bbl blg

GRAPHS = $(addsuffix .eps, $(notdir $(basename $(wildcard $(DATADIR)/*.plo))))
GNUPLTGRAPHS = $(addsuffix .eps, $(notdir $(basename $(wildcard $(DATADIR)/$(DATA300)/*.plt))))
DOTGRAPHS = $(addsuffix .ps, $(notdir $(basename $(wildcard $(FIGDIR)/*.dot))))
LATEXSRCFILES = $(addsuffix .tex, $(LATEXSRC))

.SUFFIXES:	.pdf .ps .dvi .tex .eps

default: pdf

compress: $(GRAPHS) $(GNUPLTGRAPHS) $(DOTGRAPHS) $(FIGURES) $(LATEXSRCFILES)
	$(CP) $(PAPER).bbl.compressed $(PAPER).bbl
	$(LATEX) $(PAPER)
	$(LATEX) $(PAPER)
	dvipdf  $(PAPER)


ps: $(PAPER).ps

pdf: $(PAPER).pdf
	open $(PAPER).pdf

$(PAPER).dvi: $(GRAPHS) $(GNUPLTGRAPHS) $(DOTGRAPHS) $(FIGURES) $(LATEXSRCFILES)

%.eps: $(DATADIR)/%.plo
	cd $(DATADIR); $(PLOTICUS) $*.plo -o ../$@

%.eps: $(DATADIR)/%.gp
	cd $(DATADIR); $(GNUPLOT) $*.gp
	$(MV) $(DATADIR)/$@ .

%.ps: $(FIGDIR)/%.dot
	cd $(FIGDIR); $(DOT) $*.dot -o $@

%.pdf: %.dvi
	dvipdf $*

%.ps: %.dvi
	dvips $* -o

%.dvi: %.tex
	$(LATEX) $*
	$(LATEX) $*
	$(LATEX) $*
	$(LATEX) $*

clean:
	$(RM) -f *.aux *.bbl *.blg *.dvi *.log *.out *~
	#cd $(DATADIR); rm -f *~

spotless: clean
	$(RM) -f $(GRAPHS) $(PAPER).ps $(PAPER).pdf
