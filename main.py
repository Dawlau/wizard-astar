import copy

'''
Models a maze.
Contains cell colors and maze structure.
'''
class Maze:

	def __init__(self, colorsMaze, maze):
		self.colorsMaze = copy.deepcopy(colorsMaze)
		self.maze = copy.deepcopy(maze)

	# getters
	def getColor(self, position):
		return self.colorsMaze[position[0]][position[1]]

	def getBoots(self, position):
		return self.maze[position[0]][position[1]]

	def getMaze(self):
		return self.maze

	# check if position is in the maze
	def isValid(self, position):
		i, j = position
		return 0 <= i and i < len(self.maze) and 0 <= j and j < len(self.maze[0])

	def setPosition(self, position, color):
		i, j = position
		self.maze[i][j] = color

	# for debugging
	def __str__(self):
		res = ""

		for r in self.maze:
			res += str(r) + "\n"

		return res

	def __eq__(self, other):

		for i in range(len(self.maze)):
			for j in range(len(self.maze[0])):
				if self.maze[i][j] != other.maze[i][j]:
					return False
		return True

'''
Models the wizard's boots.
Contains the color and uses.
'''
class Boots:

	def __init__(self, color, uses):
		self.color = color
		self.uses = uses

	# getters and setters
	def getColor(self):
		return self.color

	def getUses(self):
		return self.uses

	def setColor(self, color):
		self.color = color

	def setUsers(self, uses):
		self.uses = uses

	def __str__(self):
		return str(self.color) + " " + str(self.uses) + "\n"

	# == operator
	def __eq__(self, other):
		return self.color == other.color and self.uses == other.uses

'''
Contains all the data needed for the algorithms nodes.

'''
class Node:

	def __init__(self, maze = None, currentBoots = None, backupBoots = None, wizardPosition = None, dad = None):
		self.maze = copy.deepcopy(maze)
		self.currentBoots = copy.deepcopy(currentBoots)
		self.backupBoots = copy.deepcopy(backupBoots)
		self.wizardPosition = wizardPosition
		self.dad = copy.deepcopy(dad)
		self.g = dad.getG() if dad is not None else 0
		self.h = 0
		self.goal = "stone"

	# getters and setters
	def getMaze(self):
		return self.maze

	def getCurrentBoots(self):
		return self.currentBoots

	def getBackupBoots(self):
		return self.backupBoots

	def getWizardPosition(self):
		return self.wizardPosition

	def __str__(self):
		return self.maze.__str__() + self.currentBoots.__str__() + self.backupBoots.__str__() + "\n" + str(self.wizardPosition)

	def getDad(self):
		return self.dad

	def getG(self):
		return self.g

	def setG(self, g):
		self.g = g

	def getH(self):
		return self.h

	def setH(self, h):
		self.h = round(h, 6)

	def getGoal(self):
		return self.goal

	def setGoal(self, goal):
		self.goal = goal

	def __lt__(self, other):
		return self.g < other.g

	def __eq__(self, other):
		if self.backupBoots is None and other.backupBoots is None:
			cond = True
		else:
			if self.backupBoots is None or other.backupBoots is None:
				cond = False
			else:
				cond = self.backupBoots == other.backupBoots
		return self.maze == other.maze and self.currentBoots == other.currentBoots and cond and self.wizardPosition == other.wizardPosition

'''
Models the graph for A* algorithm
'''

class Graph:

	MOVEROW = [-1, 0, 1, 0]
	MOVECOL = [0, 1, 0, -1]

	# get input from file
	def parseInputFile(self, Filename):
		with open(Filename, "r") as r:
			_input = r.read().strip()
			_input = [line for line in _input.split("-") if line != ""]

			colors = _input[0]
			_input = _input[1].split("\n\n")

			colorsMaze = _input[0]
			maze = _input[1]

			return colors, colorsMaze, maze

	def parseInput(self, Filename):
		colors, colorsMaze, maze = self.parseInputFile(Filename)

		colors = [line.strip().split() for line in colors.split("\n")]
		colors = {line[0] : int(line[1]) for line in colors if line != []}

		stringColorsMaze = colorsMaze
		colorsMaze = []

		for line in stringColorsMaze.strip().split("\n"):
			colorsMaze.append(line.split())

		stringMaze = maze
		maze = []

		for line in stringMaze.strip().split("\n"):
			maze.append(line.split())

		return colors, colorsMaze, maze

	# initialize the graph
	def __init__(self, Filename, heuristicType):

		self.heuristicType = heuristicType

		colors, colorsMaze, maze = self.parseInput(Filename)

		self.colors = colors
		self.init_maze = Maze(colorsMaze, maze)
		for i in range(len(maze)):
			for j in range(len(maze[0])):
				if maze[i][j] == "*":
					self.startNode = Node(self.init_maze, Boots(colorsMaze[i][j], 1), None, (i, j))


	def getColorCost(self, position):
		return self.colors[self.init_maze.getColor(position)]

	def getMaze(self):
		return self.init_maze

	def validNode(self, node):
		return node.getMaze().isValid(node.getWizardPosition()) and node.getCurrentBoots().getColor() == self.getMaze().getColor(node.getWizardPosition()) and node.getCurrentBoots().getUses() <= 3

	'''
	Checks if the given node is a goal node
	'''
	def isGoal(self, node, goal):
		if goal == "exit":
			return node.getMaze().getBoots(node.getWizardPosition()) == "*"
		elif goal == "stone":
			return node.getMaze().getBoots(node.getWizardPosition()) == "@"
		else:
			print("error")

	'''
	Calculate 4 types of heuristics
	'''
	def calcH(self, node, goal):
		if self.heuristicType == "banala":
			if self.isGoal(node, goal):
				return 0
			else:
				return 1
		elif self.heuristicType == "admisibil1": # manhattan distance
			wi, wj = node.getWizardPosition()


			maze = node.getMaze().getMaze()
			for i in range(len(maze)):
				for j in range(len(maze[0])):
					if self.isGoal(Node(node.getMaze(), None, None, (i, j)), goal):
						return abs(i - wi) + abs(j - wj)

		elif self.heuristicType == "admisibil2": # euclidean distance
			wi, wj = node.getWizardPosition()

			import math

			maze = node.getMaze().getMaze()
			for i in range(len(maze)):
				for j in range(len(maze[0])):
					if self.isGoal(Node(node.getMaze(), None, None, (i, j)), goal):
						return math.sqrt((i - wi) * (i - wi) + (j - wj) * (j - wj))
		elif self.heuristicType == "neadmisibil":
			wi, wj = node.getWizardPosition()

			import math

			maze = node.getMaze().getMaze()
			for i in range(len(maze)):
				for j in range(len(maze[0])):
					if self.isGoal(Node(node.getMaze(), None, None, (i, j)), goal):
						return 10 * (abs(i - wi) + abs(j - wj))
		else:
			print("error")

	'''
	Run astar and sort every iteration
	'''
	def runAstar(self, timeout):

		import time

		self.startNode.setH(self.calcH(self.startNode, "stone"))
		OPEN = [self.startNode]
		CLOSED = []
		maxNodesCount = 1

		foundSol = False
		start = time.time()
		while len(OPEN):

			if time.time() - start > timeout:
				return "TIMEOUT"

			maxNodesCount = max(maxNodesCount, len(OPEN) + len(CLOSED))
			node = OPEN.pop(0)
			CLOSED.append(node)

			OPEN.sort(key = lambda x : x.getG(), reverse=True)
			OPEN.sort(key = lambda x : x.getH())

			if self.isGoal(node, node.getGoal()):

				if node.getGoal() == "exit":
					foundSol = True
					stack = []
					ans = ""
					cost = node.getG()
					pathLength = 0

					while node is not None:
						stack.append(node)
						node = node.getDad()
						pathLength += 1


					stack.reverse()
					for n in stack:
						ans += str(n)

					ans += "Cost: " + str(cost) + "\n"
					ans += "Path length: " + str(pathLength) + "\n"
					ans += "Max number of nodes in memory: " + str(maxNodesCount) + "\n"
					return ans
				else:
					node.setGoal("exit")
					OPEN.append(node)

			for nextNode in self.genNextNodes(node, node.getGoal()): # for every successor
				nextNode.setGoal(node.getGoal())
				if nextNode in OPEN:
					i = OPEN.index(nextNode)
					if nextNode.getH() < OPEN[i].getH():
						OPEN[i] = copy.deepcopy(nextNode)
					elif nextNode.getH() == OPEN[i].getH():
						if nextNode.getG() > OPEN[i].getG():
							OPEN[i] = copy.deepcopy(nextNode)
				else:
					if nextNode in CLOSED:
						i = CLOSED.index(nextNode)
						if nextNode.getH() < CLOSED[i].getH() or (nextNode.getH() == CLOSED[i].getH() and nextNode.getG() > CLOSED[i].getG()): # found better path
							CLOSED.pop(i)
					OPEN.append(nextNode)

		if not foundSol:
			return "No solution"


	'''
	Run UCS on specified timeout
	'''
	def runUCS(self, timeout):

		import heapq as hq
		import time

		heap = [self.startNode]
		maxNodesCount = 1

		foundSol = False
		start = time.time()
		while len(heap):

			if time.time() - start > timeout:
				return "TIMEOUT"

			heap.sort(key = lambda x : x.getG() if x.getGoal() == "exit" else 100 * x.getG())
			maxNodesCount = max(maxNodesCount, len(heap))
			node = heap[0]
			heap.pop(0)

			if self.isGoal(node, node.getGoal()):

				if node.getGoal() == "exit": # print path and required parameters
					foundSol = True
					stack = []
					cost = node.getG()
					ans = ""
					pathLength = 0
					while node is not None:
						stack.append(node)
						node = node.getDad()
						pathLength += 1

					stack.reverse()
					for n in stack:
						ans += str(n)
					ans += "Cost: " + str(cost) + "\n"
					ans += "Path length: " + str(pathLength) + "\n"
					ans += "Max number of nodes in memory: " + str(maxNodesCount) + "\n"
					return ans
				else:
					node.setGoal("exit")
					heap.append(node)


			for nextNode in self.genNextNodes(node, node.getGoal()):
				heap.append(nextNode)
				nextNode.setGoal(node.getGoal())

		if not foundSol:
			return "No solution"

	# '''
	# Builds paths for IDA*
	# '''
	# def buildPaths(self, node, limit):

	# 	if node.getH() > limit:
	# 		return node.getH()

	# 	if self.isGoal(node, node.getGoal()) and node.getH() == limit:
	# 		n = copy.deepcopy(node)
	# 		stack = []

	# 		while n is not None:
	# 			stack.append(n)
	# 			n = n.getDad()

	# 		stack.reverse()

	# 		for n in stack:
	# 			print(n)
	# 		return "done"

	# 	ans = float('inf')
	# 	for nextNode in self.genNextNodes(node, node.getGoal()):
	# 		dfAns = self.buildPaths(nextNode, limit)
	# 		if dfAns == "done":
	# 			return "done"
	# 		if dfAns < ans:
	# 			ans = dfAns
	# 	return ans

	# def runIDAstar(self, timeout):

	# 	limit = self.startNode.getH()

	# 	while True:

	# 		ans = self.buildPaths(self.startNode, limit)
	# 		if ans == "done":
	# 			break
	# 		if ans == float('inf'):
	# 			print("No solution")
	# 			break
	# 		limit = ans


	'''
	Generates the graph nodes relative to the goal of the algorithm
	'''
	def genNextNodes(self, node, goal):

		successors = []
		for dir in range(len(self.MOVEROW)):

			maze = node.getMaze()
			currentPosition = node.getWizardPosition()

			nextPosition = (currentPosition[0] + self.MOVEROW[dir], currentPosition[1] + self.MOVECOL[dir])

			if maze.isValid(nextPosition):

				cost = self.colors[maze.getColor(nextPosition)]
				nextMaze = copy.deepcopy(maze)

				# get all boots combinations and try to go to the next position

				currentBoots = node.getCurrentBoots()
				backupBoots = node.getBackupBoots()

				if nextMaze.getBoots(currentPosition) in self.colors.keys(): # if I have a pair of boots on current position

					parcelBoots = Boots(nextMaze.getBoots(currentPosition), 0)
					if backupBoots is None: # no backup boots

						backupBoots = copy.deepcopy(parcelBoots)

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

						if self.validNode(newNode):
							successors.append(newNode)

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots # swap boots

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

						if(self.validNode(newNode)):
							successors.append(newNode)
					else:

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

						if self.validNode(newNode):
							successors.append(newNode)

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots

						if currentBoots.getColor() != parcelBoots.getColor():

							# don't take boots on the parcel
							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

							if self.validNode(newNode):
								successors.append(newNode)

							currentBoots, parcelBoots = parcelBoots, currentBoots # swap out currentBoots

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # classic swap

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # undo swap
							currentBoots, parcelBoots = parcelBoots, currentBoots # undo swap

						elif currentBoots.getColor() == parcelBoots.getColor():
							if currentBoots.getUses() > 0:
								# print("Parcel boots: ", parcelBoots)
								currentBoots, parcelBoots = parcelBoots, currentBoots # swap out currentBoots

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # classic swap

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # undo swap
								currentBoots, parcelBoots = parcelBoots, currentBoots # undo swap

						if backupBoots.getColor() != parcelBoots.getColor():

							# don't take boots on the parcel
							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

							if self.validNode(newNode):
								successors.append(newNode)

							backupBoots, parcelBoots = parcelBoots, backupBoots # swap out backupBoots

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # classic swap

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # undo swap
							backupBoots, parcelBoots = parcelBoots, backupBoots # undo swap

						elif backupBoots.getColor() == parcelBoots.getColor():
							if backupBoots.getUses() > 0:
								backupBoots, parcelBoots = parcelBoots, backupBoots # swap out backupBoots

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # classic swap

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # undo swap
								backupBoots, parcelBoots = parcelBoots, backupBoots # undo swap

				else: # if I don't have a pair of boots on current position

					newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

					if self.validNode(newNode):
						successors.append(newNode)

					if backupBoots is not None:

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots # swap boots

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition, node)

						if(self.validNode(newNode)):
							successors.append(newNode)

		# fix g and h

		# successors = list(set(successors))

		for successor in successors:
			newBoots = successor.getCurrentBoots()
			add = self.getColorCost(successor.getWizardPosition())

			if Boots(newBoots.getColor(), newBoots.getUses() - 1) != node.getCurrentBoots():
				add += 1

			successor.setG(successor.getG() + add)
			successor.setH(successor.getH() + self.calcH(successor, goal))


		# return successors
		return successors


class App:

	def __init__(self):

		import sys

		self.inputFolder = sys.argv[1]
		self.outputFolder = sys.argv[2]
		self.solCount = int(sys.argv[3])
		self.timeout = float(sys.argv[4])

	def run(self):

		import os

		files = [f for f in os.listdir(self.inputFolder) if os.path.isfile(os.path.join(self.inputFolder, f))]

		for file in files:
			inputFile = os.path.join(self.inputFolder, file)
			graphBanal = Graph(inputFile, "banala")
			graphAdmisibil1 = Graph(inputFile, "admisibil1")
			graphAdmisibil2 = Graph(inputFile, "admisibil2")
			graphNeadmisibil = Graph(inputFile, "neadmisibil")

			outputFile = os.path.join("output", "output_banala_" + file)
			with open(outputFile, "w") as w:
				w.write(graphBanal.runAstar(self.timeout))

			outputFile = os.path.join("output", "output_admisibil1_" + file)
			with open(outputFile, "w") as w:
				w.write(graphAdmisibil1.runAstar(self.timeout))

			outputFile = os.path.join("output", "output_admisibil2_" + file)
			with open(outputFile, "w") as w:
				w.write(graphAdmisibil2.runAstar(self.timeout))

			outputFile = os.path.join("output", "output_neadmisibil_" + file)
			with open(outputFile, "w") as w:
				w.write(graphNeadmisibil.runAstar(self.timeout))

			outputFile = os.path.join("output", "output_ucs_" + file)
			with open(outputFile, "w") as w:
				w.write(graphBanal.runUCS(self.timeout))

			outputFile = os.path.join("output", "output_ucs_" + file)
			with open(outputFile, "w") as w:
				w.write(graphAdmisibil1.runUCS(self.timeout))

			outputFile = os.path.join("output", "output_ucs_" + file)
			with open(outputFile, "w") as w:
				w.write(graphAdmisibil2.runUCS(self.timeout))

			outputFile = os.path.join("output", "output_ucs_" + file)
			with open(outputFile, "w") as w:
				w.write(graphNeadmisibil.runUCS(self.timeout))


app = App()
app.run()