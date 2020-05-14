import minmax
import board
import time
import os
import time
m = minmax.minmax()
b = board.SimpleBoard()
g = board.Game()

def speed_test():
	mapstart = time.perf_counter()
	m.evaluator(b, b.RED)
	mapend = time.perf_counter()
	print("Time Elapsed: "+str(mapend-mapstart))

	mapstarter = time.perf_counter()
	m.evaluator2(b, b.RED)
	mapender = time.perf_counter()
	print("Time Elapsed2: "+str(mapender-mapstarter))
	#m.minimax(b, 4, b.RED, float('-inf'), float('inf'))


def even_fight():
	for i in range(100):
		time.sleep(0.40)
		#os.system("clear")
		mapstart = time.perf_counter()
		g.step()
		mapend = time.perf_counter()
		print("Time Elapsed: "+str(mapend-mapstart))
		if g.board.is_over():
			print("Game Finished")
			break


def random_fight():
	for i in range(100):
		time.sleep(0.40)
		input("")

		if g.step_r():
			print("Game Finished")
			break
		if g.board.is_over():
			print("Game Finished")
			break