import copy


class Maze:

	def __init__(self, colorsMaze, maze):
		self.colorsMaze = copy.deepcopy(colorsMaze)
		self.maze = copy.deepcopy(maze)

	def getColor(self, position):
		return self.colorsMaze[position[0]][position[1]]

	def getBoots(self, position):
		return self.maze[position[0]][position[1]]

	def isValid(self, position):
		i, j = position
		return 0 <= i and i < len(self.maze) and 0 <= j and j < len(self.maze[0])

	def setPosition(self, position, color):
		i, j = position
		self.maze[i][j] = color

	def __str__(self):
		res = ""

		for r in self.maze:
			res += str(r) + "\n"

		return res


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

	def __str__(self):
		return str(self.color) + " " + str(self.uses) + "\n"

	def __eq__(self, other):
		return self.color == other.color and self.uses == other.uses


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

	def __str__(self):
		return self.maze.__str__() + self.currentBoots.__str__() + self.backupBoots.__str__() + "\n" + str(self.wizardPosition)


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


	def getMaze(self):
		return self.init_maze

	def validNode(self, node):
		return node.getCurrentBoots().getColor() == self.getMaze().getColor(node.getWizardPosition()) and node.getCurrentBoots().getUses() <= 3

	def genNextNodes(self, node):

		successors = []
		for dir in range(len(self.MOVEROW)):

			maze = node.getMaze()
			currentPosition = node.getWizardPosition()

			nextPosition = (currentPosition[0] + self.MOVEROW[dir], currentPosition[1] + self.MOVECOL[dir])

			if maze.isValid(nextPosition):

				cost = self.colors[maze.getColor(nextPosition)]
				nextMaze = copy.deepcopy(maze)

				# nextMaze.setPosition(nextPosition, '*') # move wizard to the next position
				# nextMaze.setPosition(currentPosition, self.init_maze.getBoots(currentPosition)) # restore the cell with the original value

				# get all boots combinations and try to go to the next position

				currentBoots = node.getCurrentBoots()
				backupBoots = node.getBackupBoots()

				if nextMaze.getBoots(currentPosition) in self.colors.keys(): # if I have a pair of boots on current position

					parcelBoots = Boots(nextMaze.getBoots(currentPosition), 0)
					if backupBoots is None: # no backup boots

						backupBoots = copy.deepcopy(parcelBoots)

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

						if self.validNode(newNode):
							successors.append(newNode)

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots # swap boots

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

						if(self.validNode(newNode)):
							successors.append(newNode)
					else:

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

						if self.validNode(newNode):
							successors.append(newNode)

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots

						if currentBoots.getColor() != parcelBoots.getColor():

							# don't take boots on the parcel
							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

							if self.validNode(newNode):
								successors.append(newNode)

							currentBoots, parcelBoots = parcelBoots, currentBoots # swap out currentBoots

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # classic swap

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # undo swap
							currentBoots, parcelBoots = parcelBoots, currentBoots # undo swap

						elif currentBoots.getColor() == parcelBoots.getColor():
							if currentBoots.getUses() > 0:
								print("Parcel boots: ", parcelBoots)
								currentBoots, parcelBoots = parcelBoots, currentBoots # swap out currentBoots

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # classic swap

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # undo swap
								currentBoots, parcelBoots = parcelBoots, currentBoots # undo swap

						if backupBoots.getColor() != parcelBoots.getColor():

							# don't take boots on the parcel
							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

							if self.validNode(newNode):
								successors.append(newNode)

							backupBoots, parcelBoots = parcelBoots, backupBoots # swap out backupBoots

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # classic swap

							newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

							if self.validNode(newNode):
								successors.append(newNode)

							if currentBoots != backupBoots:
								currentBoots, backupBoots = backupBoots, currentBoots # undo swap
							backupBoots, parcelBoots = parcelBoots, backupBoots # undo swap

						elif backupBoots.getColor() == parcelBoots.getColor():
							if backupBoots.getUses() > 0:
								backupBoots, parcelBoots = parcelBoots, backupBoots # swap out backupBoots

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # classic swap

								newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

								if self.validNode(newNode):
									successors.append(newNode)

								if currentBoots != backupBoots:
									currentBoots, backupBoots = backupBoots, currentBoots # undo swap
								backupBoots, parcelBoots = parcelBoots, backupBoots # undo swap

				else: # if I don't have a pair of boots on current position

					newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

					if self.validNode(newNode):
						successors.append(newNode)

					if backupBoots is not None:

						if currentBoots != backupBoots:
							currentBoots, backupBoots = backupBoots, currentBoots # swap boots

						newNode = Node(nextMaze, Boots(currentBoots.getColor(), currentBoots.getUses() + 1), backupBoots, nextPosition)

						if(self.validNode(newNode)):
							successors.append(newNode)

		# return successors
		return list(set(successors))



graph = AstarGraph("input.txt")