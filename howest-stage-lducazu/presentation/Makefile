.PHONY: all clean

HTML_FLAGS =

HTML_TGT = preso.html

%.html : %.adoc
	asciidoctor-revealjs $(HTML_FLAGS) --out-file=$@ $<

all: $(HTML_TGT)

clean:
	rm -f $(HTML_TGT)

