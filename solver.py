from __future__ import print_function
from sudoku import *

def solve(sboard):

	return

def easy_fill(sboard):
	"""Examines for guaranteed locations and fills those in."""
	x, y, val = row_check(sboard)
	if val:
		sboard.edit_value(x, y, val)
		return easy_fill(sboard)

	x, y, val = col_check(sboard)
	if val:
		sboard.edit_value(x, y, val)
		return easy_fill(sboard)

	x, y, val = box_check(sboard)
	if val:
		sboard.edit_value(x, y, val)
		return easy_fill(sboard)

	return sboard

def row_check(sboard):
	for i in range(sboard.BoardSize):
		array = []
		for j in range(sboard.BoardSize):
			array.append(sboard.CurrentGameboard[i][j])

		if count_zeros(array) == 1:
			j_index, val = get_value(array, sboard.BoardSize)
			return i, j_index, val

	return False, False, False

def col_check(sboard):
	for i in range(sboard.BoardSize):
		array = []
		for j in range(sboard.BoardSize):
			array.append(sboard.CurrentGameboard[j][i])

		if count_zeros(array) == 1:
			j_index, val = get_value(array, sboard.BoardSize)
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
				index, val = get_value(array, sboard.BoardSize)
				x, y = box_coordinate_convert(index, squares_row, squares_col, side_length)
				return x, y, val

	return False, False, False

board = init_board("4x4.sudoku")
board.edit_value(2,0,2)

def get_value(array, size):
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

def box_coordinate_convert(index, s_row, s_col, side):
	row = 0
	while index > (side - 1):
		index -= side
		row += 1
	col = index

	return row + s_row * side, col + s_col * side

def pprint(sboard):
	for i in sboard.CurrentGameboard:
		for j in i:
			if (j == 0):
				print("-", end=" ")
			else:
				print(j, end=" ")
		print("")
	return

