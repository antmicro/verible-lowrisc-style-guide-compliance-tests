# Verible status report utilities

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This project is intended to provide set of scripts needed to analyze how good (or bad) Verible formatted code works.
Data collected by tools are presented as all-in-one-place [report](https://antmicro.github.io/verible-lowrisc-style-guide-compliance-tests/).

The report consists of
1. LowRISC style compliance status
2. OpenTitan formatting status
3. Detailed formatting status for some of OpenTitan files

## Short summary of provided scipts

1. `file_list_pending.py` - generates `file_list_pending.txt` which contains a list of files
                            that might be added to `util/verible-format-allowlist.txt` in the
							OpenTitan [repository](https://github.com/lowrisc/opentitan).
2. `gen_ot_file_lists.py` - generates list of files in an `opentitan/` (local) repository. That filesets
                            are then used by other scripts.
3. `process_fileset.py` - processes TODO fileset and generates intermediate reports, e.g. formatter output diffs
4. `gen_status_pages.py` - generates OpenTitan-related status reports
5. `genindex.py` - generates `index.rst` file (with tools/repos versions)
6. `examined.py` - generates examined files reports (formatting output: style compliant/unconfirmed/incorrect)
7. `utils.py` - utils used by above utils
