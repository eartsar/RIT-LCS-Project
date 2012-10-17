import random
import subprocess
import lcs
import time

print 'Finding length n strings to get close to ~10 seconds computation...'

done = False
n = 1
while not done:
    # generate a sequence of 0 and 1 characters
    first = ''.join(random.choice(['0', '1']) for x in range(n))
    second = ''.join(random.choice(['0', '1']) for x in range(n))

    # Generate the profiler command
    # We have to run it in a different python process because cprofile
    # doesn't return string output, it prints. We'll just capture that
    # printed output.
    profile_cmd = 'lcs.naiveGetLCS("' + first + '", "' + second + '")'
    proc = subprocess.Popen(['python', 'subprofile.py', profile_cmd], stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    lines = (out.strip()).split('\n')

    # Get the CPU seconds from this call
    pre = lines[0].find('calls) in ') + len('calls) in ')
    post = lines[0].find(' second')
    seconds = float(lines[0][pre:post])
    if seconds > 10:
        print 'Configuration for Naive LCS in ' + str(seconds) + ' CPU seconds.'
        print '  String lengths: ' + str(n)
        print '  First:  ' + first
        print '  Second: ' + second
        lcs, depth = lcs.naiveGetLCS(first, second)
        print '  LCS:    ' + lcs
        print '  Recursive Depth:  ' + str(depth)
        print ''
        print out
        done = True
    else:
        print '  ~' + str(seconds) + ' CPU seconds.'

    n = n + 1
    # give the threads time to close and clean up
    time.sleep(0.5)
