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

def main():
  with open('report/source/ot.rst', 'w') as fp:
    fp.write('.. |hr| raw:: html\n')
    fp.write('\n')
    fp.write(' ' * 4 + '<hr />\n')
    fp.write('\n')

    fp.write('OpenTitan formatting status\n')
    fp.write('===========================\n')
    fp.write('\n')

    fp.write('.. toctree::\n')
    fp.write(' ' * 3 + ':maxdepth: 3\n')
    #fp.write(' ' * 3 + ':caption: Contents:\n')
    fp.write('\n')
    fp.write(' ' * 3 + 'otfs\n')
    fp.write(' ' * 3 + 'allow\n')
    fp.write(' ' * 3 + 'wip\n')
    fp.write(' ' * 3 + 'autogen\n')
    fp.write(' ' * 3 + 'todo\n')
    fp.write('\n')

    def write_table_entry(fp, s, n):
      fp.write(s + ' ' * (30 - len(s)) + ' ' + n + '\n')

    write_table_entry(fp, '=' * 30, '=' * 30)
    write_table_entry(fp, 'Fileset', 'Number')
    write_table_entry(fp, '=' * 30, '=' * 30)

    filelist_all = []
    if True:
      with open('file_list_all.txt', 'r') as f:
        for line in f:
          filelist_all.append(line.strip())
      write_table_entry(fp, 'OpenTitan', str(len(filelist_all)))

    filelist_allow = []
    if True:
      with open('file_list_allow.txt', 'r') as f:
        for line in f:
          filelist_allow.append(line.strip())
      write_table_entry(fp, 'Verible-formatted', str(len(filelist_allow)))

    filelist_pending = []
    filelist_pending_prnum = []
    if True:
      with open('file_list_pending.txt', 'r') as f:
        for line in f:
          filelist_pending.append(line.strip().split(':')[0])
          filelist_pending_prnum.append(line.strip().split(':'))
      write_table_entry(fp, 'Work-In-Progress', str(len(filelist_pending)))

    filelist_autogen = []
    if True:
      with open('file_list_autogen.txt', 'r') as f:
        for line in f:
          filelist_autogen.append(line.strip())
      write_table_entry(fp, 'Auto-generated (skipped)', str(len(filelist_autogen)))

    filelist_err = []
    if True:
      with open('file_list_err.txt', 'r') as f:
        for line in f:
          filelist_err.append(line.strip())
      write_table_entry(fp, 'Error', str(len(filelist_err)))


    filelist_todo = []
    if True:
      filelist_todo = filelist_all.copy()

      def remove_from_fileset(fs_a, fs_b):
        for f in fs_b:
          try:
            fs_a.remove(f)
          except ValueError:
            pass

      remove_from_fileset(filelist_todo, filelist_allow)
      remove_from_fileset(filelist_todo, filelist_pending)
      remove_from_fileset(filelist_todo, filelist_autogen)
      remove_from_fileset(filelist_todo, filelist_err)

      write_table_entry(fp, 'TODO', '**' + str(len(filelist_todo)) + '**')

    write_table_entry(fp, '=' * 30, '=' * 30)
    fp.write('\n')

    with open('report/source/otfs.rst', 'w') as f:
      f.write('.. raw:: html\n')
      f.write('\n')
      f.write(' ' * 4 + '<style> .green {color:green; font-weight:bold;} </style>\n')
      f.write('\n')
      f.write('.. role:: green\n')
      f.write('\n')
      f.write('.. raw:: html\n')
      f.write('\n')
      f.write(' ' * 4 + '<style> .red {color:red; font-weight:bold;} </style>\n')
      f.write('\n')
      f.write('.. role:: red\n')
      f.write('\n')
      f.write('.. raw:: html\n')
      f.write('\n')
      f.write(' ' * 4 + '<style> .yellow {color:#cc9900; font-weight:bold;} </style>\n')
      f.write('\n')
      f.write('.. role:: yellow\n')
      f.write('\n')
      f.write('.. raw:: html\n')
      f.write('\n')
      f.write(' ' * 4 + '<style> .blue {color:blue; font-weight:bold;} </style>\n')
      f.write('\n')
      f.write('.. role:: blue\n')
      f.write('\n')

      s = 'OpenTitan fileset (' + str(len(filelist_all)) + ' entries)\n'
      f.write(s)
      f.write('=' * len(s) + '\n')

      filename_len = 0
      for e in filelist_all:
        filename_len = max(len(e), filename_len)

      f.write('=' * filename_len + ' ' + '=' * 10 + '\n')
      f.write('Filename' + ' ' * (filename_len - len('Filename')) + ' ' + 'Status\n')
      f.write('=' * filename_len + ' ' + '=' * 10 + '\n')

      for e in filelist_all:
        f.write(e + ' ' * (filename_len - len(e)) + ' ')
        if e in filelist_allow:
          f.write(':green:`FORMATTED`')
        elif e in filelist_pending:
          f.write(':yellow:`WIP`')
        elif e in filelist_autogen:
          f.write('**Skipped (autogen)**')
        elif e in filelist_todo:
          f.write(':blue:`TODO`')
        elif e in filelist_err:
          f.write(':red:`ERROR`')
        else:
          f.write('Unknown')
        f.write('\n')

      f.write('=' * filename_len + ' ' + '=' * 10 + '\n')
      f.write('\n')

    def write_title(fp, title):
      fp.write(title + '\n')
      fp.write('=' * len(title) + '\n')

    def dump_list(filelist, title, filename):
      with open('report/source/' + filename + '.rst', 'w') as f:
        write_title(f, title + ' (' + str(len(filelist)) + ' entries)')
        f.write('\n')

        fn_len = 0
        for e in filelist:
          fn_len = max(len(e), fn_len)

        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')
        f.write('Filename' + ' ' * (fn_len - len('Filename')) + '\n')
        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')
        for e in filelist:
          f.write(e + ' ' * (fn_len - len(e)) + '\n')
        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')

    dump_list(filelist_todo, 'OpenTitan TODO list', 'todo')
    dump_list(filelist_allow, 'Verible-formatted fileset', 'allow')
    dump_list(filelist_autogen, 'Auto-generated (skipped)', 'autogen')

    def dump_pending_list(filelist, title, filename):
      with open('report/source/' + filename + '.rst', 'w') as f:
        write_title(f, title + ' (' + str(len(filelist)) + ' entries)')
        f.write('\n')

        fn_len = 0
        for e in filelist:
          fn_len = max(len(e[0]), fn_len)

        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')
        f.write('Filename' + ' ' * (fn_len - len('Filename')) + ' ' + 'Pending PR\n')
        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')
        for e in filelist:
          fname = e[0]
          pr = 'https://github.com/lowRISC/opentitan/pull/' + e[1]
          pr = '`' + e[1] + ' <' + pr + '>`_'
          f.write(fname + ' ' * (fn_len - len(fname)) + ' ' + str(pr) + '\n')
        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')

    dump_pending_list(filelist_pending_prnum, 'Work-In-Progress list', 'wip')

  examined = []
  if True:
    from examined import read_examined_fileset
    examined = read_examined_fileset()
    examined_fnames = []
    for e in examined: examined_fnames.append(e['file'])

    examined_confirmed = []
    examined_unconfirmed = []
    examined_bugs = []
    examined_unknown = []

    for e in examined:
      etype = e['type']

      if etype == 'bug':
        examined_bugs.append(e)
      elif etype == 'confirmed':
        examined_confirmed.append(e)
      elif etype == 'unconfirmed':
        examined_unconfirmed.append(e)
      else:
        examined_unknown.append(e)

    def dump_list(filelist, title, filename):
      with open('report/source/' + filename + '.rst', 'w') as f:
        write_title(f, title + ' (' + str(len(filelist)) + ' entries)')
        f.write('\n')

        fn_len = 0
        for e in filelist:
          tmp = ':ref:`' + str(e['file']).replace('/', '_').replace('.', '_') + '`'
          fn_len = max(len(tmp), fn_len)

        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')
        f.write('Filename' + ' ' * (fn_len - len('Filename')) + ' ' + 'Related' + '\n')
        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')
        for e in filelist:
          #f.write(e['file'] + ' ' * (fn_len - len(e['file'])))
          tmp = ':ref:`' + str(e['file']).replace('/', '_').replace('.', '_') + '`'
          f.write(tmp + ' ' * (fn_len - len(tmp)))
          f.write(' ')
          if len(e['issues']) > 0:
            for i in e['issues']:
              num = i.split('/')[-1]
              f.write('`GH#' + str(num) + ' <' + str(i) + '>`_ ')
          if len(e['style_rules']) > 0:
            n = 1
            for i in e['style_rules']:
              f.write('`RULE#' + str(n) + ' <' + i + '>`_ ')
              n = n + 1
          f.write('\n')
        f.write('=' * fn_len + ' ' + '=' * 30 + '\n')
        f.write('\n')

        for e in filelist:
          f.write('.. _' + str(e['file']).replace('/', '_').replace('.', '_') + ':\n')
          f.write('\n')

          f.write(e['file'] + '\n')
          f.write('-' * len(e['file']) + '\n')
          f.write('\n')

          for d in e['desc']:
            f.write(d + '\n')
          f.write('\n')

          def write_note(txt):
            f.write('.. note::\n')
            for l in txt:
              f.write(' ' * 3 + l + '\n')
            f.write('\n')

          if 'issues' in e.keys() and len(e['issues']) > 0:
            txt = []
            txt.append('Related issues:')
            for i in e['issues']:
              txt.append(i)
            write_note(txt)

          if len(e['style_rules']) > 0:
            txt = []
            txt.append('Corresponding style rules:')
            for i in e['style_rules']:
              txt.append(i)
            write_note(txt)

          from utils import verible_format
          vret = verible_format(e['file'])

          if 'err' in vret.keys():
            pass
          else:
            from utils import dump_diff
            dump_diff(f, vret['diff'])

    dump_list(examined_confirmed, 'Correct formatting', 'examined_confirmed')
    dump_list(examined_bugs, 'Incorrect formatting', 'examined_bugs')
    dump_list(examined_unconfirmed, 'Unconfirmed formatting', 'examined_unconfirmed')

if __name__ == "__main__":
  main()
