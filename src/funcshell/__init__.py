# -*- coding: utf-8 -*-

import cly
import glob
import os
import sys
try:
  import func.overlord.client as fc
  from func.CommonErrors import Func_Client_Exception
except IOError:
  print 'You do not have the required permissions to run funcshell.'
  sys.exit(1)

class Client(object):
  def __init__(self):
    self.list = set()

  def add(self, client_list):
    self.list.update(self.minions(client_list))

  def get(self):
    client_list = list(self.list)
    client_list.sort()
    return client_list

  def join(self, join_str=';'):
    return join_str.join(self.get())

  def minions(self, clients_glob):
    return fc.Minions(clients_glob).get_all_hosts()

  def overlord(self, hosts=None):
    return fc.Overlord(self.join())

  def ready(self):
    return bool(self.list)

  def remove(self, client_list):
    self.list.difference_update(self.minions(client_list))

  def set(self, client_list):
    self.list = set(self.minions(client_list))

class Shell(object):
  def __init__(self):
    self.client = Client()
    self.grammar = cly.Grammar()
    self._grammar()
    self._modules()

  def _grammar(self):
    re_hostname = r'(?:@?[a-zA-Z0-9*]+[a-zA-Z0-9-.*;]*){1,}'
    self.grammar(
      exit=cly.Node(help='Exit the shell')(
        cly.Action(help='Exit the shell', callback=self.exit),
      ),
      get=cly.Node(help='Get information about the current session')(
        clients=cly.Node(help='Get client list')(
          cly.Action(help='Get client list', callback=self.get_clients),
        ),
      ),
      set=cly.Node(help='Define settings for the current session')(
        clients=cly.Node(help='Manage session clients')(
          clients_set=cly.Variable(pattern=r'%s' % re_hostname, help='Use a host or group name to add clients to the client list')(
            cly.Action(help='Set client list host(s)', callback=self.set_clients),
          ),
          clients_add=cly.Variable(pattern=r'\+\ %s' % re_hostname, help='Use a + before a host or group name to add clients to the client list')(
            cly.Action(help='Add host(s) to client list', callback=self.add_clients),
          ),
          clients_remove=cly.Variable(pattern=r'-\ %s' % re_hostname, help='Use a - before a host or group name to remove clients from the client list')(
            cly.Action(help='Remove host(s) from client list', callback=self.remove_clients),
          ),
        ),
      ),
    )

  def _modules(self):
    module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules')
    module_list_str = glob.glob('%s/[!_]*.py*' % module_dir)
    module_list_str = list(set([os.path.basename(x).split('.py')[0] for x in module_list_str]))
    module_list = __import__('funcshell.modules', globals(), locals(), module_list_str)
    for module_str in module_list_str:
      module = getattr(module_list, module_str)
      try:
        module.register(self)
      except AttributeError:
        print '%s does not have a register function.' % module.__name__

  def exit():
    sys.exit(0)

  def add_clients(self, clients_add):
    self.client.add(clients_add[2:])

  def get_clients(self):
    if self.client.ready():
      print self.client.join('\n')

  def remove_clients(self, clients_remove):
    self.client.remove(clients_remove[2:])

  def set_clients(self, clients_set):
    self.client.set(clients_set)

  def run(self):
    cly.interact(self.grammar, application='funcshell')

def main():
  shell = Shell()
  shell.run()
