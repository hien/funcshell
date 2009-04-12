# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Silas Sewell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'silas@sewell.ch (Silas Sewell)'

# Helper functions

def clean(content):
  return content.strip()

def header(content):
  return line('==> %s <==' % content)

def line(content):
  return content + '\n'

# Shell display functions

def get_client(client):
  client = list(client)
  client.sort()
  return clean(line(';'.join(client)))

# Module display functions

def command_exists(results):
  content = ''
  for host, result in results.items():
    content += header(host)
    content += unicode(result)
  return clean(content)

def command_run_item(host, result):
  content = ''
  code = result[0]
  stout = result[1].strip()
  sterr = result[2].strip()
  content += header('%s :: %s' % (host, code))
  if stout and sterr:
    content += line('stout:\n%s\n' % stout)
    content += line('sterr:\n%s' % sterr)
  elif stout:
    content += line(stout)
  elif sterr:
    content += line(sterr)
  return content + '\n'

def command_run(results):
  content = ''
  for host, result in results.items():
    content += command_run_item(host, result)
  return clean(content)
