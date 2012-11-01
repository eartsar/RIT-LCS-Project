import lcs
import cProfile
import sys
from cStringIO import StringIO


def run(lcsMethod, first, second):
    # Generate the profiler command
    # We have to run it in a different python process because cprofile
    # doesn't return string output, it prints. We'll just capture that
    # printed output by piping the output to this procress, then.
    profile_cmd = 'lcsret[0] = lcsMethod("' + first + '","' + second + '")'
    #print 'Sanity Check LCS Result: ', lcsMethod(first, second)
    lcsret = ['']
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    cProfile.runctx(profile_cmd, {'lcsMethod': lcsMethod}, {'lcsret': lcsret})
    lcsret = lcsret[0]
    rcalls = str(lcs.global_rcalls)
    out = mystdout.getvalue()
    sys.stdout = old_stdout
    lines = (out.strip()).split('\n')

    # Get the CPU seconds from this call.
    pre = 0
    if lines[0].find('calls) in ') > 0:
        pre = lines[0].find('calls) in ') + len('calls) in ')
    else:
        pre = lines[0].find('calls in ') + len('calls) in ')
    post = lines[0].find(' second')
    seconds = float(lines[0][pre:post])
    output = '\n' + \
    '===================================================\n' + \
    'Configuration for LCS in ' + str(seconds) + ' CPU seconds.\n' + \
    '  String lengths: S1:' + str(len(first)) + ' S2:' + str(len(second)) + '\n' + \
    '  First:  ' + first + '\n' + \
    '  Second: ' + second + '\n' + \
    '  LCS:    ' + str(lcsret) + '\n' + \
    '  Recursive Calls:  ' + str(rcalls) + '\n' + \
    out + '\n' + \
    '===================================================\n'
    lcs.resetGlobals()
    return seconds, output
