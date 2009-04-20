# -*- coding: utf-8 -*-

import cly
from func.CommonErrors import Func_Client_Exception
from funcshell.modules import BaseModule
from funcshell.utils import EasyShell

class Command(BaseModule):
  def _grammar(self):
    self.grammar(
      command=cly.Node(help='Module to interact with remote shells')(
        exists=cly.Node(help='Check if a command exists')(
          command=cly.Variable(pattern=r'.*')(
            cly.Action(help='Command name', callback=self.exists),
          ),
        ),
        run=cly.Node(help='Run a command')(
          command=cly.Variable(pattern=r'.*')(
            cly.Action(help='Full command', callback=self.run),
          ),
        ),
        shell=cly.Node(help='Run a command shell')(
          cly.Action(help='Run a command shell', callback=self.shell),
        ),
      ),
    )

  def exists(self, command):
    try:
      result_list = self.client.overlord().command.exists(command)
      for host, result in result_list.items():
        if not self.is_error(result):
          print self.header(host)
          print result
        else:
          self.error(host, result)
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e

  def run(self, command):
    try:
      result_list = self.client.overlord().command.run(command)
      for host, result in result_list.items():
        if not self.is_error(result):
          code, stdin, stderr = result[0], result[1].strip(), result[2].strip()
          print self.header('%s :: %s' % (host, code))
          if stdin and stderr:
            print 'stdin: %s\n\nstderr: %s' % (stdin, stderr)
          elif stdin:
            print stdin
          else:
            print stderr
        else:
          self.error(host, result)
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e

  def shell(self):
    shell = EasyShell(callback=self.run)
    try:
      shell.run()
    except KeyboardInterrupt:
      print ''
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e

def register(shell):
  shell.command = Command(shell.client, shell.grammar)
