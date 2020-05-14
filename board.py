import minmax
#=== Globals

# Piece Colors
BLACK = 0
RED = 1


class SimpleBoard():
	BLACK = 0
	RED = 1
	def __init__(self):
		self.width = 8
		self.height = 8

		self.black_pieces = []
		self.red_pieces = []
 
		for i in range(self.width):
			self.black_pieces.append([i, (i+1)%2, False])
			self.red_pieces.append([i, self.height - (i%2) - 1, False])
			

		self.max_depth = 10

	def is_over(self):
		if len(self.black_pieces) == 0 or len(self.red_pieces) == 0:
			return True
		return False

	def apply_move(self, move):
		piece = move[0]
		move = move[1]

		#==== Start of non-logic code (Reused, fix this somehow)
		if piece in self.black_pieces:
			current_side = BLACK
			current_list = self.black_pieces
		if piece in self.red_pieces:
			current_side = RED
			current_list = self.red_pieces

		target = [piece[0] + move[0], piece[1] + move[1]]

		if [i for i in target] + [False] in self.black_pieces or [i for i in target] + [False] in self.red_pieces:
			target = [i for i in target] + [False]

		if [i for i in target] + [True] in self.black_pieces or [i for i in target] + [True] in self.red_pieces:
			target = [i for i in target] + [True]
		#==== End of non-logic code

		# Check if its a jump move
		if current_side == BLACK and target in self.red_pieces or current_side == RED and target in self.black_pieces:
			# === Its a jump move
			jump_target = [target[0] + move[0], target[1] + move[1], target[2]]
			current_list[current_list.index(piece)] = jump_target
			if current_side == BLACK:
				self.red_pieces.remove(target)
			if current_side == RED:
				self.black_pieces.remove(target)
			return True
		# Just A Regular Move
		current_list[current_list.index(piece)] = target + [piece[2]]
		
		for all_piece in self.red_pieces:
			if all_piece[1] == 0:
				all_piece[2] = True

		for all_piece in self.black_pieces:
			if all_piece[1] == self.height-1:
				all_piece[2] = True

	def get_all_moves(self, side):
		pieces = None
		if side == BLACK:
			pieces = self.black_pieces
		else:
			pieces = self.red_pieces

		possible_moves = []
		for piece in pieces:
			for move in self.possible_moves(piece):
				if self.is_valid_move(piece, move, True):
					possible_moves = [(piece, move)]
					return possible_moves

				elif self.is_valid_move(piece, move):
					possible_moves.append((piece, move))

		return possible_moves

	def is_valid_move(self, piece, move, check_jump = False):
		if piece in self.black_pieces:
			current_side = BLACK
		
		if piece in self.red_pieces:
			current_side = RED

		target = [piece[0] + move[0], piece[1] + move[1]]
		if [i for i in target] + [False] in self.black_pieces or [i for i in target] + [False] in self.red_pieces:
			target = [i for i in target] + [False]

		if [i for i in target] + [True] in self.black_pieces or [i for i in target] + [True] in self.red_pieces:
			target = [i for i in target] + [True]

		# === Out of bounds
		if target[1] < 0 or target[1] >= self.height or target[0] < 0 or target[0] >= self.width:
			return False

		elif target in self.black_pieces and current_side == BLACK or target in self.red_pieces and current_side == RED:
			return False

		elif current_side == BLACK and target in self.red_pieces or current_side == RED and target in self.black_pieces:
			# === Attempt to jump it
			# === Does it go out of bounds if we jump?
			jump_target = [target[0] + move[0], target[1] + move[1]]
			if jump_target[1] < 0 or jump_target[1] >= self.height or jump_target[0] < 0 or jump_target[0] >= self.width:
				return False

			if jump_target+[False] in self.red_pieces or jump_target+[False] in self.black_pieces or jump_target+[True] in self.red_pieces or jump_target+[True] in self.black_pieces:
				return False

			if check_jump == True:
				return True

		if check_jump == True:
			return False
		return True


	def possible_moves(self, piece):
		black_moves = [(-1, 1), (1, 1)]
		red_moves = [(-1, -1), (1, -1)]

		if piece[2] == True:
			return black_moves + red_moves
		elif piece in self.black_pieces:
			return black_moves
		elif piece in self.red_pieces:
			return red_moves


	def board_output(self):
		matrix = [['.'] * self.width for i in range(self.height)]
		for piece in self.red_pieces:
			if piece[2] == False:
				matrix[piece[0]][piece[1]] = 'r'
			else:
				matrix[piece[0]][piece[1]] = 'R'

		for piece in self.black_pieces:
			if piece[2] == False:
				matrix[piece[0]][piece[1]] = 'b'
			else:
				matrix[piece[0]][piece[1]] = 'B'

		return matrix


import random



class Game():
	def __init__(self):
		self.board = SimpleBoard()
		self.minmax = minmax.minmax()
		self.its_reds_turn = True
		self.max_depth = 6

	def pretty_print(self):
		for i in self.board.board_output():
			cated = ""
			for ii in i:
				cated += str(ii)
			print(cated)

	def random_action(self, player):
		action = random.choice(self.board.get_all_moves(player))
		self.board.apply_move(action)

	def step_r(self):

		
		output = self.minmax.minimax(self.board, self.max_depth, RED, float('-inf'), float('inf'))
		if output[1] != None:
			self.board.apply_move(output[1])
		if self.board.is_over():
			return True
		print("It is RED'S turn.")
		self.pretty_print()
		print("Score for this node: " + str(output[0]))
		print("    Score Breakdown: " + str(self.minmax.score_vars))
		print("          Max Depth: " + str(self.max_depth))
		print("It is BLACK'S turn.")
		self.random_action(BLACK)

		self.pretty_print()

	def step(self):
		current_player = RED if self.its_reds_turn else BLACK

		p = "RED" if self.its_reds_turn else "BLACK"
		

		output = self.minmax.minimax(self.board, self.max_depth, current_player, float('-inf'), float('inf'))
		self.its_reds_turn = not self.its_reds_turn
		if output[1] != None:
			self.board.apply_move(output[1])
		print("It is " + p + "'S turn.")
		self.pretty_print()
		print("Score for this node: " + str(output[0]))
		print("    Score Breakdown: " + str(self.minmax.score_vars))
		print("          Max Depth: " + str(self.max_depth))

