# -*- coding: utf-8 -*-

import cmd

class EasyShell(cmd.Cmd):
  def __init__(self, callback):
    """Setup shell."""
    cmd.Cmd.__init__(self)
    self.prompt = '> '
    self.use_rawinput = True
    self.callback = callback

  def default(self, line):
    if line == 'EOF':
      print ''
      return True
    self.callback(line)

  def do_exit(self, line):
    return True

  def help_exit(self):
    print 'Type exit to quit the shell.'

  def do_help(self, line): self.help_exit()
  def help_help(self): pass
  def emptyline(self): pass
  def run(self): self.cmdloop()
