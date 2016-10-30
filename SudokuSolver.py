import argparse
from tabulate import tabulate


def open_file_generate_board():
    parser = argparse.ArgumentParser(description='A sudoku solver using DFS')
    parser.add_argument("file", help='The name of the sudoku file you wish to solve. '
                                     'Proper format is 9 lines of integers 1-9 '
                                     'where 0s represent empty spaces. One line may '
                                     'look like: 123000789')
    args = parser.parse_args()

    try:
        f = open(args.file, 'r')
    except IOError:
        print 'File \'{}\' does not exist.'.format(args.file)
        exit()


    # Make sure the file is formatted properly
    # Only take 9 lines even if it's longer, don't care past that
    for i in xrange(9):
        line = f.readline().strip('\n')
        line = ''.join(line.split())

        # A line should be exactly 9 chars, protect against that
        if len(line) != 9:
            print 'Invalid input line #{}: {}'.format(i, line)
            print 'Found {} characters. Each line should be exactly 9 characters. ' \
                  'Check the format of your text file. Exiting...'.format(len(line))
            exit()

        board.append(list(line))  # 9 * 9 board at this point
        fix.append([False] * 9)   # 9 * 9 board filled with false

    for row, line in enumerate(board):
        for col, number in enumerate(line):
            if int(number) != 0:
                fix[row][col] = True
            else:
                fix[row][col] = False
            line[col] = int(line[col])


def pretty_print_board():
    for line in board:
        for i, number in enumerate(line):
            if number == 0:
                line[i] = ' '

    print tabulate(board, tablefmt='fancy_grid')

    for line in board:
        for i, number in enumerate(line):
            if number == ' ':
                line[i] = 0


def all_diff(lst):
    seen = []
    # iterate over elements in list, if you've seen it before, not everything is diff
    for i in lst:
        if i in seen:
            return False
        # don't append 0, that's empty, we can see as many of those as we want
        if i != 0:
            seen.append(i)
    return True


# Returns true if the value in the row / col is valid
def valid(row, col):
    board_row = board[row]
    board_col = [r[col] for r in board]
    board_section = []

    row_offset = (row/3) * 3
    col_offset = (col/3) * 3

    for x in range(3):
        for y in xrange(3):
            board_section.append(board[x + row_offset][y + col_offset])

    return all_diff(board_row) and all_diff(board_col) and all_diff(board_section)


# Return true if the option is valid to put in the row / col
def valid_option(num, row, col):
    if num == 0:
        return True

    used = set()
    board_row = board[row]
    board_col = [r[col] for r in board]
    board_section = []
    row_offset = (row / 3) * 3
    col_offset = (col / 3) * 3

    for x in range(3):
        for y in xrange(3):
            board_section.append(board[x + row_offset][y + col_offset])

    for i in board_row:
        used.add(i)
    for i in board_col:
        used.add(i)
    for i in board_section:
        used.add(i)

    if num in used:
        return False
    return True


# returns true if the value in the board is fixed (included in the puzzle)
def fixed(row, col):
    return fix[row][col]


def get_empty():
    for row in xrange(9):
        for col in xrange(9):
            if board[row][col] == 0:
                return row, col
    return None, None


def get_state():
    return ''.join(str(item) for innerlist in board for item in innerlist)


def solved():
    row, col = get_empty()
    return row is None


# Backtrack from the given row and column
def backtrack_from(row, col):
    # can't backtrack from the beginning
    if row == 0 and col == 0:
        solve_sudoku()

    if col == 0:        # at the end beginning of the row, need to jump back a row
        # If it's a fixed square, don't move it.
        if fixed(row - 1, 8):
            backtrack_from(row - 1, 8)
        else:   # it's not fixed, set it to 0 and do the thing
            board[row-1][8] = 0
            solve_sudoku()
    else:
        # Look at the cell behind us, if it's fixed we can't move it.
        if fixed(row, col-1):
            backtrack_from(row, col-1)
        else:
            board[row][col-1] = 0       # Set that space to empty and go on solving.
            solve_sudoku()              # Our solve looks for first empty space, so it should find what we just set


def solve_sudoku():
    row, col = get_empty()  # Get first empty spot on board

    if row is None:  # We've solved the puzzle
        return

    # generate valid options
    options = []
    for i in xrange(1, 10):
        if valid_option(i, row, col):
            options.append(i)

    try:        # Seen this state, set our options to what we remember
        options = nodes[get_state()]
    except KeyError:        # haven't seen this state before, set the options in the state
        nodes[get_state()] = options

    if options:   # If we have options
        value = nodes[get_state()][0]    # value to place
        nodes[get_state()].remove(value)  # remove it from the state options
        board[row][col] = value
    else:                           # No options, need to backtrack and try other option.
        backtrack_from(row, col)


board = []
fix = []
nodes = {}  # State to values matching

open_file_generate_board()
print "Here's your board before being solved.\nIf this doesn't look right you might need " \
      "to change your input format."
pretty_print_board()

print '\nSolving...\n'
try:
    while not solved():
        solve_sudoku()
    print "Here's your solved puzzle!"
    pretty_print_board()
except RuntimeError as re:
    print 'ERROR: {}'.format(re)
    print 'The puzzle is likely formatted incorrectly.'




