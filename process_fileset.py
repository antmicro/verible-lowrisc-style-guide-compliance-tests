#!/usr/bin/env python3
#
# Copyright 2017-2021 The Verible Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file defines helper functions to gather the descriptions of all the
# rules in order to produce documentation (CLI help text and markdown) about
# the lint rules.

import subprocess, difflib, math

def remove_file_subset(filename, filelist):
  with open(filename, 'r') as fp:
    for line in fp:
      try:
        filelist.remove(line.strip())
      except ValueError:
        pass


def format_fileset(filelist):
  count = len(filelist)
  processed = 0

  filelist_err = []
  filelist_change = []

  for f in filelist:
    verible = subprocess.Popen(['./verible/verible-verilog-format',
                                '--formal_parameters_indentation=indent',
                                '--named_parameter_indentation=indent',
                                '--named_port_indentation=indent',
                                '--port_declarations_indentation=indent',
                                'opentitan/' + f],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdout, stderr = verible.communicate()
    if len(stderr) > 0:
      #tmp = []
      #for l in stderr.decode().split('\n'):
      #  tmp.append(l)
      #filelist_err.append((f, [tmp]))
      filelist_err.append((f, stderr.decode().split('\n')))
    else:
      with open('opentitan/' + f, 'r') as fp:
        orig = fp.read()

        formatted = []
        for l in stdout.decode().split('\n'):
          formatted.append(l)

        n = 0
        n_sep = 0;
        changes = []
        n_add = 0
        n_sub = 0
        for l in difflib.unified_diff(orig.split('\n'),
                                      stdout.decode().split('\n'),
                                      lineterm='', n=3):
          n = n + 1
          changes.append(l)
          if len(l) >= 1 and l[0] == '@':
            n_sep = n_sep + 1
          elif len(l) >= 2 and l[0] == '+' and l[1] != '+':
            n_add = n_add + 1
          elif len(l) >= 2 and l[0] == '-' and l[1] != '-':
            n_sub = n_sub + 1

        syntax = []
        if False:
          verible = subprocess.Popen(['./verible/verible-verilog-syntax',
                                      '--printtree',
                                      'opentitan/' + f],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

          stdout, stderr = verible.communicate()
          for l in stdout.decode().split('\n'):
            syntax.append(l)

        org = []
        for l in orig.split('\n'):
          org.append(l)

        filelist_change.append(\
          (n, f, changes, n_sep, n_add, n_sub,\
          math.ceil((n_add+n_sub)/2),\
          syntax, org, formatted))

    processed = processed + 1
    print('\rProcessed: ' + str(processed) + ' / ' + str(count), end='')

  print('')

  if len(filelist_err) > 0:
    with open('file_list_err.txt', 'w') as fp:
      for f in filelist_err:
        fp.write(f[0] + '\n')

  #with open('file_list_changes.txt', 'w') as fp:
  #  for f in filelist_change:
  #    if skip(f): continue

  #    fp.write('fn:' + str(f[0]) + ':' + str(f[3]) + ':' + f[1] + ':' + str(f[4]) + ':' + str(f[5]) + ':' + str(f[6]) + '\n')
  #    if f[0] > 0:
  #      for l in f[2][2:]:
  #        fp.write(l + '\n')

  if True:
    with open('report/source/verible_zero_effort.rst', 'w') as fp:
      fp.write('.. |hr| raw:: html\n')
      fp.write('\n')
      fp.write(' ' * 4 + '<hr />\n')
      fp.write('\n')

      s = 'OpenTitan no-change fileset (' + str(len([x for x in filelist_change if x[6] == 0])) + ' entries)'
      fp.write(s + '\n')
      fp.write('=' * len(s) + '\n')

      filename_len = 0
      for f in filelist_change:
        filename = f[1]
        filename_len = max(len(f[1]), filename_len)

      fp.write('=' * filename_len + ' ' + '=' * 10 + '\n')
      fp.write('Filename' + ' ' * (filename_len - len('Filename')) + ' ' + 'Status\n')
      fp.write('=' * filename_len + ' ' + '=' * 10 + '\n')

      for f in filelist_change:
        lines = f[6]
        sections = f[3]
        diff = f[2]
        filename = f[1]

        if lines > 0: continue

        fp.write(filename + ' ' * (filename_len - len(filename)) + ' ')
        fp.write('lines: ' + str(lines) + ', sections: ' + str(sections));
        fp.write('\n')

      fp.write('=' * filename_len + ' ' + '=' * 10 + '\n')
      fp.write('\n')

  def skip(t):
    lines = t[6]
    sections = t[3]
    diff = t[2]
    filename = t[1]

    if lines > 1 or sections > 1 or lines == 0 or sections == 0:
      return True

    return False

  if False:
    with open('report/source/verible.rst', 'w') as fp:
      fp.write('.. |hr| raw:: html\n')
      fp.write('\n')
      fp.write(' ' * 4 + '<hr />\n')
      fp.write('\n')

      fp.write('OpenTitan low-effort TODO fileset\n')
      fp.write('=================================\n')
      fp.write('\n')

      #fp.write('.. toctree::\n')
      #fp.write(' ' * 3 + ':maxdepth: 1\n')
      #fp.write(' ' * 3 + ':caption: Contents:\n')
      #fp.write('\n')

      filename_len = 0
      for f in filelist_change:
        filename = f[1]
        filename_len = max(len(f[1]), filename_len)

      fp.write('=' * filename_len + ' ' + '=' * 10 + '\n')
      fp.write('Filename' + ' ' * (filename_len - len('Filename')) + ' ' + 'Status\n')
      fp.write('=' * filename_len + ' ' + '=' * 10 + '\n')

      for f in filelist_change:
        lines = f[6]
        sections = f[3]
        diff = f[2]
        filename = f[1]

        if skip(f): continue

        fp.write(filename + ' ' * (filename_len - len(filename)) + ' ')
        fp.write('lines: ' + str(lines) + ', sections: ' + str(sections));
        #if skip(f):
        #  fp.write('Skipping')
        #else:
        #  fp.write('Format')
        fp.write('\n')

      fp.write('=' * filename_len + ' ' + '=' * 10 + '\n')
      fp.write('\n')

      for f in filelist_change:
        lines = f[6]
        sections = f[3]
        diff = f[2]
        filename = f[1]

        if skip(f): continue

        fp.write(filename + '\n')
        fp.write('-' * len(filename) + '\n')
        fp.write('\n')
        fp.write('.. code-block:: diff\n')
        fp.write('\n')
        for l in diff[2:]:
          fp.write(' ' * 3 + l + '\n')

        fp.write('\n')

  if False:
    with open('report/source/next.rst', 'w') as fp:
      fp.write('.. |hr| raw:: html\n')
      fp.write('\n')
      fp.write(' ' * 4 + '<hr />\n')
      fp.write('\n')

      from examined import read_examined_fileset
      examined = read_examined_fileset()
      examined_fnames = []
      for e in examined: examined_fnames.append(e['file'])

      def skip(t):
        lines = t[6]
        sections = t[3]
        diff = t[2]
        filename = t[1]

        if lines > 10 or sections != 1: return True

        if lines == 0: return True
        if filename in examined_fnames: return True

        return False

      n_files = 0
      for n in filelist_change:
        if skip(n): continue
        n_files = n_files + 1

      s = 'OpenTitan examine fileset (' + str(n_files) + ' entries)\n'
      fp.write(s)
      fp.write('=' * len(s) + '\n')
      fp.write('\n')

      filename_len = 0
      for f in filelist_change:
        filename = f[1]
        s = ':ref:`next_' + filename.replace('/', '_').replace('.', '_') + '`'
        filename_len = max(len(s), filename_len)

      fp.write('=' * filename_len + ' ' + '=' * 40 + '\n')
      fp.write('Filename' + ' ' * (filename_len - len('Filename')) + ' ' + 'Status\n')
      fp.write('=' * filename_len + ' ' + '=' * 40 + '\n')

      for f in filelist_change:
        lines = f[6]
        sections = f[3]
        diff = f[2]
        filename = f[1]

        if skip(f): continue

        s = ':ref:`next_' + filename.replace('/', '_').replace('.', '_') + '`'
        fp.write(s + ' ' * (filename_len - len(s)) + ' ')
        fp.write('lines: ' + str(lines) + ', sections: ' + str(sections));
        fp.write('\n')

      fp.write('=' * filename_len + ' ' + '=' * 40 + '\n')
      fp.write('\n')

      for f in filelist_change:
        lines = f[6]
        sections = f[3]
        diff = f[2]
        filename = f[1]
        syntax = f[7]
        orig = f[8]
        formatted = f[9]

        if skip(f): continue

        fp.write('.. _next_' + filename.replace('/', '_').replace('.', '_') + ':' + '\n')
        fp.write('\n')

        fp.write(filename + '\n')
        fp.write('-' * len(filename) + '\n')
        fp.write('\n')
        fp.write('.. code-block:: diff\n')
        fp.write('\n')
        for l in diff[2:]:
          fp.write(' ' * 3 + l + '\n')

        fp.write('\n')

        if False:
          fp.write('.. toggle-header::\n')
          fp.write(' ' * 3 + ':header: **Show/hide original file (' + str(len(orig)) + ' lines)**\n')
          fp.write('\n')

          fp.write(' ' * 3 + '.. code-block:: systemverilog\n')
          fp.write('\n')
          for l in orig:
            fp.write(' ' * 6 + str(l) + '\n')

          fp.write('\n')

        if False:
          fp.write('.. toggle-header::\n')
          fp.write(' ' * 3 + ':header: **Show/hide formatted file (' + str(len(formatted)) + ' lines)**\n')
          fp.write('\n')

          fp.write(' ' * 3 + '.. code-block:: systemverilog\n')
          fp.write('\n')
          for l in formatted:
            fp.write(' ' * 6 + str(l) + '\n')

          fp.write('\n')

        if len(syntax) > 0:
          fp.write('.. toggle-header::\n')
          fp.write(' ' * 3 + ':header: **Show/hide syntax tree (' + str(len(syntax)) + ' lines)**\n')
          fp.write('\n')

          fp.write(' ' * 3 + '.. code-block::\n')
          fp.write('\n')
          for l in syntax:
            fp.write(' ' * 6 + str(l) + '\n')

          fp.write('\n')

        fp.write('|hr|\n')
        fp.write('\n')

  if True:
    with open('report/source/error.rst', 'w') as fp:
      fp.write('.. |hr| raw:: html\n')
      fp.write('\n')
      fp.write(' ' * 4 + '<hr />\n')
      fp.write('\n')

      s = 'OpenTitan error fileset (' + str(len(filelist_err)) + ' entries)'
      fp.write(s + '\n')
      fp.write('=' * len(s) + '\n')
      fp.write('\n')

      filename_len = 0
      for f in filelist_err:
        tmp = ':ref:`error_' + str(f[0]).replace('/', '_').replace('.', '_') + '`'
        filename_len = max(len(tmp), filename_len)

      fp.write('=' * filename_len + ' ' + '=' * 30 + '\n')
      fp.write('Filename' + ' ' * (filename_len - len('Filename')) + ' ' + 'Type\n')
      fp.write('=' * filename_len + ' ' + '=' * 30 + '\n')

      for f in filelist_err:
        filename = f[0]

        #fp.write(filename + ' ' * (filename_len - len(filename)) + ' ')
        tmp = ':ref:`error_' + str(filename).replace('/', '_').replace('.', '_') + '`'
        fp.write(tmp + ' ' * (filename_len - len(tmp)) + ' ')
        err_str = str(f[1])

        if 'syntax error' in err_str:
          fp.write('Syntax error')
        elif 'lexically different' in err_str:
          fp.write('Lexically different')
        elif 'Check failed' in err_str:
          if 'verilog::formatter::TabularAlignTokenPartitions()' in err_str:
            fp.write('Internal bug (align)')
          else:
            fp.write('Internal bug')
        else:
          fp.write('Unknown')
        fp.write('\n')

      fp.write('=' * filename_len + ' ' + '=' * 30 + '\n')
      fp.write('\n')

      for f in filelist_err:
        filename = f[0]

        fp.write('.. _error_' + str(filename).replace('/', '_').replace('.', '_') + ':\n')
        fp.write('\n')

        fp.write(filename + '\n')
        fp.write('-' * len(filename) + '\n')
        fp.write('\n')
        fp.write('.. code-block::\n')
        fp.write('\n')
        for l in f[1]:
          fp.write(' ' * 3 + l + '\n')

        fp.write('\n')


def main():
  filelist = []

  with open('file_list_all.txt', 'r') as fp:
    for line in fp:
      filelist.append(line.strip())

  for f in ['file_list_allow.txt',
            'file_list_autogen.txt']:
    remove_file_subset(f, filelist)

  with open('file_list_pending.txt', 'r') as fp:
    for line in fp:
      try:
        fn = line.strip().split(':')[0]
        filelist.remove(fn)
      except ValueError:
        pass

  with open('file_list_todo.txt', 'w') as fp:
    for f in filelist:
      fp.write(f + '\n');

  format_fileset(filelist)


if __name__ == "__main__":
  main()
