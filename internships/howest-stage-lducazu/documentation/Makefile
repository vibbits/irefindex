.PHONY: all html pdf clean

HTML_FLAGS = --attribute=data-uri --attribute=icons --attribute=iconsdir=/usr/share/asciidoc/images/icons/ \
	     --attribute=experimental --attribute=reproducible --attribute=source-highlighter=rouge \
	     --attribute=toc=left --attribute=toclevels=2

PDF_FLAGS = --attribute=icons --attribute=iconsdir=/usr/share/asciidoc/images/icons/ \
	    --attribute=experimental --attribute=source-highlighter=rouge \
	    --attribute=pdf-themesdir=. --attribute=pdf-theme=pdf-theme.yml \
	    --attribute=title-page --attribute=sectnums

HTML_TGT = etn.html lo.html tdp.html

PDF_TGT = etn.pdf lo.pdf tdp.pdf

%.html : %.adoc
	asciidoctor $(HTML_FLAGS) --backend=html5 --out-file=$@ $<

%.pdf : %.adoc
	asciidoctor-pdf $(PDF_FLAGS) --out-file=$@ $<

html: $(HTML_TGT)

pdf: $(PDF_TGT)

all: html pdf

clean:
	rm -f $(HTML_TGT) $(PDF_TGT)

