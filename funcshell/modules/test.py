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
                offline=cly.Node(help='Show offline clients')(
                    cly.Action(help='Show offline clients', callback=self.offline),
                ),
                online=cly.Node(help='Show online clients')(
                    cly.Action(help='Show online clients', callback=self.online),
                ),
            ),
        )

    def ping(self, show_yes=True, show_no=True):
        try:
            result_list = self.wrap(self.client.overlord().test.ping())
            header = ['Client', 'Available']
            content = []
            for host, result in result_list.items():
                if not self.is_error(result):
                    content.append([host, 'yes'])
                else:
                    content.append([host, 'no'])
            if show_yes and show_no:
                self.tabularize(header, content)
            else:
                for host, result in content:
                    if (show_yes and result == 'yes') or (show_no and result == 'no'):
                        print host
        except Func_Client_Exception, e:
            print 'Func exception: %s' % e

    def offline(self):
        self.ping(show_yes=False)

    def online(self):
        self.ping(show_no=False)

def register(shell):
    shell.test = Test(shell.client, shell.grammar)
