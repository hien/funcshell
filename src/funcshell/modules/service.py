# -*- coding: utf-8 -*-

import cly
from func.CommonErrors import Func_Client_Exception
from funcshell.modules import BaseModule

class Service(BaseModule):
  def _grammar(self):
    self.grammar(
      service=cly.Node(help='Manage services.')(
        start=cly.Node(help='Start service')(
          service=cly.Variable(pattern=r'.*')(
            cly.Action(help='Service name', callback=self.start),
          ),
        ),
        stop=cly.Node(help='Stop service')(
          service=cly.Variable(pattern=r'.*')(
            cly.Action(help='Service name', callback=self.stop),
          ),
        ),
        restart=cly.Node(help='Restart service')(
          service=cly.Variable(pattern=r'.*')(
            cly.Action(help='Service name', callback=self.restart),
          ),
        ),
        reload=cly.Node(help='Reload service')(
          service=cly.Variable(pattern=r'.*')(
            cly.Action(help='Service name', callback=self.reload),
          ),
        ),
        status=cly.Node(help='Get service status')(
          service=cly.Variable(pattern=r'.*')(
            cly.Action(help='Service name', callback=self.status),
          ),
        ),
        get=cly.Node(help='Get information about services')(
          enabled=cly.Node(help='Get a list of services runlevels')(
            cly.Action(help='Get a list of services runlevels', callback=self.get_enabled),
          ),
          running=cly.Node(help='Get a list of running services')(
            cly.Action(help='Get a list of running services', callback=self.get_running),
          ),
        ),
      ),
    )

  def _generic(self, option, service):
    try:
      result_list = getattr(self.client.overlord().service, option)(service)
      for host, result in result_list.items():
        if not self.is_error(result):
          print self.header(host)
          if result == 0:
            print True
          else:
            print False
        else:
          self.error(host, result)
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e

  def get_enabled(self):
    try:
      result_list = self.client.overlord().service.get_enabled()
      for host, result in result_list.items():
        if not self.is_error(result):
          print self.header(host)
          cly.console.print_table(['Service', 'Levels'], result, expand_to_fit=False)
        else:
          self.error(host, result)
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e

  def get_running(self):
    try:
      result_list = self.client.overlord().service.get_running()
      for host, result in result_list.items():
        if not self.is_error(result):
          print self.header(host)
          cly.console.print_table(['Service', 'Status'], result, expand_to_fit=False)
        else:
          self.error(host, result)
    except Func_Client_Exception, e:
      print 'Func exception: %s' % e

  def reload(self, service):
    self._generic('reload', service)

  def restart(self, service):
    self._generic('restart', service)

  def start(self, service):
    self._generic('start', service)

  def status(self, service):
    self._generic('status', service)

  def stop(self, service):
    self._generic('stop', service)

def register(shell):
  shell.service = Service(shell.client, shell.grammar)
