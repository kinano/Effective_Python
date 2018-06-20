import os
import subprocess
from time import sleep
import concurrent.futures
from functools import wraps
import time

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
            print 'yield {} {}'.format(proc, hash_proc)
            yield proc, hash_proc

def test_openssl():
    # This is broken
    procs = []
    hash_procs = []

    for proc, hash_proc in get_procs():
        procs.append(proc)
        hash_procs.append(hash_proc)

    print 'Looping through procs'
    for proc in procs:
        out, err = proc.communicate()
        print 'proc out {} error {}'.format(out, err)

    print 'Looping through hash_procs'
    for hash_proc in hash_procs:
        out, err = hash_proc.communicate()
        print 'hash_proc out {} error {}'.format(out, err)

def functionTimer(calledFunction):
    """
    Times the provided function and prints the results
    @param calledFunction func
    """
    @wraps(calledFunction)
    def timed(*args, **kwargs):
        functionName = '{}.{}()'.format(
            calledFunction.__module__,
            calledFunction.__name__
        )
        startTime = time.time()
        result = calledFunction(*args, **kwargs)
        elapsedTime = time.time() - startTime
        elapsedTime = int(round(elapsedTime * 1000))
        print('{} took {} milliseconds'.format(functionName, str(elapsedTime)))
        return result

    return timed

# @functionTimer
def gcd(pair):
    a,b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

@functionTimer
def test_gcd_no_pool():
    numbers = [
        (1963309, 2265973),
        (2030677, 3814172),
        (1551645, 2229620),
        (2039045, 2020802)
    ]
    results = list(map(gcd, numbers))
    print 'resuts {}'.format(results)

@functionTimer
def test_gcd_with_threads():
    numbers = [
        (1963309, 2265973),
        (2030677, 3814172),
        (1551645, 2229620),
        (2039045, 2020802)
    ]
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, numbers))
    print 'thread resuts {}'.format(results)

@functionTimer
def test_gcd_with_processes():
    numbers = [
        (1963309, 2265973),
        (2030677, 3814172),
        (1551645, 2229620),
        (2039045, 2020802)
    ]
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, numbers))
    print 'process resuts {}'.format(results)

def test_gcd():
    test_gcd_no_pool()
    test_gcd_with_threads()
    test_gcd_with_processes()
