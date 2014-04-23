from __future__ import print_function
from sudoku import *
from copy import deepcopy

def solve(filename):
	sboard = init_board(filename)
	simplify(sboard)
	solved_board = backtrack_search(sboard)
	pprint(solved_board)
	return solved_board

def backtrack_search(sboard, depth=0):
	nums = [i for i in range(1, 1+sboard.BoardSize)]
	x, y = getEmptySpace(sboard)

	if (x == -1):
		return sboard
	else:
		result_board = False
		for i in nums:

			new_board = sboard.set_value(x, y, i)
			simple_board = deepcopy(new_board)
			simplify(simple_board)

			next_board = backtrack_search(simple_board, depth+1)
			if (valid_board_p(simple_board) and valid_board_p(next_board)):
				result_board = next_board

		return result_board

def getEmptySpace(sboard):
	for i in range(sboard.BoardSize):
		for j in range(sboard.BoardSize):
			if (sboard.CurrentGameboard[i][j] == 0):
				return i, j
	return -1, -1

## Consistency checks ##

def valid_board_p(sboard):
	## row, col and box checks
	if (sboard == False):
		return False
	return (valid_rows_p(sboard) and valid_cols_p(sboard) and valid_boxes_p(sboard))


def valid_array_p(array):
	nums = [i for i in range(1, 1+len(array))]

	for i in array:
		if (i in nums):
			nums.remove(i)
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
			j_index, val = get_missing_value(array, sboard.BoardSize)
			return i, j_index, val

	return False, False, False

def col_check(sboard):
	for i in range(sboard.BoardSize):
		array = []
		for j in range(sboard.BoardSize):
			array.append(sboard.CurrentGameboard[j][i])

		if count_zeros(array) == 1:
			j_index, val = get_missing_value(array, sboard.BoardSize)
			return j_index, i, val

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
				index, val = get_missing_value(array, sboard.BoardSize)
				x, y = box_coordinate_convert(index, squares_row, squares_col, side_length)
				return x, y, val

	return False, False, False

def box_coordinate_convert(index, s_row, s_col, side):
	row = 0
	while index > (side - 1):
		index -= side
		row += 1
	col = index

	return row + s_row * side, col + s_col * side

def get_missing_value(array, size):
	nums = [i for i in range(1, 1+size)]
	index = array.index(0)

	for i in array:
		if i in nums:
			nums.remove(i)

	return index, nums[0]

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
	return

