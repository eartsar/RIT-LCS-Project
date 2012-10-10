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
    result_matrix = dynamicGenerateMatrix(first, second)
    return result_matrix
