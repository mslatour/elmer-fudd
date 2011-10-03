import math

# Function determines iteratively the move of each predator.
#
# The function takes the following input:
# 	start = [(x,y),(x,y),(x,y),(x,y)]
# 	goal = [(x,y),(x,y),(x,y),(x,y)]
# 	(x,y) = start or goal position of predator
# 	start: x&y distance to walk
# 	goal: position to go, seen from prey:
# 	(0,1) = north of prey
# 	(1,0) = east of prey
# 	(0,-1) = south of prey
# 	(-1,0) = west of prey
# 	(x,y) with the highest index is the predator, furthest of the prey
# The output is:
# 	[move, move, move, move]
# 	defining the move for each predator (using the same IDX as start & goal)
def moveCollisionFree(start, goal):
	# movelist[IDX] = [moverank, moveTaken, newWalkDistance]
	movelist = [[0, -1, None], [0, -1, None], [0, -1, None] ,[0, -1, None]]	
	for idx in [3,2,1,0]:
		movelist = determineMoves(start, goal, idx, movelist)

	# Move taken:
	# 0 = none
	# 1 = west
	# 2 = north
	# 3 = east
	# 4 = south
	moves = [movelist[0][1], movelist[1][1], movelist[2][1], movelist[3][1]]
	return moves


# if a collision is found, try to find a non-collision move with a move of a higher rank (see doMove)
# if there is no collision (anymore), find the move of the next predator
def determineMoves(start, goal, idx, movelist):
	movelist = doMove(start, goal, idx, movelist)
	if checkCollision(idx, movelist) == True:
		movelist[idx][0] += 1	#Increase move-rank
		movelist = determineMoves(start, goal, idx, movelist)
	return movelist

# determine collision.
def checkCollision(idx, movelist):
	pos = movelist[idx][2]
	for i in range(idx+1, 4):
		if movelist[i][2] == pos:
			return True
	return False
	
# Rank of Move:
# move==0 -> move along longest axe towards prey
# move==1 -> move along shortest axe towards prey
# move==2 -> do not move
# move==3 -> move along shortest axe in opposite dir of prey
# move==4 -> move along longest axe in opposite dir of prey
def doMove(start, goal, idx, movelist):
	dx = start[idx][0] - goal[idx][0]
	dy = start[idx][1] - goal[idx][1]
	
	if movelist[idx][0] == 0: # move along longest axe
		if abs(dx) > abs(dy):
			if dx > 0:
				movelist[idx][1] = 1
				movelist[idx][2] = calcNewWalk(start[idx], (-1,0))
			else:
				movelist[idx][1] = 3
				movelist[idx][2] = calcNewWalk(start[idx], (1,0))
		else:
			if dy > 0:
				movelist[idx][1] = 4
				movelist[idx][2] = calcNewWalk(start[idx], (0,-1))
			else:
				movelist[idx][1] = 2
				movelist[idx][2] = calcNewWalk(start[idx], (0,1))
	elif movelist[idx][0] == 1: # move along shortest ax
		if abs(dx) < abs(dy):
			if dx > 0:
				movelist[idx][1] = 1
				movelist[idx][2] = calcNewWalk(start[idx], (-1,0))
			else:
				movelist[idx][1] = 3
				movelist[idx][2] = calcNewWalk(start[idx], (1,0))
		else:
			if dy > 0:
				movelist[idx][1] = 4
				movelist[idx][2] = calcNewWalk(start[idx], (0,-1))
			else:
				movelist[idx][1] = 2
				movelist[idx][2] = calcNewWalk(start[idx], (0,1))
	elif movelist[idx][0] == 2: # Stand still
		movelist[idx][1] = 0
		movelist[idx][2] = start(idx)
	elif movelist[idx][0] == 3: # move opposite dir along shortest axe
		if abs(dx) < abs(dy):
			if dx > 0:
				movelist[idx][1] = 3
				movelist[idx][2] = calcNewWalk(start[idx], (1,0))
			else:
				movelist[idx][1] = 1
				movelist[idx][2] = calcNewWalk(start[idx], (-1,0))
		else:
			if dy > 0:
				movelist[idx][1] = 2
				movelist[idx][2] = calcNewWalk(start[idx], (0,1))
			else:
				movelist[idx][1] = 4
				movelist[idx][2] = calcNewWalk(start[idx], (0,-1))
	elif movelist[idx][0] == 4: # move opposite dir along longest axe
		if abs(dx) > abs(dy):
			if dx > 0:
				movelist[idx][1] = 3
				movelist[idx][2] = calcNewWalk(start[idx], (1,0))
			else:
				movelist[idx][1] = 1
				movelist[idx][2] = calcNewWalk(start[idx], (-1,0))
		else:
			if dy > 0:
				movelist[idx][1] = 2
				movelist[idx][2] = calcNewWalk(start[idx], (0,1))
			else:
				movelist[idx][1] = 4
				movelist[idx][2] = calcNewWalk(start[idx], (0,-1))
	return movelist

GRIDSIZE = 15
def calcNewWalk(start, walked):
	x = start[0] + walked[0]
	if x > math.floor(.5*GRIDSIZE):
		x -= GRIDSIZE
	elif x < -1*math.floor(.5*GRIDSIZE):
		x += GRIDSIZE

	y = start[1] + walked[1]
	if y > math.floor(.5*GRIDSIZE):
		y -= GRIDSIZE
	elif y < -1*math.floor(.5*GRIDSIZE):
		y += GRIDSIZE
	return (x,y)



