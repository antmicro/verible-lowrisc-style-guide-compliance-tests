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

def verible_format(filename):
  ret = dict()
  ret['file'] = filename

  verible = subprocess.Popen(['./verible/verible-verilog-format',
                              '--formal_parameters_indentation=indent',
                              '--named_parameter_indentation=indent',
                              '--named_port_indentation=indent',
                              '--port_declarations_indentation=indent',
                              'opentitan/' + filename],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

  stdout, stderr = verible.communicate()
  if len(stderr) > 0:
    ret['err'] = stderr.decode().split('\n')
  else:
    with open('opentitan/' + filename, 'r') as fp:
      orig = fp.read()

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

      ret['diff'] = changes
      ret['n'] = n
      ret['n_sep'] = n_sep
      ret['n_add'] = n_add
      ret['n_sub'] = n_sub
      ret['lines'] = math.ceil((n_add+n_sub)/2)

  return ret


def dump_diff(fp, diff):
  fp.write('.. code-block:: diff\n')
  fp.write('\n')
  for l in diff[2:]:
    fp.write(' ' * 3 + l + '\n')
  fp.write('\n')


def get_auth_token():
  import os, json

  if os.path.exists('local.conf.json'):
    with open('local.conf.json', 'r') as fp:
      conf = json.load(fp)
      if 'auth_token' in conf.keys():
        return conf['auth_token']


if __name__ == '__main__':
  ret = verible_format('hw/dv/sv/tl_agent/dv/env/tl_agent_env_pkg.sv')
  print('ret: ' + str(ret))
