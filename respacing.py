# DO NOT CHANGE THIS CLASS
class RespaceTableCell:
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.validate()

    # This function allows Python to print a representation of a RespaceTableCell
    def __repr__(self):
        return "(%s,%s)"%(str(self.value), str(self.index))

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.value) == bool), "Values in the respacing table should be booleans."
        assert(self.index == None or type(self.index) == int), "Indices in the respacing table should be None or int"

# Inputs: the dynamic programming table, indices i, j into the dynamic programming table, the string being respaced, and an "is_word" function.
# Returns a RespaceTableCell to put at position (i,j)
def fill_cell(T, i, j, string, is_word):

    #print(str(i) + "," + str(j))

    if is_word(string[i:j+1]):
        #print(string[i:j+1] + " is a word!")
        return RespaceTableCell(True, j) #double check this

    else:
        for split in range(i, j):
            #print(str(i) + "," + str(j) + "," + str(split))

            #print("Split from " + str(i) + " to " + str(split) + " returns " + str(T.get(i, split).value))
            #print("Split from " + str(split + 1) + " to " +  str(j) + " returns " + str(T.get(split + 1, j).value))

            if T.get(i, split).value and T.get(split+1, j).value:
                 #print(string[i:j + 1] + " can be split after index " + str(split)) + " into " + string[i:split+1] + ", " + string[split+1:j+1]
                 return RespaceTableCell(True, split)

    return RespaceTableCell(False, None)
                  
# Inputs: N, the size of the list being respaced
# Outputs: a list of (i,j) tuples indicating the order in which the table should be filled.
def cell_ordering(N):

    order_list = []

    # Evaluate the diagonal first
    for i in range(0, N):
        order_list.append((i,i))

    for j in range(1, N):
        for i in range(0, N-j):
            order_list.append((i,i+j))

    return order_list

# Input: a filled dynamic programming table.
# (See instructions.pdf for more on the dynamic programming skeleton)
# Return the respaced string, or None if there is no respacing.
def respace_from_table(s, table):

    if table.get(0,len(s)-1).value is False:
        return None

    respaced_string = s
    space_list = []
    indexes_that_need_spaces(0, len(s)-1, space_list, table)
    space_list.sort()

    spaces_added = 0

    for i in range(len(space_list)):
        respaced_string = respaced_string[0:(space_list[i]+1+spaces_added)] + " " + respaced_string[(space_list[i]+1+spaces_added):]
        spaces_added += 1

    return respaced_string



def indexes_that_need_spaces(i, j, space_list, table):

    split_index = table.get(i, j).index

    if split_index == j:
        return

    else:
        space_list.append(split_index)
        indexes_that_need_spaces(i, split_index, space_list, table)
        indexes_that_need_spaces(split_index + 1, j, space_list, table)

    return space_list



if __name__ == "__main__":
    # Example usage.
    from dynamic_programming import DynamicProgramTable
    s = "itwasthebestoftimes"
    wordlist = ["of", "it", "the", "best", "times", "was"]
    D = DynamicProgramTable(len(s) + 1, len(s) + 1, cell_ordering(len(s)), fill_cell)
    D.fill(string=s, is_word=lambda w:w in wordlist)
    print respace_from_table(s, D)
