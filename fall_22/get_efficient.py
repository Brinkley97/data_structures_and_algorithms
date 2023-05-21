import sys
from resource import *
import time
import psutil

input_file_path = "/Users/brinkley97/Documents/development/classes/csci_570_analysis_of_algorithms/datapoints/in1.txt"
# print(input_file_path)
alpha_list = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]]
delta_val = 30


# Time
def time_wrapper():
    start_time = time.time()
    main()
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return time_taken


# Memory
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def get_final_string(k, v):
    s = k
    for i in v:
        new_str = s[:i + 1] + s + s[i + 1:]
        s = new_str
    return s


def generate_string(my_dict):
    f_strings = []
    for i, (k, v) in enumerate(my_dict.items()):
        f_strings.append(get_final_string(k, v))
    return f_strings


def get_string_alignment(opt, str1, str2, delta):
    """
  return str1_alignment, str2_alignment
  """
    str1_alignment = []
    str2_alignment = []

    m = len(opt)  # number of rows
    n = len(opt[0])  # number of cols

    i, j = m - 1, n - 1  # i corresponds to rows, j corresponds to cols

    # start at here
    while i >= 0 and j >= 0:
        # base case
        letterx = str1[j - 1]
        lettery = str2[i - 1]

        if i == 0 and j == 0:
            # print("end")
            break

        # first row
        elif i == 0:
            # go left
            # print("go left")
            # insert a gap in str2_alignment
            str1_alignment.insert(0, letterx)
            str2_alignment.insert(0, '_')
            j -= 1

        # first col
        elif j == 0:
            # go up
            # print("go up")
            # insert a gap in str1_alignment
            str1_alignment.insert(0, '_')
            str2_alignment.insert(0, lettery)
            i -= 1

        else:  # compare opt[i-1][j-1]+alphalist,opt[i-1][j],+delta,opt[i][j-1]+delta
            if (opt[i - 1][j - 1] + alpha_list[get_alpha(str1[j - 1])][get_alpha(str2[i - 1])]) == opt[i][j]:
                # print("go up left")
                str1_alignment.insert(0, letterx)
                str2_alignment.insert(0, lettery)
                i -= 1
                j -= 1
            elif opt[i - 1][j] + delta_val == opt[i][j]:
                # print("go up")
                str1_alignment.insert(0, "_")
                str2_alignment.insert(0, lettery)
                i -= 1
            else:
                # print("go left")
                str1_alignment.insert(0, letterx)
                str2_alignment.insert(0, "_")
                j -= 1
    s1, s2 = "".join(str1_alignment), "".join(str2_alignment)
    return s1, s2


# {"ACTG": [3, 6, 1], 1: [1, 2, 9]}
def get_alpha(x):
    '''Match letters
  x -- char

  return -- alpha int
  '''

    if x == 'A':
        return 0
    elif x == 'C':
        return 1
    elif x == 'G':
        return 2
    elif x == 'T':
        return 3


def alignment_cost_2(X, Y, alpha_list, delta):
    '''
  alpha -- 2D list
  x -- char
  y -- char
  return -- value
  '''
    X_length = len(X)
    Y_length = len(Y)

    # cols (x) by rows (y) =>
    OPT = [[0 for x in range(X_length + 1)] for y in range(Y_length + 1)]

    #     Base cases/Initialize
    OPT[0][0] = 0

    # To fill the rows we need the columns to change, we are moving from col 0 ... x_len; going column by column; fixed/initialize on row
    for col in range(X_length + 1):
        # print(col)
        OPT[0][col] = col * delta
        # print(OPT, np.shape(OPT))

    # To fill the col we need the row to change, we are moving from row 0 ... y_len; going row by row; fixed/initialize on col
    for row in range(Y_length + 1):
        # print(col)
        OPT[row][0] = row * delta
        # print(OPT)

    # i reps the colums; outter loop reps cols
    for i in range(1, X_length + 1):
        # j reps the rows; inner loop reps rows
        for j in range(1, Y_length + 1):
            x_i = X[i - 1]
            y_j = Y[j - 1]

            alpha = alpha_list[get_alpha(x_i)][get_alpha(y_j)]
            OPT[j][i] = min(
                alpha + OPT[j - 1][i - 1],
                delta + OPT[j - 1][i],
                delta + OPT[j][i - 1]
            )

    # return OPT[X_length][Y_length]
    return OPT[len(Y)][len(X)]
    # return OPT[i][j]


def efficient_v(X,  Y, a_list, delta):  # efficient version of alignment_cost_2
    ''''
    alpha -- 2D list
    x -- char
    y -- char
    return -- array of cost
  '''
    X_length = len(X)
    Y_length = len(Y)

    # array1 = [0 for _ in range(Y_length+1)]
    # array2 = [0 for _ in range(Y_length+1)]
    array = [[0 for _ in range(Y_length + 1)] for _ in range(2)]

    # initialization
    for i in range(1, Y_length + 1):
        array[0][i] = i * delta

    for j in range(1, X_length + 1):
        for i in range(Y_length + 1):
            str1_val = get_alpha(X[j - 1])
            str2_val = get_alpha(Y[i - 1])

            array[1][0] = delta * j

            array[1][i] = min(array[0][i] + delta, array[1][i - 1] + delta,
                              array[0][i - 1] + a_list[str1_val][str2_val])

        array[0] = [x for x in array[1]]
        # array1 = array2[:]

        # array1,array2 = array2,array1
        # print(j)
        # print(array)
        # print(array1)
        # print(array2)
        # from X to entire Y
        # left side
        # mapping of y with x left
        # find opt split point
        # split x in 1/2 and y
        # send left side of both
        # make
    return array[0]


def hirschberg_algorithm(x, y):
    # base case: if either string is empty, return the length of the other string
    if len(x) == 0:
        return len(y)
    if len(y) == 0:
        return len(x)
    # divide the problem into two smaller subproblems
    xmid = len(x) // 2
    score_l = efficient_v(x[:xmid], y, alpha_list, delta_val)
    score_r = efficient_v(x[xmid:][::-1], y[::-1], alpha_list, delta_val)


    index = 0
    minimal = float("inf")
    length = len(score_l)
    for i in range(length):
      score_l[i] += score_r[length-1-i]
      if score_l[i]<minimal:
        minimal = score_l[i]
        index = i

    return score_l, minimal,index

    # find the minimum cost alignment in the left and right subproblems
    # min_score_l = min(score_l)
    # min_score_r = min(score_r)
    # min_index_l = score_l.index(min_score_l)
    # min_index_r = score_r.index(min_score_r)

    # combine the results from the left and right subproblems
    # if min_score_l + min_score_r < len(x):
    #   return min_score_l + min_score_r
    # else:
    #   return len(x)


def main():
  with open(input_file_path) as f:
    l2write = []
    ns = {}
    lines = f.readlines()
    strings = []
    for i in range(len(lines)):
      if lines[i].strip().isdigit() == False:
        l2write.append(0)
        strings.append(lines[i].rstrip())
        ns[strings[-1]] = []
      else:
        l2write[-1] += 1
        ns[list(ns)[-1]].append(int(lines[i].rstrip()))

    X = generate_string(ns)[0]
    Y = generate_string(ns)[0]

  cost, opt = alignment_cost_2(X, Y, alpha_list, delta_val)
  print("Cost: ", cost)
  # print(get_string_alignment(opt, X, Y, delta_val))
  str_alignments_1, str_alignments_2 = get_string_alignment(opt, X, Y, delta_val)
  print(str_alignments_1)
  print()
  print(str_alignments_2)

  m = len(str_alignments_1)
  n = len(str_alignments_2)
  problem_size = m + n
  print("Problem size: ", problem_size)



if __name__ == "__main__":
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
  # print(input_file_name, output_file_name)
    main()

print("Time taken: ",time_wrapper())
print("Memory", process_memory() )
