import copy

class Maze:

	def __init__(self, colorsMaze, maze):
		self.colorsMaze = copy.deepcopy(colorsMaze)
		self.maze = copy.deepcopy(maze)

	def getColor(self, position):
		return self.colorsMaze[position[0]][position[1]]

	def getBoots(self, position):
		i, j = position
		if self.maze[i][j] == "0":
			return None
		return self.maze[i][j]

	def isValid(self, position):
		i, j = position
		return 0 <= i and i < len(self.maze) and 0 <= j and j < len(self.maze[0])


class Boots:

	def __init__(self, color, uses):
		self.color = color
		self.uses = uses

	def getColor(self):
		return self.color

	def getUses(self):
		return self.uses

	def setColor(self, color):
		self.color = color

	def setUsers(self, uses):
		self.uses = uses


class Node:

	def __init__(self, maze = None, currentBoots = None, backupBoots = None, wizardPosition = None):
		self.maze = copy.deepcopy(maze)
		self.currentBoots = copy.deepcopy(currentBoots)
		self.backupBoots = copy.deepcopy(backupBoots)
		self.wizardPosition = wizardPosition

	def getMaze(self):
		return self.maze

	def getCurrentBoots(self):
		return self.currentBoots

	def getBackupBoots(self):
		return self.backupBoots

	def getWizardPosition(self):
		return self.wizardPosition


class AstarGraph:

	MOVEROW = [-1, 0, 1, 0]
	MOVECOL = [0, 1, 0, -1]

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
		colors = {line[0] : line[1] for line in colors if line != []}

		stringColorsMaze = colorsMaze
		colorsMaze = []

		for line in stringColorsMaze.strip().split("\n"):
			colorsMaze.append(line.split())

		stringMaze = maze
		maze = []

		for line in stringMaze.strip().split("\n"):
			maze.append(line.split())

		return colors, colorsMaze, maze

	def __init__(self, Filename):

		colors, colorsMaze, maze = self.parseInput(Filename)

		self.colors = colors
		self.init_maze = Maze(colorsMaze, maze)
		for i in range(len(maze)):
			for j in range(len(maze[0])):
				if maze[i][j] == "*":
					self.startNode = Node(self.init_maze, Boots(colorsMaze[i][j], 1), None, (i, j))

		self.genNextNodes(self.startNode)

	def genNextNodes(self, node):

		for dir in range(len(self.MOVEROW)):

			nextMaze = copy.deepcopy(node.getMaze())
			currentPosition = node.getWizardPosition()

			nextPosition = (currentPosition[0] + self.MOVEROW[dir], currentPosition[1] + self.MOVECOL[dir])

			if nextMaze.isValid(nextPosition):

				cost = self.colors[nextMaze.getColor(nextPosition)]
				print(cost)

		# for dir in range(len())

graph = AstarGraph("input.txt")