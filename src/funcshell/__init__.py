# -*- coding: utf-8 -*-

import sys
from cly import *
try:
  import func.overlord.client as fc
  from func.CommonErrors import Func_Client_Exception
except IOError:
  print 'You do not have the required permissions to run funcshell.'
  sys.exit(1)
from funcshell import modules

class Client(object):
  def __init__(self):
    self.list = set()

  def add(self, client_list):
    self.list.update(self.minions(client_list))

  def remove(self, client_list):
    self.list.difference_update(self.minions(client_list))

  def set(self, client_list):
    self.list = set(self.minions(client_list))

  def get(self):
    client_list = list(self.list)
    client_list.sort()
    return client_list

  def join(self, join_str=';'):
    return join_str.join(self.get())

  def overlord(self, hosts=None):
    return fc.Overlord(self.join())

  def ready(self):
    return bool(self.list)

  def minions(self, clients_glob):
    return fc.Minions(clients_glob).get_all_hosts()

class Shell(object):
  def __init__(self):
    self.client = Client()
    self.command = modules.Command(self.client.overlord)

  def get_clients(self):
    if self.client.ready():
      print self.client.join('\n')

  def set_clients(self, clients_set):
    self.client.set(clients_set)

  def add_clients(self, clients_add):
    self.client.add(clients_add[2:])

  def remove_clients(self, clients_remove):
    self.client.remove(clients_remove[2:])

def exit():
  sys.exit(0)

def main():
  re_hostname = r'(?:@?[a-zA-Z0-9*]+[a-zA-Z0-9-.*;]*){1,}'
  shell = Shell()
  grammar = Grammar(
    exit=Node(help='Exit the shell')(
      Action(help='Exit the shell', callback=exit),
    ),
    get=Node(help='Get information about the current session')(
      clients=Node(help='Get client list')(
        Action(help='Get client list', callback=shell.get_clients),
      ),
    ),
    set=Node(help='Define settings for the current session')(
      clients=Node(help='Manage session clients')(
        clients_set=Variable(pattern=r'%s' % re_hostname, help='Use a host or group name to add clients to the client list')(
          Action(help='Set client list host(s)', callback=shell.set_clients),
        ),
        clients_add=Variable(pattern=r'\+\ %s' % re_hostname, help='Use a + before a host or group name to add clients to the client list')(
          Action(help='Add host(s) to client list', callback=shell.add_clients),
        ),
        clients_remove=Variable(pattern=r'-\ %s' % re_hostname, help='Use a - before a host or group name to remove clients from the client list')(
          Action(help='Remove host(s) from client list', callback=shell.remove_clients),
        ),
      ),
    ),
    command=Node(help='Module to interact with remote shells')(
      exists=Node(help='Check if a command exists')(
        command=Variable(pattern=r'.*')(
          Action(help='Command name', callback=shell.command.exists),
        ),
      ),
      run=Node(help='Run a command')(
        command=Variable(pattern=r'.*')(
          Action(help='Full command', callback=shell.command.run),
        ),
      ),
      shell=Node(help='Run a command shell')(
        Action(help='Run a command shell', callback=shell.command.shell),
      ),
    ),
  )
  interact(grammar, application='funcshell')
