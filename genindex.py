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

import os.path, subprocess

def main():
  with open('report/source/index.rst', 'w') as fp:
    fp.write('.. |hr| raw:: html\n')
    fp.write('\n')
    fp.write(' ' * 3 + '<hr />\n')
    fp.write('\n')
    fp.write('.. |br| raw:: html\n')
    fp.write('\n')
    fp.write(' ' * 3 + '<br />\n')
    fp.write('\n')

    fp.write('Contents\n')
    fp.write('========\n')
    fp.write('\n')

    # Report info
    if True:
      fp.write('.. note::\n')
      fp.write('\n')
      import time
      fp.write(' ' * 3 + 'Generated on ' + str(time.asctime(time.gmtime())) + ' UTC |br|\n')
      fp.write('\n')

    # Verible info
    if True:
      verible = subprocess.Popen(['./verible/verible-verilog-format',
                                  '--version'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
      stdout, stderr = verible.communicate()
      fp.write('.. note::\n')
      fp.write('\n')
      fp.write(' ' * 3 + 'Verible version:\n')
      for l in stdout.decode().split('\n'):
        if len(l) > 0:
          fp.write(' ' * 3 + l + ' |br|\n')
      fp.write('\n')

    # OpenTitan info
    if True:
      import git
      repo = git.Repo('opentitan')
      obj = repo.head.object

      def conv_date(t):
        import time
        return str(time.asctime(time.gmtime(t)))
        #time.strftime("%a, %d %b %Y %H:%M", time.gmtime(t))

      fp.write('.. note::\n')
      fp.write('\n')
      fp.write(' ' * 3 + 'OpenTitan info: |br|\n')
      fp.write(' ' * 3 + 'Commit: ' + obj.hexsha + ' |br|\n')
      fp.write(' ' * 3 + 'Commited date: ' + conv_date(obj.committed_date) + ' |br|\n')
      fp.write(' ' * 3 + 'Authored date: ' + conv_date(obj.authored_date) + ' |br|\n')
      fp.write('\n')

    # Style tester info
    if True:
      verible = subprocess.Popen(['./verible/verible-verilog-style-tester',
                                  '--version'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
      stdout, stderr = verible.communicate()
      fp.write('.. note::\n')
      fp.write('\n')
      fp.write(' ' * 3 + 'Style Tester (Verible) version:\n')
      for l in stdout.decode().split('\n'):
        if len(l) > 0:
          fp.write(' ' * 3 + l + ' |br|\n')
      fp.write('\n')


    fp.write('.. toctree::\n')
    fp.write(' ' * 3 + ':maxdepth: 3\n')
    fp.write('\n')

    subpages = ['ot',
                'style',
                'verible_zero_effort',
                'examined_confirmed',
                'error',
                'examined_bugs',
                'examined_unconfirmed']

    if os.path.isfile('report/source/next.rst'):
      subpages.append('next')

    for e in subpages:
      fp.write(' ' * 3 + e + '\n')


if __name__ == "__main__":
  main()
