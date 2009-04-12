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

import sys
from cly import *
try:
  import func.overlord.client as fc
  from func.CommonErrors import Func_Client_Exception
except IOError:
  print 'You do not have the required permissions to run funcshell.'
  sys.exit(1)
from funcshell import templates

class Shell(object):
  def __init__(self):
    self.client_list = set()

  def __client(self, hosts=None):
    hosts_str = self.__client_list_str(hosts)
    return fc.Overlord(hosts_str)

  def __client_list_str(self, hosts=None):
    if not hosts:
      hosts = self.client_list
    return ';'.join(hosts)

  def __ready(self):
    if not self.client_list:
      print 'Client list required.'
    else:
      return True

  def __handle_error(self, error_type, error_text):
    print 'Error: %s' % error_type
    print error_text

  def get_client(self):
    if self.client_list:
      print templates.render('get_client', self.client_list)

  def set_client(self, client_set):
    self.client_list = set(self.find_minions(client_set))

  def add_client(self, client_add):
    self.client_list.update(self.find_minions(client_add[1:]))

  def remove_client(self, client_remove):
    self.client_list.difference_update(self.find_minions(client_remove[1:]))

  def find_minions(self, client_glob):
    return fc.Minions(client_glob).get_all_hosts()

  def command_exists(self, command):
    if not self.__ready(): return
    client = self.__client()
    try:
      results = client.command.exists(command)
      print templates.render('command_exists', results)
    except Func_Client_Exception, e:
      self.__handle_error(Func_Client_Exception, e)

  def command_run(self, command):
    if not self.__ready(): return
    client = self.__client()
    try:
      results = client.command.run(command)
      print templates.render('command_run', results)
    except Func_Client_Exception, e:
      self.__handle_error(Func_Client_Exception.__name__, e)

def exit():
  sys.exit(0)

def run():
  re_hostname = r'[a-z0-9-.*]+'
  shell = Shell()
  grammar = Grammar(
    exit=Node(help='Exit the shell')(
      Action(help='Exit the shell', callback=exit),
    ),
    get=Node(help='Get information about the current session')(
      client=Node(help='Get client list')(
        Action(help='Get client list', callback=shell.get_client),
      ),
    ),
    set=Node(help='Define settings for the current session')(
      client=Node(help='Manage session clients')(
        client_set=Variable(pattern=r'[@]?%s' % re_hostname, help='Use a host or group name to add clients to the client list')(
          Action(help='Set client list host(s)', callback=shell.set_client),
        ),
        client_add=Variable(pattern=r'\+@?%s' % re_hostname, help='Use a + before a host or group name to add clients to the client list')(
          Action(help='Add host(s) to client list', callback=shell.add_client),
        ),
        client_remove=Variable(pattern=r'-@?%s' % re_hostname, help='Use a - before a host or group name to remove clients from the client list')(
          Action(help='Remove host(s) from client list', callback=shell.remove_client),
        ),
      ),
    ),
    command=Node(help='Module to interact with remote shells')(
      exists=Node(help='Check if a command exists')(
        command=Variable(pattern=r'.*')(
          Action(help='Command name', callback=shell.command_exists),
        ),
      ),
      run=Node(help='Run a command')(
        command=Variable(pattern=r'.*')(
          Action(help='Full command', callback=shell.command_run),
        ),
      ),
    ),
  )
  interact(grammar, application='funcshell')
