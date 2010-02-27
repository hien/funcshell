import cly
from func.CommonErrors import Func_Client_Exception
from funcshell.modules import BaseModule

class Service(BaseModule):

    def _grammar(self):
        self.grammar(
            service=cly.Node(help='Manage services')(
                service=cly.Variable(pattern=r'\S+', help='Service name')(
                    reload=cly.Node(help='Reload service')(
                        cly.Action(help='Reload service', callback=self.reload),
                    ),
                    restart=cly.Node(help='Restart service')(
                        cly.Action(help='Restart serivce', callback=self.restart),
                    ),
                    start=cly.Node(help='Start service')(
                        cly.Action(help='Start service', callback=self.start),
                    ),
                    status=cly.Node(help='Status service')(
                        cly.Action(help='Get service status', callback=self.status),
                    ),
                    stop=cly.Node(help='Stop service')(
                        stop=cly.Action(help='Stop service', callback=self.stop),
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
            result_list = self.wrap(getattr(self.client.overlord().service, option)(service))
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
            result_list = self.wrap(self.client.overlord().service.get_enabled())
            for host, result in result_list.items():
                if not self.is_error(result):
                    print self.header(host)
                    reformat_result = []
                    for name, levels in result:
                        levels.insert(0, name)
                        reformat_result.append(levels)
                    self.tabularize(['Service', 'Levels', '', '', '', '', '', ''], reformat_result)
                else:
                    self.error(host, result)
        except Func_Client_Exception, e:
            print 'Func exception: %s' % e

    def get_running(self):
        try:
            result_list = self.wrap(self.client.overlord().service.get_running())
            for host, result in result_list.items():
                if not self.is_error(result):
                    print self.header(host)
                    self.tabularize(['Service', 'Status'], result)
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
