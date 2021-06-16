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

import pycurl, json
from io import BytesIO 

from utils import get_auth_token

def get_pr_files(pr_url):
  prfiles = list()

  auth_token = get_auth_token()

  i = 1
  while True:
    b_obj = BytesIO()

    crl = pycurl.Curl()

    header = dict()
    header['per_page'] = 100
    header['page'] = i

    url = pr_url + '/files?'
    for h in header:
      url = url + '&' + str(h) + '=' + str(header[h])

    crl.setopt(crl.URL, url)
    crl.setopt(crl.HTTPGET, 1)

    http_header = []
    http_header.append('accept: application/vnd.github.v3+json')
    if auth_token:
      http_header.append('Authorization: token ' + auth_token)
    crl.setopt(crl.HTTPHEADER, http_header)

    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close()
 
    get_body = b_obj.getvalue()
    data = json.loads(get_body.decode('utf8'))

    prfiles = prfiles + [e for e in data]

    i = i + 1

    if len(data) < header['per_page']:
      break

  return prfiles


def get_pr_list():
  prlist = list()

  auth_token = get_auth_token()

  i = 1
  while True:
    b_obj = BytesIO()

    crl = pycurl.Curl()

    header = dict()
    header['per_page'] = 100
    header['page'] = i

    url = 'https://api.github.com/repos/lowrisc/opentitan/pulls?'
    for h in header:
      url = url + '&' + str(h) + '=' + str(header[h])

    crl.setopt(crl.URL, url)
    crl.setopt(crl.HTTPGET, 1)

    http_header = []
    http_header.append('accept: application/vnd.github.v3+json')
    if auth_token:
      http_header.append('Authorization: token ' + auth_token)
    crl.setopt(crl.HTTPHEADER, http_header)

    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform() 
    crl.close()
 
    get_body = b_obj.getvalue()
    data = json.loads(get_body.decode('utf8'))

    for e in data:
      prlist.append(e['url'])

    i = i + 1
    if len(data) < header['per_page']:
      break;

  return prlist


def main():
  allow_list = []

  prlist = get_pr_list()
  for pr in prlist:
    print('Checking PR: ' + str(pr))
    prnum = pr.split('/')[-1]
    prfiles = get_pr_files(pr)

    for e in prfiles:
       if e['filename'] == 'util/verible-format-allowlist.txt':
         for f in e['patch'].split('\n'):
           if f[0] != '+': continue
           allow_list.append(f[1:] + ':' + prnum)

  with open('file_list_pending.txt', 'w') as fp:
    for f in allow_list:
      fp.write(str(f) + '\n')


if __name__ == "__main__":
  main()
