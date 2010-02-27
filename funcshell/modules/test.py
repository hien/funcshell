import cly
from func.CommonErrors import Func_Client_Exception
from funcshell.modules import BaseModule

class Test(BaseModule):

    def _grammar(self):
        self.grammar(
            test=cly.Node(help='Run tests')(
                ping=cly.Node(help='Ping clients')(
                    cly.Action(help='Ping clients', callback=self.ping),
                ),
            ),
        )

    def ping(self):
        try:
            result_list = self.wrap(self.client.overlord().test.ping())
            header = ['Client', 'Available']
            content = []
            for host, result in result_list.items():
                if not self.is_error(result):
                    content.append([host, 'yes'])
                else:
                    content.append([host, 'no'])
            self.tabularize(header, content)
        except Func_Client_Exception, e:
            print 'Func exception: %s' % e

def register(shell):
    shell.test = Test(shell.client, shell.grammar)
