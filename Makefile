SLUG = subs

SLIDE_HTML = $(SLUG).html
ZIP_FILE = $(SLUG).zip

SUPPORT = lineselect.js slides.js slides.css typogr.min.js
IMAGES = *.jpg *.png
VENDOR = slippy highlight

.PHONY: $(SLIDE_HTML)

default: test slides

test:
	pytest -q

slides: $(SLIDE_HTML)

$(SLIDE_HTML):
	python -m cogapp -r $@

clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -f $(ZIP_FILE)

sterile: clean
	python -m cogapp -x -r $(SLIDE_HTML)

ZIP_EXTRA =

zip $(ZIP_FILE): $(SLIDE_HTML)
	zip -r $(ZIP_FILE) $(SLIDE_HTML) $(SUPPORT) $(IMAGES) $(ZIP_EXTRA) $(VENDOR)
