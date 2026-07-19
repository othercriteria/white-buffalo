# White Buffalo - Manuscript Build
#
# Usage:
#   make manuscript    - Compile to single markdown file
#   make pdf           - Compile to PDF
#   make epub          - Compile to EPUB
#   make docx          - Compile to Word document
#   make all           - Build all formats
#   make wordcount     - Show word count
#   make clean         - Remove generated files

TITLE = White Buffalo
OUTPUT_DIR = build
DRAFT_DIR = drafts

# Source files in reading order
SOURCES = $(sort $(wildcard $(DRAFT_DIR)/*.md))

# Pandoc options
PANDOC_OPTS = --from=markdown --standalone
PDF_OPTS = $(PANDOC_OPTS) --pdf-engine=xelatex -V geometry:margin=1in -V fontsize=12pt
EPUB_OPTS = $(PANDOC_OPTS) --toc --toc-depth=1
DOCX_OPTS = $(PANDOC_OPTS) --reference-doc=reference/template.docx 2>/dev/null || $(PANDOC_OPTS)

# Metadata for title page
METADATA = --metadata title="$(TITLE)" \
           --metadata author="Ben Cohen and Daniel Klein"

.PHONY: all book wrap print-interior hooks manuscript pdf epub docx wordcount transcripts clean

all: manuscript pdf epub docx

# The illustrated edition (v1 assembly): plates injected at their text
# anchors per planning/assembly.md. Outputs build/white-buffalo.{pdf,epub}.
book: $(OUTPUT_DIR)
	@python3 assemble.py

# POD production artifacts (DK 2026-07-19). The print interior is the
# POD PDF minus its digital cover leaf (pages 1-2); the wrap's spine
# is sized from that count (cream bulk 0.0025 in/page).
print-interior: book
	@pdfseparate -f 3 build/white-buffalo-pod.pdf 'build/.pi-%d.pdf'
	@pdfunite $$(ls build/.pi-*.pdf | sort -t- -k2 -n) build/white-buffalo-print-interior.pdf
	@rm -f build/.pi-*.pdf
	@pdfinfo build/white-buffalo-print-interior.pdf | grep Pages

wrap: book
	@imagegen/.venv/bin/python imagegen/cover_wrap.py --pages 140 -o build/cover-wrap.png

# Install repo git hooks (pre-commit: rebuild book when drafts/, art/,
# or assemble.py are staged; fails the commit on anchor drift).
hooks:
	@ln -sf ../../scripts/pre-commit .git/hooks/pre-commit
	@echo "Installed .git/hooks/pre-commit -> scripts/pre-commit"

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

manuscript: $(OUTPUT_DIR)
	@echo "Compiling manuscript to markdown..."
	@cat $(SOURCES) > $(OUTPUT_DIR)/manuscript.md
	@echo "Created $(OUTPUT_DIR)/manuscript.md"
	@wc -w $(OUTPUT_DIR)/manuscript.md | awk '{print "Word count:", $$1}'

pdf: $(OUTPUT_DIR)
	@echo "Compiling manuscript to PDF..."
	@pandoc $(SOURCES) $(PDF_OPTS) $(METADATA) -o $(OUTPUT_DIR)/manuscript.pdf
	@echo "Created $(OUTPUT_DIR)/manuscript.pdf"

epub: $(OUTPUT_DIR)
	@echo "Compiling manuscript to EPUB..."
	@pandoc $(SOURCES) $(EPUB_OPTS) $(METADATA) -o $(OUTPUT_DIR)/manuscript.epub
	@echo "Created $(OUTPUT_DIR)/manuscript.epub"

docx: $(OUTPUT_DIR)
	@echo "Compiling manuscript to Word..."
	@pandoc $(SOURCES) $(PANDOC_OPTS) $(METADATA) -o $(OUTPUT_DIR)/manuscript.docx
	@echo "Created $(OUTPUT_DIR)/manuscript.docx"

wordcount:
	@echo "Manuscript word count:"
	@cat $(SOURCES) | wc -w
	@echo ""
	@echo "Per chapter:"
	@wc -w $(SOURCES) | head -n -1 | awk '{printf "  %-40s %5d words\n", $$2, $$1}'

transcripts:
	@echo "Exporting session transcripts to transcripts/..."
	@python3 scripts/export-transcripts.py

clean:
	rm -rf $(OUTPUT_DIR)
