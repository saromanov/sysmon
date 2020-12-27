import sh

def free_mem():
    free = sh.grep(sh.free('-m'), 'Mem').split()[3]
    return f'Free memory: {free}'