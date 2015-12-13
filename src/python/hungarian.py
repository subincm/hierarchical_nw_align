from munkres import Munkres

def Hungarian_algo(cost_matrix):
    best_cluster_pairs = []
    m = Munkres()
    indexes = m.compute(cost_matrix)
    total = 0.0
    for row, column in indexes:
        value = cost_matrix[row][column]
        total += value
        best_cluster_pairs.append((row, column))
        print '(%d, %d) -> %f' % (row, column, value)
    print 'total cost assignment=%d' % total
    return best_cluster_pairs