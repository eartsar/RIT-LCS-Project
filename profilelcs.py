import random
import subprocess
import lcs
import time
from optparse import OptionParser


def main():
    parser = OptionParser()
    parser.add_option("-r", "--repeat", dest="repeatnum", default="1", type="int", help="repeat the test a certain number of times")
    parser.add_option("-a", "--algorithm", dest="algchoice", default="ALL", type="string", help="specify an algorithm to profile (NAIVE, MEMO, DP, H, ALL)")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-t", "--target", dest="targettime", default=10, type="int", help="run until computation time exceeds specified")
    parser.add_option("-s", "--sequence", dest="sequencetype", default="BINARY", type="string", help="type of sequence (BINARY, ACGT)")

    (options, args) = parser.parse_args()

    print 'Target Computation Time: ' + options.targettime

    for x in range(options.repeatnum):
        done = False
        n = 1
        while not done:
            # generate a random sequence of 0 and 1 characters
            if options.generate is "RANDOM":
                if options.sequencetype is "BINARY":
                    first = ''.join(random.choice(['0', '1']) for x in range(n))
                    second = ''.join(random.choice(['0', '1']) for x in range(n))
                else:
                    print "option not yet implemented: ACGT"
                    first = ''.join(random.choice(['0', '1']) for x in range(n))
                    second = ''.join(random.choice(['0', '1']) for x in range(n))
            else:
                if options.sequencetype is "BINARY":
                    # use this for benchmarking "fixed" strings
                    # this forces the worst case for naive
                    first = '0' * n
                    second = '1' * n
                else:
                    first = 'A' * n
                    second = 'G' * n

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
            if options.verbose:
                if seconds > targettime:
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


if __name__ == '__main__':
    main()