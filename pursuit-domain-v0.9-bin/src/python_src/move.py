move(self, prey, pred)
	# determine collision-free move.
	# returns 'msg' which is a string describing the move 

	# change coordinates into range (-7, 7)
	# (is easier to work with)	
	myself = (prey[0] - 7, prey[1] - 7)
	mypred = (pred[0] - 7, pred[1] - 7)

	# create preferred-move list
	# the lower the index, the more preferred the move
	# moves = [(dPred_Dist1, move1), (dPred_Dist2, move2), (dPred_Dist3, move3) ...]
	# 	--> dPred_Dist = absolute total distance of predator to moving predator, after move
	#	--> move = move taken (msg!)

	moves = []	
	if abs(myself[0]) > abs(myself[1]):
		# x = larger!

		if myself[0] > 0:
			moves.append((abs(mypred[0]-1)+abs(mypred[1]), "move east"))		#right
			if myself[1] > 0:		
				moves.append((abs(mypred[0])+abs(mypred[1]-1), "move north"))	#up
				moves.append((abs(mypred[0]+1)+abs(mypred[1]), "move west"))	#left
				moves.append((abs(mypred[0])+abs(mypred[1]+1), "move south"))	#down
			else:
				moves.append((abs(mypred[0])+abs(mypred[1]+1), "move south"))	#down
				moves.append((abs(mypred[0]+1)+abs(mypred[1]), "move west"))	#left
				moves.append((abs(mypred[0])+abs(mypred[1]-1), "move north"))	#up
		else:
			moves.append((abs(mypred[0]+1)+abs(mypred[1]), "move west"))		#left
			if myself[1] > 0:		
				moves.append((abs(mypred[0])+abs(mypred[1]-1), "move north"))	#up
				moves.append((abs(mypred[0]-1)+abs(mypred[1]), "move east"))	#right
				moves.append((abs(mypred[0])+abs(mypred[1]+1), "move south"))	#down
			else: 
				moves.append((abs(mypred[0])+abs(mypred[1]+1), "move south"))	#down
				moves.append((abs(mypred[0]-1)+abs(mypred[1]), "move east"))	#right
				moves.append((abs(mypred[0])+abs(mypred[1]-1), "move north"))	#up
	else:
		# y is larger!

		if myself[1] > 0:
			moves.append((abs(mypred[0])+abs(mypred[1]-1), "move north"))		#up
			if myself[0] > 0:
				moves.append((abs(mypred[0]-1)+abs(mypred[1]), "move east"))	#right
				moves.append((abs(mypred[0])+abs(mypred[1]+1), "move south"))	#down
				moves.append((abs(mypred[0]+1)+abs(mypred[1]), "move west"))	#left
			else:
				moves.append((abs(mypred[0]+1)+abs(mypred[1]), "move west"))	#left
				moves.append((abs(mypred[0])+abs(mypred[1]+1), "move south"))	#down
				moves.append((abs(mypred[0]-1)+abs(mypred[1]), "move east"))	#right
		else:		
			moves.append((abs(mypred[0])+abs(mypred[1]+1), "move south"))		#down	
			if myself[0] > 0:	
				moves.append((abs(mypred[0]-1)+abs(mypred[1]), "move east"))	#right
				moves.append((abs(mypred[0])+abs(mypred[1]-1), "move north"))	#up
				moves.append((abs(mypred[0]+1)+abs(mypred[1]), "move west"))	#left
			else:
				moves.append((abs(mypred[0]+1)+abs(mypred[1]), "move west"))	#left
				moves.append((abs(mypred[0])+abs(mypred[1]-1), "move north"))	#up
				moves.append((abs(mypred[0]-1)+abs(mypred[1]), "move east"))	#right
	
	# take move which is most preferred, but does avoid collision.
	for i in moves:
		if i[0] > 4:		
			return i[1]

	# if there is no move possible, move away from predator
	# (can occure after initialization)
	if abs(mypred[0]) > abs(mypred[1]):
		# move along x-dir
		if mypred[0] > 0:
			# predator is right, --> move left
			return "move west"
		else:
			# predator is left, --> move right
			return "move east"
	else:
		# move along y-dir
		if mypred[1] > 0:
			# predator is up, --> move down
			return "move south"
		else:
			# predator is down, --> move up
			return "move north"

	return "move none"
