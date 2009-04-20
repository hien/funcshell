import inspect

class MethodWrapper(object):
  def __init__(self, module, method):
    self.module = module
    self.method = method

  def __call__(self, *args, **kwargs):
    if self.module.client.list:
      try:
        self.method(*args, **kwargs)
      except Exception, e:
        print 'Uncaught module exception: %s' % e
    else:
      print 'Clients required.'

class BaseModule(object):
  def __init__(self, client, grammar):
    self.special_methods = ['header', 'is_error', 'error']
    self.client = client
    self.grammar = grammar
    self._grammar()

  def __getattribute__(self, name):
    value = object.__getattribute__(self, name)
    if inspect.ismethod(value) and not name.startswith('_') and name not in self.special_methods:
      return MethodWrapper(self, value)
    return value

  def header(self, text):
    return '==> %s <==' % text

  def is_error(self, result):
    return isinstance(result, list) and result[0] == 'REMOTE_ERROR'

  def error(self, host, result):
    print self.header(host)
    print result[2]
