import cmd

class EasyShell(cmd.Cmd):

    def __init__(self, callback, prompt='> '):
        cmd.Cmd.__init__(self)
        self.callback = callback
        self.prompt = prompt
        self.use_rawinput = True

    def default(self, line):
        if line == 'EOF':
            print ''
            return self.do_exit(line)
        self.callback(line)

    def do_exit(self, line):
        return True

    def do_help(self, line):
        self.help_exit()

    def emptyline(self):
        pass

    def help_exit(self):
        print 'Type exit to quit the shell.'

    def help_help(self):
        pass

    def run(self):
        self.cmdloop()
