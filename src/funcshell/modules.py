from func.CommonErrors import Func_Client_Exception

class Module(object):
  def __init__(self, overlord):
    self.overlord = overlord

  def header(self, text):
    return '==> %s <==' % text

  def is_error(self, result):
    return isinstance(result, list) and result[0] == 'REMOTE_ERROR'

  def error(self, host, result):
    print self.header(host)
    print result[2]

class Command(Module):
  def exists(self, command):
    try:
      result_list = self.overlord().command.exists(command)
      for host, result in result_list.items():
        if not self.is_error(result):
          print self.header(host)
          print result
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e

  def run(self, command):
    try:
      result_list = self.overlord().command.run(command)
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
    from funcshell.utils import CommandShell
    shell = CommandShell(callback=self.run)
    try:
      shell.cmdloop()
    except KeyboardInterrupt:
      print ''
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e
