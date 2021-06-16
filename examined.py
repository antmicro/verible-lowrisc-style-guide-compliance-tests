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

import re, os

def read_examined_fileset():
  examined = []

  p = re.compile(':([a-z]+):[\s+](.*)')

  for root, dirs, files in os.walk('examined/'):
    for f in files:
      if not f.endswith('.txt'):
        continue

      with open(root + f, 'r') as efp:
        entry_type = 'unknown'

        for e in efp:
          l = e.strip()

          #if len(l) == 0: continue
          if len(l) > 0 and (l[0] == '#' or l[0:2] == '//'): continue

          m = p.match(l)
          if m:
            tag = m.group(1)
            if tag == 'otf':
              examined.append(dict())
              examined[-1]['file'] = m.group(2).strip()
              examined[-1]['type'] = entry_type
              examined[-1]['desc'] = []
              examined[-1]['issues'] = []
              examined[-1]['style_rules'] = []
            elif tag == 'bug':
              entry_type = 'bug'
            elif tag == 'unconfirmed':
              entry_type = 'unconfirmed'
            elif tag == 'confirmed':
              entry_type = 'confirmed'
            elif tag == 'issue':
              examined[-1]['issues'].append(m.group(2).strip())
            elif tag == 'style':
              examined[-1]['style_rules'].append(m.group(2).strip())
          else:
            if len(examined) > 0:
              examined[-1]['desc'].append(str(l))

  return examined

if __name__ == "__main__":
  fs = read_examined_fileset()
  for e in fs:
    print(':: ' + str(e))
