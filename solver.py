from __future__ import print_function
from time import time
from sudoku import *
from copy import deepcopy, copy

# KEVIN CHEN
# KJC004
# EECS 348
# HW1, SUDOKU SOLVER

# One method was added to the provided starter code class.

def solve(filename, method="back"):
	sboard = init_board(filename)

	print("Initial Board: ")
	pprint(sboard)
	simplify(sboard)

	global nums
	nums = [i for i in range(1, 1+sboard.BoardSize)]

	start_time = time()
	if method == "back":
		solved_board, num_checks = backtrack_search(sboard)
	elif method == "forward":
		solved_board, num_checks = forward_tracking(sboard)
	else:
		print("Method ", method, " not implemented.")
		return
	end_time = time() - start_time

	print("Solved Board: ")
	pprint(solved_board)

	print("Number of checks: ", num_checks)
	print("Runtime: ", end_time, " seconds")
	return solved_board

#### GENERAL RECURSION ####

def forward_tracking(sboard, depth = 0, num_checks = 0):
	allowed_values = get_all_allowable_values(sboard)	

	if not allowed_values or any(i[0] == [] for i in allowed_values):
		return sboard, num_checks
	else:
		result_board = False
		x = allowed_values[0][1]
		y = allowed_values[0][2]
		# x, y = get_mrv(sboard)	# for implementing MRV
		for i in allowed_values[0][0]:
		# for i in get_coordinate_values(x, y, sboard):	# once again, for MRV
			new_board = sboard.set_value(x, y, i)
			simple_board = simplify(deepcopy(new_board))

			if not valid_board_p(simple_board):
				return False, num_checks

			next_board, new_num_checks = backtrack_search(simple_board, depth+1, num_checks+1)
			num_checks = new_num_checks

			if valid_board_p(next_board):
				result_board = next_board
				if iscomplete(result_board.CurrentGameboard) == True:
					return result_board, num_checks

		print(num_checks, depth, sep=" | ")

		return result_board, num_checks

# Currently enabled mode: MRV + reverse MCV
def backtrack_search(sboard, depth = 0, num_checks = 0):
	#x, y = get_empty_space(sboard) # pure backtracking
	x, y = get_mrv(sboard)

	# pprint(sboard)

	if (x == -1):
		return sboard, num_checks
	else:
		result_board = False
		for i in get_coordinate_values(x, y, sboard): # pure backtracking / mcv + mrv
		#for i in lcv_sort(get_coordinate_values(x, y, sboard), x, y, sboard): 	#lcv
			#print(get_coordinate_values(x, y, sboard))

			new_board = sboard.set_value(x, y, i)
			simple_board = deepcopy(new_board)
			simplify(simple_board)

			if not valid_board_p(simple_board):
				return False, num_checks
			
			next_board, new_num_checks = backtrack_search(simple_board, depth+1, num_checks+1)
			num_checks = new_num_checks

			if valid_board_p(next_board):
				result_board = next_board
				if iscomplete(result_board.CurrentGameboard) == True:
					return result_board, num_checks

		print(num_checks, depth, sep=" | ")

		return result_board, num_checks

def get_all_allowable_values(sboard):
	zeros = []
	for i in range(sboard.BoardSize):
		for j in range(sboard.BoardSize):
			if (sboard.CurrentGameboard[i][j] == 0):
				zeros.append([i, j])
	if not zeros:
		return False

	return [[get_coordinate_values(i[0], i[1], sboard), i[0], i[1]] for i in zeros]

#### HEURISTIC IMPLEMENTATIONS ####

# lcv functions

def lcv_sort(vals, x, y, sboard):
	lcv_scores = [[get_constraintness(vals[i], x, y, sboard), vals[i]] for i in range(len(vals))]
	lcv_scores.sort(key=lambda k: k[0])

	return [i[1] for i in lcv_scores]

def get_constraintness(val, x, y, sboard):
	score = 0
	row = sboard.CurrentGameboard[x]
	col = [i[y] for i in sboard.CurrentGameboard]
	box = get_box_array(x, y, sboard)
	
	side_length = int(sboard.BoardSize ** (0.5))
	squares_row = x // side_length
	squares_col = y // side_length

	for i in range(len(row)):
		if row[i] == 0 and val in get_coordinate_values(i, y, sboard):
			score += 1

	for i in range(len(row)):
		if col[i] == 0 and val in get_coordinate_values(x, i, sboard):
			score += 1

	for i in range(len(box)):
		if box[i] == 0:
			x_val, y_val = box_coordinate_convert(i, squares_row, squares_col, side_length)
			if (val in get_coordinate_values(x_val, y_val, sboard)):
				score += 1
	return score

# MRV + MCV tiebreaker
def get_mrv(sboard):
	rem_values = get_all_allowable_values(sboard)

	if not rem_values:
		return -1, -1

	for i in rem_values:
		i.append(get_constrainingness(i[1], i[2], sboard))

	#rem_values.sort(key=lambda k: k[3], reverse=True) # proper MCV
	rem_values.sort(key=lambda k: k[3]) # stable sort; reverse MCV
	rem_values.sort(key=lambda k: len(k[0]))
	return rem_values[0][1], rem_values[0][2]

def get_constrainingness(x, y, sboard):
	row = sboard.CurrentGameboard[x]
	col = [i[y] for i in sboard.CurrentGameboard]
	box = get_box_array(x, y, sboard)

	return count_zeros(row) + count_zeros(col) + count_zeros(box)

# general backtracking
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

	row_vals = get_valid_values(row, sboard.BoardSize) # gets a tuple
	col_vals = get_valid_values(col, sboard.BoardSize)
	box_vals = get_valid_values(box, sboard.BoardSize)

	vals = []
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

#### BOARD UTILITY FUNCTION ####

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
