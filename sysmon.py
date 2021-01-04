import sh

class Command:
    '''
    Basic class for command execution
    '''
    def __init__(self):
        pass
    
    def run(self):
        raise NotImplemented
    def __str__(self):
        raise NotImplemented

class FreeMem(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        free = sh.grep(sh.free('-m'), 'Mem').split()[3]
        print(f'Free memory: {free}')

    def __str__(self):
        return 'freemem'

class Docker(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self)
    
    def run(self):
        c = lambda x: int(sh.wc(sh.docker(x), '-l'))-1
        print(f'Running containers: {c("ps")}')
        print(f'Total containers: {c("images")}')

    def __str__(self):
        return 'docker'
    
def lscpu():
    result = sh.lscpu('--parse=CORE')
    print(f'Total cores {result}')

def process_num():
    result = sh.wc(sh.ps('aux'), '-l')
    print(f'Total processes: {result}')

def disk_space():
    df = lambda output: sh.awk(sh.df("-h", f"--output={output}","--total"), "END {print $1}").rstrip()
    result_free = df('avail')
    result_total = df('size')
    print(f'free disk space {result_free}/{result_total}')

def vmstat():
    print(sh.vmstat())

def pipeline(*args):
    '''
    pipeline defines main method for executing of tasks
    '''
    print(sh.uname('-v'))
    for method in args:
        if not isinstance(method, Command):
            raise Exception('unable to validate method')
        method.run()

pipeline(FreeMem(), Docker())