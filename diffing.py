# DO NOT CHANGE THIS CLASS
class DiffingCell:
    def __init__(self, cost, s_char, t_char):
        self.cost = cost
        self.s_char = s_char
        self.t_char = t_char
        self.validate()

    # Helper function so Python can print out objects of this type.
    def __repr__(self):
        return "(%d,%s,%s)"%(self.cost, self.s_char, self.t_char)

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.cost) == int), "cost should be an integer"
        assert(type(self.s_char) == str), "s_char should be a string"
        assert(type(self.t_char) == str), "t_char should be a string"
        assert(len(self.s_char) == 1), "s_char should be length 1"
        assert(len(self.t_char) == 1), "t_char should be length 1"

# Input: a dynamic programming table,  cell index i and j, the input strings s and t, and a cost function cost.
# Should return a DiffingCell which we will place at (i,j) for you.
def fill_cell(table, i, j, s, t, cost):

    if i == 0 and j == 0:
        return DiffingCell(0, ' ', ' ')

    if i == 0:
        return DiffingCell(cost('-', t[j-1]) + table.get(i, j-1).cost, '-', t[j-1])

    if j == 0:
        return DiffingCell(cost(s[i-1], '-') + table.get(i-1, j).cost, s[i-1], '-')

    if s[i-1] == t[j-1]:
        return DiffingCell(table.get(i-1,j-1).cost, s[i-1], t[j-1])

    else:
        options = list()
        options.append((cost(s[i-1], t[j-1]) + table.get(i-1, j-1).cost, s[i-1], t[j-1]))
        options.append((cost(s[i-1], '-') + table.get(i-1, j).cost, s[i-1], '-'))
        options.append((cost('-', t[j-1]) + table.get(i, j-1).cost, '-', t[j-1]))
        options.sort()

        return DiffingCell(options[0][0], options[0][1], options[0][2])

# Input: n and m, the sizes of s and t, respectively.
# Should return a list of (i,j) tuples, the order you would like us to call fill_cell
def cell_ordering(n,m):

    order_list = [(0, 0)]

    # Evaluate first column i == 0
    for j in range(1, m + 1):
        order_list.append((0, j))

    # Evaluate first row j == 0
    for i in range(1, n + 1):
        order_list.append((i, 0))

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            order_list.append((i, j))

    return order_list

# Returns a size-3 tuple (cost, align_s, align_t).
# cost is an integer cost.
# align_s and align_t are strings of the same length demonstrating the alignment.
# See instructions.pdf for more information on align_s and align_t.
def diff_from_table(s, t, table):

    align_s = ""
    align_t = ""

    cur_i, cur_j = len(s), len(t)

    while not(cur_i == 0 and cur_j == 0) and cur_i >= 0 and cur_j >= 0:
        s_char = table.get(cur_i, cur_j).s_char
        t_char = table.get(cur_i, cur_j).t_char

        align_s = s_char + align_s
        align_t = t_char + align_t

        if s_char != '-' and t_char != '-':
            cur_i -= 1
            cur_j -= 1

        elif s_char == '-':
            cur_j -= 1

        elif t_char == '-':
            cur_i -= 1

    print align_s
    print align_t

    print table.get(len(s), len(t)).cost

    return table.get(len(s), len(t)).cost, align_s, align_t

# Example usage
if __name__ == "__main__":
    # Example cost function from instructions.pdf
    def costfunc(s_char, t_char):
        if s_char == t_char: return 0
        if s_char == 'a':
            if t_char == 'b': return 5
            if t_char == 'c': return 3
            if t_char == '-': return 2
        if s_char == 'b':
            if t_char == 'a': return 1
            if t_char == 'c': return 4
            if t_char == '-': return 2
        if s_char == 'c':
            if t_char == 'a': return 5
            if t_char == 'b': return 5
            if t_char == '-': return 1
        if s_char == '-':
            if t_char == 'a': return 3
            if t_char == 'b': return 3
            if t_char == 'c': return 3

    import dynamic_programming
    s = "acb"
    t = "baa"
    D = dynamic_programming.DynamicProgramTable(len(s) + 1, len(t) + 1, cell_ordering(len(s), len(t)), fill_cell)
    D.fill(s = s, t = t, cost=costfunc)
    (cost, align_s, align_t) = diff_from_table(s,t, D)
    print align_s
    print align_t
    print "cost was %d"%cost
