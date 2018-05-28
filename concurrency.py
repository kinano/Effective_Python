import os
import subprocess
from time import sleep
import concurrent.futures

def run1():
    proc = subprocess.Popen(['echo', ' Hello' ], stdout=subprocess.PIPE)

    out, err = proc.communicate()
    print out, err



def run2():

    proc = subprocess.Popen(['sleep', '0.01'], stdout=subprocess.PIPE)

    while proc.poll() is None:
        print 'Waiting'

    print proc.poll()

def run_md5(input_stdin):
    print 'calling run_md5'
    sleep(3)
    return subprocess.Popen(
        ['md5sum'],
        stdin=input_stdin,
        stdout=subprocess.PIPE
    )

def run_openssl():
    print 'calling run_openssl'
    for _ in range(3):
        data = os.urandom(10)
        sleep(3)
        env = os.environ.copy()
        env['password'] = 'hahahha'
        proc = subprocess.Popen(
            [
                'openssl',
                'enc',
                '-des3',
                '-pass',
                'env:password'
            ],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        proc.stdin.write(data)
        proc.stdin.flush()
        return proc, run_md5(input_stdin=proc.stdout)

def get_procs():
    print 'get_procs was called'

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        for proc, hash_proc in executor.map(run_openssl):
            yield proc, hash_proc

def test_openssl():
    procs = []
    hash_procs = []

    for proc, hash_proc in get_procs():
        procs.append(proc)
        hash_procs.append(hash_proc)

    print 'Looping through procs'
    for proc in procs:
        out, err = proc.communicate()
        print out

    print 'Looping through hash_procs'
    for hash_proc in hash_procs:
        out, err = hash_proc.communicate()
        print out

