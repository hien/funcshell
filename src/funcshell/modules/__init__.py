# -*- coding: utf-8 -*-

import cly
import inspect

class MethodWrapper(object):
  def __init__(self, module, method):
    self.module = module
    self.method = method

  def __call__(self, *args, **kwargs):
    if self.module.client.ready():
      try:
        self.method(*args, **kwargs)
      except Exception, e:
        print 'Uncaught module exception: %s' % e
    else:
      print 'Clients required.'

class BaseModule(object):
  def __init__(self, client, grammar):
    self.special_methods = ['error', 'header', 'is_error', 'tabularize']
    self.client = client
    self.grammar = grammar
    self._grammar()

  def __getattribute__(self, name):
    value = object.__getattribute__(self, name)
    if inspect.ismethod(value) and not name.startswith('_') and name not in self.special_methods:
      return MethodWrapper(self, value)
    return value

  def tabularize(self, header, content):
    cly.console.print_table(header, content, auto_format=('', '', ''), expand_to_fit=False)

  def error(self, host, result):
    print self.header(host)
    print result[2]

  def header(self, text):
    return '==> %s <==' % text

  def is_error(self, result):
    return isinstance(result, list) and result[0] == 'REMOTE_ERROR'
