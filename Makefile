QUIET ?= @

all::
	$(QUIET)true

define sphinx_conf
import sphinx_rtd_theme

project = 'Verible status report'
copyright = '2017-2021, The Verible Authors'
author = 'The Verible Authors'

exclude_patterns = []

extensions = [ "sphinx_rtd_theme", "sphinxcontrib.contentui" ]

html_theme = 'sphinx_rtd_theme'
endef

export sphinx_conf

report/.dir:
	mkdir report && touch $@

report/source/.dir: report/.dir
	mkdir report/source && touch $@

report/source/conf.py: report/source/.dir
	echo "$$sphinx_conf" > $@

report/source/index.rst: report/source/.dir genindex.py
	./genindex.py

report/source/style.rst: ./verible/verible-verilog-style-tester
	./verible/verible-verilog-style-tester \
		--dump_header --dump_internal > $@

file_list_pending.txt: file_list_pending.py
	./$<

file_list_all.txt: gen_ot_file_lists.py
	./$<

report-prep: report/source/.dir \
				process_fileset.py \
				gen_status_pages.py \
				file_list_pending.txt \
				file_list_all.txt \
				report/source/index.rst \
				report/source/conf.py \
				report/source/style.rst
	./process_fileset.py
	./gen_status_pages.py

.ONESHELL:
venv/bin/activate:
	virtualenv venv
	. venv/bin/activate
	pip3 install \
		sphinx_rtd_theme \
		sphinxcontrib.contentui

.ONESHELL:
report-gen-html: venv/bin/activate
	. venv/bin/activate
	LANG=C LC_ALL=C sphinx-build -M html report/source/ report/

all:: report-prep report-gen-html
	[ -d publish ] && rsync -a --delete-after \
								--exclude='.git/' \
								--exclude='.nojekyll' \
								./report/html/. ./publish/.

clean::
	rm -f file_list_all.txt
	rm -f file_list_allow.txt
	rm -f file_list_autogen.txt
	rm -f file_list_err.txt
	rm -f file_list_todo.txt
	rm -rf report

distclean:: clean
	rm -f file_list_pending.txt
	rm -rf __pycache__ venv
	#rm -rf verible opentitan
