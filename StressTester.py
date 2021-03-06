import profilelcs as profiler
import lcs


def run(lcsMethod, verbose=False):
    done = False
    n = 1

    grow_fast = lcsMethod is not lcs.naiveGetLCS
    while not done:
        # generate a random sequence of 0 and 1 characters
        # first = ''.join(random.choice(['0', '1']) for x in range(n))
        # second = ''.join(random.choice(['0', '1']) for x in range(n))

        # use this for benchmarking "fixed" strings
        # this forces the worst case for naive
        first = '0' * n
        second = '1' * n
        seconds, output = profiler.run(lcsMethod, first, second)
        if seconds > 10:
                print output
                done = True
        else:
                if verbose:
                    print 'N(' + str(n) + ')  => ' + str(seconds) + ' CPU seconds'
                if grow_fast:
                    if n == 1:
                        n = 2
                    elif seconds > 2:
                        n = int((n * max((1 - seconds / 10), 0.1)) + n)
                    else:
                        n = n * 2
                else:
                    n += 1
