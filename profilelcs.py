import random
import subprocess
import lcs
import time

print 'Finding length n strings to get close to ~10 seconds computation...'

done = False
n = 1
while not done:
    # generate a random sequence of 0 and 1 characters
    # first = ''.join(random.choice(['0', '1']) for x in range(n))
    # second = ''.join(random.choice(['0', '1']) for x in range(n))

    # use this for benchmarking "fixed" strings
    # this forces the worst case for naive
    first = '0' * n
    second = '1' * n

    # Generate the profiler command
    # We have to run it in a different python process because cprofile
    # doesn't return string output, it prints. We'll just capture that
    # printed output by piping the output to this procress, then.
    profile_cmd = 'lcsret = lcs.naiveGetLCS("' + first + '", "' + second + '")'
    proc = subprocess.Popen(['python', 'subprofile.py', profile_cmd], stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    lines = (out.strip()).split('\n')

    # This is just some interprocess communication nonsense.
    # The delegated process will print out the results we want.
    rcalls = lines[-1][len('#rcalls: '):]
    lcsret = lines[-2][len('#lcsret: '):]

    # Get the CPU seconds from this call.
    pre = lines[0].find('calls) in ') + len('calls) in ')
    post = lines[0].find(' second')
    seconds = float(lines[0][pre:post])

    # Print stuff
    if seconds > 10:
        print ''
        print '==================================================='
        print '                  Target hit!'
        print 'Configuration for Naive LCS in ' + str(seconds) + ' CPU seconds.'
        print '  String lengths: ' + str(n)
        print '  First:  ' + first
        print '  Second: ' + second
        print '  LCS:    ' + lcsret
        print '  Recursive Calls:  ' + str(rcalls)
        print ''

        tail = out.find('#lcsret')
        print out[:tail]
        print '==================================================='
        done = True
    else:
        print 'N(' + str(n) + ')  => ' + str(seconds) + ' CPU seconds'

    n = n + 1
    lcs.resetGlobals()

    # give the threads time to close and clean up
    time.sleep(0.3)
