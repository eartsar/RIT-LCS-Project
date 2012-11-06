global_rcalls = 0


def resetGlobals():
    global global_rcalls
    global_rcalls = 0


def naiveGetLCS(first, second):
    global global_rcalls

    result = _naiveGetLCS(first, second)
    print '#lcsret: ' + result
    print '#rcalls: ' + str(global_rcalls)
    resetGlobals()


def _naiveGetLCS(first, second):
    """
    This function will return the longest common subsequence between two
    strings using a naive recursive approach with no performance boosts.
    """
    # global to count recursive calls
    global global_rcalls

    # base case
    if len(first) == 0 or len(second) == 0:
        return ''

    # match case
    elif first[-1:] == second[-1:]:
        global_rcalls += 1
        return _naiveGetLCS(first[:-1], second[:-1]) + first[-1:]

    # split case
    else:
        c1 = _naiveGetLCS(first, second[:-1])
        c2 = _naiveGetLCS(first[:-1], second)
        global_rcalls += 2
        if len(c1) >= len(c2):
            return c1
        else:
            return c2


def memoizedGetLCS(first, second):
    global global_rcalls

    result = _memoizedGetLCS(first, second)
    print '#lcsret: ' + result
    print '#rcalls: ' + str(global_rcalls)
    resetGlobals()


def _memoizedGetLCS(first, second):
    """
    This function will return the longest common subsequence between two
    strings using the standard recursive approach with memoization. The
    python dictionary, d, is passed around, holding the results of any
    sub-problem. If d does not contain the subproblem, it gets computed
    and then stored.

    d uses a tuple of (string, string) as a key, and has a string (LCS)
    value.
    """
    d = {}
    result, d = _memoizedGetLCSHelper(first, second, d)
    return result


def _memoizedGetLCSHelper(first, second, d):
    """
    'Inner' recursive function used by memoizedGetLCS()
    The memoization dictionary 'd' is always passed around and updated,
    and as such, should always be passed in as a parameter, and returned.
    The dictionary should never be re-initialized.
    """
    global global_rcalls
    global_rcalls += 1
    if len(first) == 0 or len(second) == 0:
        return '', d
    elif first[-1:] == second[-1:]:
        result, d = _memoizedGetLCSHelper(first[:-1], second[:-1], d)
        return result + first[-1:], d
    else:
        if (first, second[:-1]) in d:
            c1 = d[(first, second[:-1])]
        else:
            c1, d = _memoizedGetLCSHelper(first, second[:-1], d)
            d[(first, second[:-1])] = c1

        if (first[:-1], second) in d:
            c2 = d[(first[:-1], second)]
        else:
            c2, d = _memoizedGetLCSHelper(first[:-1], second, d)
            d[(first[:-1], second)] = c2

        if len(c1) >= len(c2):
            return c1, d
        else:
            return c2, d


def dynamicGetLCS(first, second):
    global global_rcalls

    result = _dynamicGetLCS(first, second)
    print '#lcsret: ' + result
    print '#rcalls: ' + str(global_rcalls)
    resetGlobals()


def _dynamicGetLCS(first, second):
    """
    This function will return the longest common subsequence of two strings,
    using dynamic programming by generating a matrix.
    """
    result_matrix = dynamicGenerateMatrix(first, second)
    done = False

    i = len(second)
    j = len(first)
    result = ''

    while not done:
        if i == 0 or j == 0:
            done = True
        elif first[j - 1] == second[i - 1]:
            result = first[j - 1] + result
            i = i - 1
            j = j - 1
        elif result_matrix[i][j] == result_matrix[i][j - 1]:
            j = j - 1
        elif result_matrix[i][j] == result_matrix[i - 1][j]:
            i = i - 1

    return result


def dynamicGenerateMatrix(first, second):
    """
    This function generates and returns the LCS matrix used in the dynamic
    programming solution. The dimensions of the matrix are len(first) rows
    and len(second) columns.
    """

    # populate the initial matrix
    lcs_matrix = [[None for j in range(len(first) + 1)] for i in range(len(second) + 1)]

    # give a first row header
    for i in range(len(first) + 1):
        lcs_matrix[0][i] = 0

    # give a first column header
    for i in range(len(second) + 1):
        lcs_matrix[i][0] = 0

    # for each element in the matrix, left to right, top to bottom
    for i in range(1, len(second) + 1):
        for j in range(1, len(first) + 1):
            # check to see if the letters match
            if first[j - 1] == second[i - 1]:
                # if so, increment the value from the previous on the diagonal
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
            else:
                # otherwise, take the longer subsequence of the top, or left
                lcs_matrix[i][j] = max(lcs_matrix[i][j - 1], lcs_matrix[i - 1][j])

    # return the LCSm matrix
    return lcs_matrix


def hirshbergGetLCS(first, second):
    global global_rcalls

    result = _hirshbergGetLCS(first, second)
    print '#lcsret: ' + result
    print '#rcalls: ' + str(global_rcalls)
    resetGlobals()


def _hirshbergGetLCS(first, second):
    return algorithmC(first, second)


def algorithmB(first, second):
    """
    Algorithm B for Hirshberg's quadratic time linear space solution to LCS.
    This function will return a single row of the LCS matrix, to be used in
    Hirshberg's algorithm C.
    """
    k = [[0] * (len(second) + 1), [0] * (len(second) + 1)]
    for i in range(1, len(first) + 1):
        temp = k[0]
        k[0] = k[1]
        k[1] = temp
        for j in range(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                k[1][j] = k[0][j - 1] + 1
            else:
                k[1][j] = max(k[1][j - 1], k[0][j])
    return k[1]


def algorithmC(first, second):
    """
    Algorithm C for Hirshberg's quadratic time linear space solution to LCS.
    This function will return the LCS of two strings.
    """
    m = len(first)
    n = len(second)

    # if problem is trivial, solve it
    if n == 0:
        return ""

    # if the first is a single character, and it exists in the second, return it
    elif m == 1:
        if first in second:
            return first
        else:
            return ""

    # otherwise, split the problem
    else:
        i = m // 2
        l1 = algorithmB(first[:i], second)
        l2 = algorithmB(first[i:][::-1], second[::-1])
        r = -1
        jmin = 0
        for j in range(n):
            if l1[j] + l2[n - j] > r:
                r = l1[j] + l2[n - j]
                jmin = j
        k = jmin
        # solving simpler problems
        c1 = algorithmC(first[:i], second[:k])
        c2 = algorithmC(first[i:], second[k:])
        return c1 + c2


def main():
    """
    The main function of this python module. It just tests the various
    functions.
    """

    first = 'AGCAT'
    second = 'GACT'

    print 'First sequence: ' + first
    print 'Second sequence: ' + second
    print ''
    print 'Naive: ' + _naiveGetLCS(first, second)
    print 'Memoized: ' + _memoizedGetLCS(first, second)
    print 'Dynamic: ' + _dynamicGetLCS(first, second)
    print 'Hirshberg: ' + _hirshbergGetLCS(first, second)
    return


if __name__ == '__main__':
    main()
