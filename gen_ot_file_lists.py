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

import os

def ot_fileset(top_dir = 'opentitan'):
  filelist_all = []

  for root, dirs, files in os.walk(top_dir):
    #print('r: ' + str(root) + ', d: ' + str(dirs) + ', f: ' + str(files))

    if root.startswith(top_dir + '/hw/vendor') or \
       root.startswith(top_dir + '/hw/top_'):
      continue

    for f in files:
      if not (f.endswith('.sv') or \
              f.endswith('.svh')):
        continue

      tmp = root + '/' + f
      filelist_all.append(tmp[len(top_dir)+1:])

  return filelist_all

def ot_allow_fileset(top_dir = 'opentitan'):
  filelist_allow = []

  with open(top_dir + '/util/verible-format-allowlist.txt', 'r') as fp:
    for e in fp:
      fname = e.strip()

      if len(fname) == 0 or fname[0] == '#':
        continue

      tmp = top_dir + '/' + fname
      filelist_allow.append(tmp[len(top_dir)+1:])

  return filelist_allow

def ot_autogen_fileset(top_dir = 'opentitan'):
  filelist_autogen = []

  for root, dirs, files in os.walk(top_dir):
    for f in files:
      if not f.endswith('.sv.tpl'):
        continue

      tmp = root + '/' + f
      filelist_autogen.append(tmp[len(top_dir)+1:])

  ret = []
  for e in ot_fileset():
    tpl = e + '.tpl'
    if tpl in filelist_autogen:
      ret.append(tpl[:-4])

  return ret

if __name__ == "__main__":
  ot_files = ot_fileset()
  with open('file_list_all.txt', 'w') as fp:
    for e in ot_files:
      fp.write(e + '\n')

  ot_allow = ot_allow_fileset()
  with open('file_list_allow.txt', 'w') as fp:
    for e in ot_allow:
      fp.write(e + '\n')

  ot_autogen = ot_autogen_fileset()
  with open('file_list_autogen.txt', 'w') as fp:
    for e in ot_autogen:
      fp.write(e + '\n')
