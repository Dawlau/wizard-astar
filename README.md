# wizard-astar




define what a state looks like
read input

state:

current maze
maze colors
current boots color
current boots uses
backup boots color
backup boots uses

generate successors:

validation:
current boots color == color of next parcel
current boots usage < 3


transition:

move to a valid neighbour and have the next possible options (in maze and current boots color is the same with the color of the neighbour):
	I) the wizard can either swap current boots with backup boots or not (before entering the parcel) if they are not the same color and same usage and if backup boots exist
	II) check wether there are some boots the wizard can take on the parcel:
				1) if not, nothing to be done here
				2) if there are some boots these are the possible outcomes:
						- if wizard has no backup boots then just put the parcel boots on backup boots
						- otherwise: if currentBoots.color != parcelBoots.color then get new node by swapping currentBoots with parcelBoots and then maybe jump to I)
									 if currentBoots.color == parcelBoots.color and currentBoots.usage > 0 then get new node by swapping currentBoots with parcelBoots and then maybe jump to I)

									 same for backupBoots


	for every transition, the usage of current boots increases by one
	on the new maze, mark the current position of the wizard (with '*') and restore the last position with the original character

costs:

move to parcel of some color => cost is given by the cost of that color
swap backup boots with current boots => cost is 1


goal:

get the magic stone
get back to the entrance