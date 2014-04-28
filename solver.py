from __future__ import print_function
from time import time
from sudoku import *
from copy import deepcopy, copy

def solve(filename):
	sboard = init_board(filename)

	print("Initial Board: ")
	pprint(sboard)
	simplify(sboard)

	global nums
	nums = [i for i in range(1, 1+sboard.BoardSize)]

	start_time = time()
	solved_board, num_checks = backtrack_search(sboard)
	end_time = time() - start_time

	print("Solved Board: ")
	pprint(solved_board)

	print("Number of checks: ", num_checks)
	print("Runtime: ", end_time, " seconds")
	return solved_board

def backtrack_search(sboard, depth = 0, num_checks=0):
	x, y = get_empty_space(sboard)

	# pprint(sboard)

	if (x == -1):
		return sboard, num_checks
	else:
		result_board = False
		for i in get_coordinate_values(x, y, sboard):
			#print(get_coordinate_values(x, y, sboard))

			new_board = sboard.set_value(x, y, i)
			simple_board = deepcopy(new_board)
			#simplify(simple_board)
			
			next_board, new_num_checks = backtrack_search(simple_board, depth+1, num_checks+1)
			num_checks = new_num_checks

			if valid_board_p(next_board):
				result_board = next_board
				if iscomplete(result_board.CurrentGameboard) == True:
					return result_board, num_checks

		print(num_checks, depth, sep=" | ")

		return result_board, num_checks

def get_empty_space(sboard):
	for i in range(sboard.BoardSize):
		for j in range(sboard.BoardSize):
			if (sboard.CurrentGameboard[i][j] == 0):
				return i, j
	return -1, -1

def get_coordinate_values(x, y, sboard):

	row = sboard.CurrentGameboard[x]
	col = [i[y] for i in sboard.CurrentGameboard]
	box = get_box_array(x, y, sboard)

	row_vals = get_valid_values(row, sboard.BoardSize) # gets a tuple...
	col_vals = get_valid_values(col, sboard.BoardSize)
	box_vals = get_valid_values(box, sboard.BoardSize)

	vals = [] # dis be inefficient
	for i in nums:
		if (i in row_vals[1] and i in col_vals[1] and i in box_vals[1]):
			vals.append(i)
	return vals

def get_box_array(x, y, sboard):
	side_length = int(sboard.BoardSize ** (0.5))

	if (x == 0):
		squares_row = 0
	else:
		squares_row = x - (x % side_length)

	if (y == 0):
		squares_col = 0
	else:
		squares_col = y - (y % side_length)

	array = []
	for i in range(side_length):
		for j in range(side_length):
			array.append(sboard.CurrentGameboard[i + squares_row][j + squares_col])

	return array

## Consistency checks ##

def valid_board_p(sboard):
	## row, col and box checks
	if (sboard == False):
		return False
	return (valid_rows_p(sboard) and valid_cols_p(sboard) and valid_boxes_p(sboard))

def valid_array_p(array):
	numbs = copy(nums)
	for i in array:
		if (i in numbs):
			numbs.remove(i)
		elif (i != 0):
			return False

	return True

def valid_rows_p(sboard):
	for i in range(sboard.BoardSize):
		array = []
		for j in range(sboard.BoardSize):
			array.append(sboard.CurrentGameboard[i][j])

		if not valid_array_p(array):
			return False
	return True

def valid_cols_p(sboard):
	for i in range(sboard.BoardSize):
		array = []
		for j in range(sboard.BoardSize):
			array.append(sboard.CurrentGameboard[j][i])

		if not valid_array_p(array):
			return False

	return True

def valid_boxes_p(sboard):
	side_length = int(sboard.BoardSize ** (0.5))

	for squares_row in range(side_length):
		for squares_col in range(side_length):
			array = []
			for i in range(side_length):
				for j in range(side_length):
					array.append(sboard.CurrentGameboard[i + squares_row *  side_length][j + squares_col * side_length])

			if not valid_array_p(array):
				return False
	return True

## Simplifies a board -- fills in all spots that have almost all of their components in it. ##

def simplify(sboard):
	"""Examines for guaranteed locations and fills those in."""
	x, y, val = row_check(sboard)
	if val:
		sboard.edit_value(x, y, val)
		return simplify(sboard)

	x, y, val = col_check(sboard)
	if val:
		sboard.edit_value(x, y, val)
		return simplify(sboard)

	x, y, val = box_check(sboard)
	if val:
		sboard.edit_value(x, y, val)
		return simplify(sboard)

	return sboard

def row_check(sboard):
	for i in range(sboard.BoardSize):
		array = []
		for j in range(sboard.BoardSize):
			array.append(sboard.CurrentGameboard[i][j])

		if count_zeros(array) == 1:
			j_index, val = get_valid_values(array, sboard.BoardSize)
			return i, j_index, val[0]

	return False, False, False

def col_check(sboard):
	for i in range(sboard.BoardSize):
		array = []
		for j in range(sboard.BoardSize):
			array.append(sboard.CurrentGameboard[j][i])

		if count_zeros(array) == 1:
			j_index, val = get_valid_values(array, sboard.BoardSize)
			return j_index, i, val[0]

	return False, False, False

def box_check(sboard):
	side_length = int(sboard.BoardSize ** (0.5))

	for squares_row in range(side_length):
		for squares_col in range(side_length):
			array = []
			for i in range(side_length):
				for j in range(side_length):
					array.append(sboard.CurrentGameboard[i + squares_row *  side_length][j + squares_col * side_length])

			if count_zeros(array) == 1:
				index, val = get_valid_values(array, sboard.BoardSize)
				x, y = box_coordinate_convert(index, squares_row, squares_col, side_length)
				return x, y, val[0]

	return False, False, False

def box_coordinate_convert(index, s_row, s_col, side):
	row = 0
	while index > (side - 1):
		index -= side
		row += 1
	col = index

	return row + s_row * side, col + s_col * side

def get_valid_values(array, size):
	if 0 in array:
		index = array.index(0)
	else:
		index = 5
	numbs = copy(nums)

	for i in array:
		if i in numbs:
			numbs.remove(i)

	return index, numbs

def count_zeros(array):
	counter = 0
	for i in array:
		if i == 0:
			counter += 1
	return counter

def pprint(sboard):
	for i in sboard.CurrentGameboard:
		for j in i:
			if (j == 0):
				print("-", end=" ")
			else:
				print(j, end=" ")
		print("")
	print("")
	return

solve("tests/9x9.sudoku")