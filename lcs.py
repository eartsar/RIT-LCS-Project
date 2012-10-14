def dynamicGenerateMatrix(first, second):
    """Generates and returns the LCS matrix for the dynamic programming solution."""

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


def dynamicGetLCS(first, second):
    """
    This function will return the longest common subsequence of two strings,
    using dynamic programming by generating a matrix.

    TODO: Function currently returns the matrix. Use the matrix to get the LCS.
    """
    """
    start at the very end of the dual array
        if the result_matrix[i][j] == result_matrix[i][j-1]
            move up and make recursive call
        if the result_matrix[i][j] == result_matrix[i-1][j]
            move left and make the recursive call
        else
            move diag and concat first[i]
    """
    result_matrix = dynamicGenerateMatrix(first, second)
    return result_matrix


def algorithmB(first, second):
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
        l1 = algorithmB(first[0:i], second)
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
