#!/usr/bin/python
#
# Copyright (C) 2008 Silas Sewell
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

__author__ = 'silas@sewell.ch (Silas Sewell)'

import cmd, sys
try:
  import func.overlord.client as fc
  from func.CommonErrors import Func_Client_Exception
except IOError:
  print 'You must be root to use Func Shell.'
  sys.exit(1)

def print_result(host, result):
  extra_space = (80-len(host)-3)
  if extra_space > 0:
    extra_line = ' '*(80-len(host)-6)
  else:
    extra_line = ''
  print '='*80
  print '== %s%s ==' % (host, extra_line)
  print '='*80
  print ''
  if result[0]:
    print result[2].strip()
  else:
    print result[1].strip()
  print ''

class FuncShellInterpreter(object):
  """Interpret input."""
  def __init__(self):
    self.client = None

  def handle_command(self, line):
    """Handle commands to send to Func clients."""
    if self.client:
      try:
        results = self.client.command.run(line)
        for host, value in results.items():
          print_result(host, value)
      except Func_Client_Exception:
        print 'No hosts found.'
    else:
      print 'No hosts specified.'

  def get_hosts(self):
    """Display selected hosts."""
    text = ''
    if self.client:
      try:
        minions = self.client.list_minions()
        for minion in minions:
          if text:
            text = '%s\n%s' % (text, minion)
          else:
            text = minion
      except Func_Client_Exception:
        text = 'No hosts found.'
    else:
      text = 'No hosts specified.'
    return text

  def set_use(self, use):
    """Set hosts to use."""
    self.client = fc.Client(use)

class FuncShell(cmd.Cmd):
  """
  Accept input and handle input.
  """
  def __init__(self):
    """Setup shell."""
    cmd.Cmd.__init__(self)
    self.interpreter = FuncShellInterpreter()
    self.prompt = 'fs> '
    self.use_rawinput = True

  def default(self, line):
    """Handle commands not caught by do_* functions."""
    # Catch commands sent to host
    if line.startswith('!'):
      self.interpreter.handle_command(line[1:])
    else:
      # Catch Ctrl+d
      if line == 'EOF':
        print ''
      else:
        print 'Unknown command.'

  def help_exit(self):
    """Display help for exit command."""
    print 'Gracefully exit the shell.'

  def do_exit(self, line):
    """Gracefully exit the shell."""
    self.exit()
    return True

  def help_use(self):
    """Display help for use command."""
    print 'Define hosts to send commands to'
    print '  usage:   use [hosts]'
    print '  example: use web*.example.org'

  def do_use(self, line):
    """Set hosts to send commands to."""
    if line:
      try:
        self.interpreter.set_use(line)
      except Func_Client_Exception:
        print 'No hosts found.'
    else:
      self.help_use()

  def help_get(self):
    """Display help for get command."""
    print 'Display shell options'
    print '  usage:   get [options]'
    print '  example: get hosts'
    print '  Available parameters'
    print '   * hosts - show selected hosts'

  def do_get(self, line):
    """Display shell options."""
    if line == 'hosts':
      try:
        print self.interpreter.get_hosts()
      except:
        print 'No hosts found.'
    else:
      self.help_get()

  def help_help(self):
    """Display help for help command."""
    print 'get command specific help'
    print '  usage:   help [command]'
    print '  example: help use'

  def emptyline(self): pass
  def exit(self): pass

if __name__ == '__main__':
  shell = FuncShell()
  try:
    shell.cmdloop()
  except KeyboardInterrupt:
    print 'exit'
    shell.exit()
