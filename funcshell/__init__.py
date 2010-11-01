import copy
import glob
import os
import sys
import cly
import cly.console
try:
    import func.overlord.client as fc
    from func import jobthing
    from func.CommonErrors import Func_Client_Exception
except IOError:
    print 'You do not have the required permissions to run funcshell.'
    sys.exit(1)

class Error(Exception): pass
class ChangeError(Error): pass

class Client(object):

    RUNNING = jobthing.JOB_ID_RUNNING = 0
    FINISHED = jobthing.JOB_ID_FINISHED = 1
    LOST_IN_SPACE = jobthing.JOB_ID_LOST_IN_SPACE = 2
    PARTIAL = jobthing.JOB_ID_PARTIAL = 3

    def __init__(self):
        self.async = False
        self.threads = 1
        self.list = set()
        self.timeout = fc.DEFAULT_TIMEOUT

    def add(self, client_list):
        old_list_len = len(self.list)
        self.list.update(self.minions(client_list))
        if old_list_len == len(self.list):
            raise ChangeError('No clients added.')

    def get(self):
        client_list = list(self.list)
        client_list.sort()
        return client_list

    def join(self, join_str=';'):
        return join_str.join(self.get())

    def minions(self, clients_glob):
        return fc.Minions(clients_glob).get_all_hosts()

    def overlord(self):
        options = {'timeout': self.timeout}
        if self.async:
            options['async'] = self.async
            options['nforks'] = self.threads
        self._overlord = fc.Overlord(self.join(), **options)
        return self._overlord

    def ready(self):
        return bool(self.list)

    def remove(self, client_list):
        old_list_len = len(self.list)
        self.list.difference_update(self.minions(client_list))
        if old_list_len == len(self.list):
            raise ChangeError('No clients removed.')

    def set(self, client_list):
        self.list = set(self.minions(client_list))
        if not self.list:
            raise ChangeError('Set clients list empty.')

class Shell(object):

    def __init__(self):
        self.client = Client()
        self.grammar = cly.Grammar()
        self._grammar()
        self._modules()

    def _grammar(self):
        re_hostname = r'(?:@?[a-zA-Z0-9*]+[a-zA-Z0-9-.\*;]*){1,}'
        self.grammar(
            exit=cly.Node(help='Exit the shell')(
                cly.Action(help='Exit the shell', callback=self.exit),
            ),
            get=cly.Node(help='Get information about the current session')(
                async=cly.Node(help='Get async state')(
                    cly.Action(help='Get async state', callback=self.get_async),
                ),
                clients=cly.Node(help='Get client list')(
                    cly.Action(help='Get client list', callback=self.get_clients),
                ),
                threads=cly.Node(help='Get thread count')(
                    cly.Action(help='Get thread count', callback=self.get_threads),
                ),
                timeout=cly.Node(help='Get timeout')(
                    cly.Action(help='Get timeout', callback=self.get_timeout),
                ),
            ),
            set=cly.Node(help='Define settings for the current session')(
                async=cly.Node(help='Enable or disable async mode')(
                    enabled=cly.Node(help='Enable async mode')(
                        cly.Action(help='Enable async mode', callback=self.enable_async),
                    ),
                    disabled=cly.Node(help='Disable async mode')(
                        cly.Action(help='Disable async mode', callback=self.disable_async),
                    ),
                ),
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
                threads=cly.Node(help='Set thread count')(
                    thread_count=cly.Variable(pattern=r'([0-9]){1,}', help='Set thread count')(
                        cly.Action(help='Set thread count', callback=self.set_threads),
                    ),
                ),
                timeout=cly.Node(help='Set timeout')(
                    timeout=cly.Variable(pattern=r'([0-9]){1,}', help='Set client timeout')(
                        cly.Action(help='Set timeout', callback=self.set_timeout),
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
                cly.console.cerror('%s does not have a register function.' % module.__name__)

    def exit(self):
        sys.exit(0)

    def enable_async(self):
        self.client.async = True

    def disable_async(self):
        self.client.async = False

    def get_async(self):
        if self.client.async:
            state = 'enabled'
        else:
            state = 'disabled'
        print 'async state is %s.' % state

    def add_clients(self, clients_add):
        try:
            self.client.add(clients_add[2:])
        except ChangeError, error:
            cly.console.cwarning(error)

    def get_clients(self):
        if self.client.ready():
            print self.client.join('\n')

    def remove_clients(self, clients_remove):
        try:
            self.client.remove(clients_remove[2:])
        except ChangeError, error:
            cly.console.cwarning(error)

    def set_clients(self, clients_set):
        try:
            self.client.set(clients_set)
        except ChangeError, error:
            cly.console.cwarning(error)

    def get_threads(self):
        print 'Thread count is %s.' % self.client.threads

    def get_timeout(self):
        if self.client.timeout is None:
            print 'Timeout is set to the func default.'
        else:
            print 'Timeout is %s seconds.' % self.client.timeout

    def set_threads(self, thread_count):
        self.client.threads = int(thread_count)

    def set_timeout(self, timeout):
        timeout = int(timeout)
        if timeout <= 0:
            timeout = None
        self.client.timeout = timeout

    def run(self):
        cly.interact(self.grammar, application='funcshell')
