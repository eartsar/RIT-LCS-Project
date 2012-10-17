import cProfile
import sys
import lcs

# The point of this script is so that the profiling's output can be captured
# This will get called using subprocess of another script, and its cProfile
# printing will be captured and piped to the high level script.
# It's a bit of a hack, but this is the only built-in profiler that uses CPU
# time instead of normal time.


# define this so my editor doesn't yell at me
lcsret = ''

# the script is given the execution command to profile
# The command looks like this:
#   lcsret = lcs.naiveGetLCS(first, second)

cProfile.run(sys.argv[1])

# Print the returns so they can be captured by subprocess
print '#lcsret: ' + lcsret
print '#rcalls: ' + str(lcs.global_rcalls)
