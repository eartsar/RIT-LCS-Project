import profilelcs as profiler


def run(lcsMethod, verbos=False):
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
        seconds, output = profiler.run(lcsMethod, first, second)
    if seconds > 10:
            print output
            done = True
    else:
            if verbos:
                print 'N(' + str(n) + ')  => ' + str(seconds) + ' CPU seconds'
            n += 1
