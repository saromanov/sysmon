import argparse
import sh

class Command:
    '''
    Basic class for command execution
    '''
    def __init__(self):
        pass
    
    def run(self):
        raise NotImplemented
    def __repr__(self):
        raise NotImplemented

class FreeMem(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        free = sh.grep(sh.free('-m'), 'Mem').split()[3]
        print(f'title("Free memory") {free}')

    def __repr__(self):
        return 'freemem'

class Docker(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        c = lambda x: int(sh.wc(sh.docker(x), '-l'))-1
        print(f'{title("Running containers")} {c("ps")}')
        print(f'{title("Total containers")} {c("images")}')

    def __repr__(self):
        return 'docker'

class Lscpu(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        result = sh.grep('-c', '^processor',  '/proc/cpuinfo')
        print(f'{title("Total cores")} {result}')

    def __repr__(self):
        return 'lscpu'

class ProcessNum(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        result = sh.wc(sh.ps('aux'), '-l')
        print(f'{title("Total processes")} {result}')

    def __repr__(self):
        return 'ps_aux'

class DiskSpace(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        df = lambda output: sh.awk(sh.df("-h", f"--output={output}","--total"), "END {print $1}").rstrip()
        result_free = df('avail')
        result_total = df('size')
        title_text = title('free disk space')
        print(f'{title_text}{result_free}/{result_total}')

    def __repr__(self):
        return 'df_h'

class Vmstat(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        print(sh.vmstat())

    def __repr__(self):
        return 'vmstat'

def title(text):
    '''
        returns colorized title for command
    '''
    return f'\u001b[36m{text}: \u001b[0m'

def pipeline(*args):
    '''
    pipeline defines main method for executing of tasks
    '''
    print(sh.uname('-v'))
    for method in args:
        if not isinstance(method, Command):
            raise Exception('unable to validate method')
        method.run()

commands = [FreeMem(), Docker(), Lscpu(), ProcessNum(), DiskSpace(), Vmstat()]
parser = argparse.ArgumentParser(description='Sysmon')
parser.add_argument('--exclude', action="store", dest="exclude")
parser.add_argument('--include', action="store", dest="include")
parser.add_argument('--names', action="store", dest="names")
args = parser.parse_args()
if args.names:
    for c in commands:
        print(c)
    exit()
if args.include:
    new_commands = [c for c in commands for a in args.include.split(',') if a ==str(c)]
    pipeline(*new_commands)
else:
    pipeline(*commands)