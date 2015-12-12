from munkres import Munkres

def Hungarian_algo():
    cost_matrix = [[2,3,3],
                   [3,2,3],
                   [3,3,2]]
    m = Munkres()
    indexes = m.compute(cost_matrix)
    total = 0
    for row, column in indexes:
        value = cost_matrix[row][column]
        total += value
        print '(%d, %d) -> %d' % (row, column, value)
    print 'total profit=%d' % total