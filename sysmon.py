import sh

def free_mem():
    free = sh.grep(sh.free('-m'), 'Mem').split()[3]
    return f'Free memory: {free}'

def docker():
    c = lambda x: int(sh.wc(sh.docker(x), '-l'))-1
    print(f'Running containers: {c("ps")}')
    print(f'Total containers: {c("images")}')

def lscpu():
    result = sh.lscpu('--parse=CORE')
    print(f'Total cores {result}')

def process_num():
    result = sh.wc(sh.ps('aux'), '-l')
    print(f'Total processes: {result}')

print(free_mem())
docker()
lscpu()
process_num()