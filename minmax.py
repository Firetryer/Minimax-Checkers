from copy import deepcopy
import _pickle as cPickle

BLACK = 0
RED = 1
NONE = -1

MAX = 1
MIN = 0
import time
class minmax:

	def __init__(self):
		self.score_vars = {}


	def minimax(self, state, depth, player, alpha, beta):
		current_depth = depth
		if current_depth <= 0 or state.is_over():
			return (self.evaluator(state, player), None)

		if player == RED:
			best_value = float('-inf')
		else:
			best_value = float('inf')

		all_moves = state.get_all_moves(player)
		best_move = None

		for move in all_moves:
			#new_state = deepcopy(state)
			new_state = cPickle.loads(cPickle.dumps(state, -1))
			new_state.apply_move(move)
			child_eval, child_move = self.minimax(new_state, current_depth-1, RED if player == BLACK else BLACK, alpha, beta)
			if player == RED and best_value < child_eval:
				best_value = child_eval
				best_move = move
				alpha = max(alpha, best_value)
				if beta <= alpha:
					break

			if player == BLACK and best_value > child_eval:
				best_value = child_eval
				best_move = move
				beta = min(beta, best_value)
				if beta <= alpha:
					break
					
		return best_value, best_move


	def evaluator(self, board, player):
		if len(board.red_pieces) == 0:
			return float('-inf')

		elif len(board.black_pieces) == 0:
			return float('inf')

		pieces = board.red_pieces

		if player == RED:
			score_modifier = 1

		elif player == BLACK:
			score_modifier = -1

		distance_score = 0.1
		king_score = 0
		edge_score = 0
		score = 0

		
		for focus_piece in pieces:
			if focus_piece[2] == True:
				king_score += 10
			if focus_piece[0] == 0 or focus_piece[0] == board.width - 1:
				edge_score += 2

			if focus_piece[1] == 0 or focus_piece[1] == board.height - 1:
				edge_score += 0.5


			distance_score = 0
			for other_piece in pieces:
				if focus_piece == other_piece:
					continue
				distance_x = abs(focus_piece[0] - other_piece[0])
				distance_y = abs(focus_piece[1] - other_piece[1])
				distance_score += (distance_x) + (distance_y)
		
		#  distance_score /= len(pieces)

		size_score = 0
		if len(pieces) > len(board.black_pieces):
			size_score = 15 + (len(pieces) - len(board.black_pieces)) * 1.2
		else:
			size_score = -15
		
		score = king_score + size_score + edge_score + (distance_score * 0.5)
		self.score_vars["king_score"] = king_score
		self.score_vars["size_score"] = size_score
		self.score_vars["edge_score"] = edge_score
		self.score_vars["distance_score"] = distance_score * 0.5
		return score * score_modifier

