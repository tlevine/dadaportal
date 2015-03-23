import subprocess, sys

SH_MESSAGE = '''You are about to run this command.

    $ %s

Are you sure you want to run it? Hit enter if yes.
'''
def sh(command):
    sys.stdout.write(SH_MESSAGE % command)
    input()
    p = subprocess.Popen(command.split(), stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    p.wait()
    return p.stdout.read()

def direction(command):
    sys.stdout.write(command.strip() + '\n')
    input()

