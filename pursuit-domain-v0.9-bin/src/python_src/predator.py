#!/usr/bin/python

from socket import *
import string
import random
import math
	
gridsize = 15

# MAIN CLASS
class Predator:

    sock = None

    # processes the incoming visualization messages from the server
    def processVisualInformation( self, msg ):
        
        if string.find( msg, '(see)' ) == 0:
            return
        # strip the '(see ' and the ')'
        msg = msg[6:-3]
        observations = string.split(msg, ') (')
        for o in observations:
            (obj, x, y) = string.split(o, " ")
            print obj + " seen at (" + x + ", " + y + ")"
            # implementation should be done by students            
            # TODO: process these relative x and y coordinates

    # determines the next movement command for this agent
    def determineMovementCommand( self ):

        rand = random.randint(0, 4)                   
        if(rand == 0):
          msg = "(move south)"
        elif(rand == 1):
          msg = "(move north)"
        elif(rand == 2):
          msg = "(move west)"
        elif(rand == 3):
          msg = "(move east)"
        elif(rand == 4):
          msg = "(move none)"

        return msg

    # determine a communication message 
    def determineCommunicationCommand( self ):
        # TODO: Assignment 3
        return ""

    # process the incoming visualization messages from the server   
    def processCommunicationInformation( self, str ):
        # TODO: Assignment 3
        pass

    def processEpisodeEnded( self ):
       # TODO: initialize used variables (if any)
       pass
       
    def processCollision( self ):
       # TODO: is called when predator collided or penalized
       pass

    def processPenalize( self ):
       # TODO: is called when predator collided or penalized
       pass

    # BELOW ARE METODS TO CALL APPROPRIATE METHODS; CAN BE KEPT UNCHANGED
    def connect( self, host='', port=4001 ):
        self.sock = socket( AF_INET, SOCK_DGRAM)                  
        self.sock.bind( ( '', 0 ) )                               
        self.sock.sendto( "(init predator)" , (host, port ) )       
        pass
  
    def mainLoop( self ):
        msg, addr = self.sock.recvfrom( 1024 )                    
        self.sock.connect( addr )                                 
        ret = 1
        while ret:
            msg = self.sock.recv( 1024 )                            
            if string.find( msg, '(quit' ) == 0 :
                # quit message
                ret = 0                                       

            elif string.find( msg, '(hear' ) == 0 :
                # process audio
                self.processCommunicationInformation( msg )

            elif string.find( msg, '(see' ) == 0 :
                # process visual
                self.processVisualInformation( msg )

                msg = self.determineCommunicationCommand( )
                if len(msg) > 0:
                    self.sock.send( msg )
        
            elif string.find( msg, '(send_action' ) == 0 :  
                msg = self.determineMovementCommand( )
                self.sock.send( msg )           

            elif string.find( msg, '(referee episode_ended)' ) == 0:  
                msg = self.processEpisodeEnded( )
         
            elif string.find( msg, '(referee collision)' ) == 0:  
                msg = self.processCollision( )

            elif string.find( msg, '(referee penalize)' ) == 0:  
                msg = self.processPenalize( )
                
            else:
                print "msg not understood " + msg
        self.sock.close()                                         
        pass
  
# SimplePredator CLASS

class SimplePredator(Predator):
	prey_distance_matrix = []
	
	def determineMovementCommand( self ):
		msg = "(move none)"		
		closestprey = sorted(self.prey_distance_matrix)[0]
		x = closestprey[1]
		y = closestprey[2]	

		if abs(x) > abs(y):
			#walk x direction
			if x > 0:
				msg = "(move east)"
			else:
				msg = "(move west)"
		else:
			#walk y direcrion
			if y > 0:
				msg = "(move north)"
			else:
				msg = "(move south)"
		return msg
    
	def processVisualInformation( self, msg ): 
		self.prey_distance_matrix = []
		if string.find( msg, '(see)' ) == 0:
			return
		# strip the '(see ' and the ')'
		msg = msg[6:-3]
		observations = string.split(msg, ') (')
		for o in observations:
			(obj, x, y) = string.split(o, " ")
			print obj + " seen at (" + x + ", " + y + ")"
			if( obj == "prey" ):
				# Calculate euclid distance
				dist = math.hypot(float(x),float(y))
				# Store tuple of the distance, x and y
				self.prey_distance_matrix.append((dist,int(x),int(y)))
	
	def processEpisodeEnded( self ):
    	# TODO: initialize used variables (if any)
		pass
       
	def processCollision( self ):
    	# TODO: is called when predator collided or penalized
		pass

	def processPenalize( self ):
    	# TODO: is called when predator collided or penalized
		pass
	
# Assignment1Predator CLASS
class Assignment1Predator(Predator):

	# When initialized:
	# A matrix with a row for each prey, where each row contains:
	# [
	# 	total_dist, 	The cumulative distance of all predators to the prey
	#	[
	#		(dist, x, y),	The relative coordinates of the prey viewed from me
	#		(disti, xi, yi),		The relative coordinates of the prey viewed from predator i
	#		....	The relative coordinates of the prey viewed from predator i+1, i+2, ...
	#	]
	# ]
	prey_distance_matrix = []
	
	def determineMovementCommand( self ):
		msg = "(move none)"
		
		# (me_index, prey_vector) = getClosestPreyVector(distance_matrix)
		prey_vector = self.getClosestPreyVector(self.prey_distance_matrix)
		print "Prey vector:",prey_vector
		me = prey_vector[0]
		
		formation_matrix = self.extractFormationMatrix(prey_vector[1])
		print 'Formation matrix:', formation_matrix
		formation = self.determineBestFormation(formation_matrix)
		print 'Formation:', formation

		print 'My distance to the prey: ',prey_vector[1][me]

		if formation[0] == me:
			# Go to the north position
			dist2formation = (prey_vector[1][me][1], prey_vector[1][me][2]+1)
		elif formation[1] == me:
			# Go to the east position
			dist2formation = (prey_vector[1][me][1]+1, prey_vector[1][me][2])
		elif formation[2] == me:
			# Go to the south position
			dist2formation = (prey_vector[1][me][1], prey_vector[1][me][2]-1)
		else:
			# Go to the west position
			dist2formation = (prey_vector[1][me][1]-1, prey_vector[1][me][2])
		
		msg = self.determineMovement( formation, dist2formation, prey_vector)

		if msg == None:
			msg = '(move none)'
		# make recursive
	
		print msg;	
		return msg

	def determineMovement(self, formation, dist2formation, prey_vector):
		print 'Dist2formation',dist2formation
		if abs(dist2formation[0]) > abs(dist2formation[1]):
			if dist2formation[0] > 0:
				# Check if this is not a single choice for the prey
				if self.determineSingleChoicePrey(formation, prey_vector) == 1:
					# don't move in the same direction as the prey
					# so give precedence to the other coordinate
					if dist2formation[1] == 0:
						print 'Single choice avoid!!'
						print dist2formation
						dist2formation = (dist2formation[0]-gridsize,dist2formation[1])
						print dist2formation
					else:
						dist2formation = (0,dist2formation[1])
						
					return self.determineMovement(formation,dist2formation, prey_vector)
				else:
					return "(move east)"
			else:
				# Check if this is not a single choice for the prey
				if self.determineSingleChoicePrey(formation, prey_vector) == 3:
					# don't move in the same direction as the prey
					# so give precedence to the other coordinate
					if dist2formation[1] == 0:
						print 'Single choice avoid!!'
						print dist2formation
						dist2formation = (dist2formation[0]-gridsize,dist2formation[1])
						print dist2formation
					else:
						dist2formation = (0,dist2formation[1])
					return self.determineMovement(formation, dist2formation, prey_vector)
				else:
					return "(move west)"
		elif abs(dist2formation[1]) > abs(dist2formation[0]):
			if dist2formation[1] > 0:
				# Check if this is not a single choice for the prey
				if self.determineSingleChoicePrey(formation, prey_vector) == 0:
					# don't move in the same direction as the prey
					# so give precedence to the other coordinate
					if dist2formation[0] == 0:
						print 'Single choice avoid!!'
						print dist2formation
						dist2formation = (dist2formation[0],dist2formation[1]-gridsize)
						print dist2formation
					else:
						dist2formation = (dist2formation[0],0)
					return self.determineMovement(formation, dist2formation, prey_vector)
				else:
					return "(move north)"
			else:
				# Check if this is not a single choice for the prey
				if self.determineSingleChoicePrey(formation, prey_vector) == 2:
					# don't move in the same direction as the prey
					# so give precedence to the other coordinate
					if dist2formation[0] == 0:
						print 'Single choice avoid!!'
						print dist2formation
						dist2formation = (dist2formation[0],dist2formation[1]+gridsize)
						print dist2formation
					else:
						dist2formation = (dist2formation[0],0)
				else:
					return "(move south)"
		else:
			if dist2formation[0] == 0:
				return "(move none)"
			else:
				if dist2formation[0] > 0:
					# Check if this is not a single choice for the prey
					if self.determineSingleChoicePrey(formation, prey_vector) == 1:
						# don't move in the same direction as the prey
						# so give precedence to the other coordinate
						dist2formation = (0,dist2formation[1])
						return self.determineMovement(formation, dist2formation, prey_vector)
					else:
						return "(move east)"
				else:
					if self.determineSingleChoicePrey(formation, prey_vector) == 3:
						# don't move in the same direction as the prey
						# so give precedence to the other coordinate
						dist2formation = (0,dist2formation[1])
						return self.determineMovement(formation, dist2formation, prey_vector)
					else:
						return "(move west)"


	# In case there is only one option left for the prey to go to
	# return the direction in which it will move. If there are more
	# positions return None
	def determineSingleChoicePrey(self, formation, prey_vector):
		# Check if three predators are within one cell of the prey
		# because that would mean that there is only one free cell 
		# to where the prey can move
		
		free = None;
			
		for i in range(0, len(formation) ):
			if ( prey_vector[1][formation[i]][0] > 1 ):
				if( free == None ):
					free = i
				else:
					return None
		return free
			
	def determineBestFormation(self,formation_matrix):
		print '\n'
		print '############## DETERMINE BEST FORMATION #################'
		print formation_matrix
		print '---------------------------------------------------------'
		# top, right, bottom, left
		positions = [ 0, 0, 0, 0 ]

		# For each predator i
		for i in range(0, len(formation_matrix)):
			# Determine best position
			closest_pos = self.getClosestFormationPosition(formation_matrix, i)
			print "Closest position for",i,":",closest_pos
			# Check if position is vacant
			if positions[closest_pos] == 0:
				# If position is vacant, store predator i
				print 'Position is vacant, store ',i
				positions[closest_pos] = i
			else:
				# If another predator is already stored on this position
				# then resolve the conflict and retry
				print 'Position is taken by ',positions[closest_pos]
				print 'Resolve conflict between ',i,' and ',positions[closest_pos],', formation_matrix before', formation_matrix
				formation_matrix = self.resolveConflict(formation_matrix, positions[closest_pos], i, closest_pos)
				print 'Conflict resolved, formation after', formation_matrix
				return self.determineBestFormation( formation_matrix )
		return positions;
		
	def getClosestFormationPosition(self,formation_matrix, me):
		my_formation_matrix = formation_matrix[me]
		for vector_index in range(0, len(formation_matrix)):
			if vector_index != me :
				for index in range(0, len(formation_matrix[vector_index])):
					if formation_matrix[vector_index][index] == 0:
						my_formation_matrix[index] += 0.1

		min_index = 0
		min_value = float('inf')
		for index in range(0,len(formation_matrix[me])):
			if formation_matrix[me][index] < min_value:
				min_index = index
				min_value = formation_matrix[me][index]

		return min_index

	def resolveConflict(self,formation_matrix, pred1, pred2, pos):
		if( pred1 < pred2):
			formation_matrix[pred2][pos] = float('inf')
		else:
			formation_matrix[pred1][pos] = float('inf')
		return formation_matrix

	def getClosestPreyVector(self,prey_matrix):
		closest_prey_vector = prey_matrix[0][1]

		l = len(prey_matrix)
		if (l > 1) and (prey_matrix[0][0] == prey_matrix[1][0]):
			num_of_pred = len(prey_matrix[0][1])

			min_dist = prey_matrix[0][0]
			# calculate non-absolute x & y cumulative manhatten distance
			min_cumX = prey_matrix[0][1][0][1]
			min_cumY = prey_matrix[0][1][0][2]
			for i in range(1, num_of_pred):
				min_cumX += prey_matrix[0][1][i][1]	
				min_cumY += prey_matrix[0][1][i][2]	

			for i in range(1,l):
				if prey_matrix[i][0] == min_dist:	
					# calculate non-absoulte x & y cumulative manhatten distance
					cumX = prey_matrix[i][1][0][1]
					cumY = prey_matrix[i][1][0][2]
					for j in range(1, num_of_pred):
						cumX += prey_matrix[i][1][j][1]	
						cumY += prey_matrix[i][1][j][2]

					if (cumX < min_cumX) or ((cumX == min_cumX) and (cumY < min_cumY)):
						closest_prey_vector = prey_matrix[i][1]
						min_cumX = cumX
						min_cumY = cumY
				else:
					break

		# keep track of the reasoning predator.
		myself = closest_prey_vector[0] 
		#sort: manhatten, smallest-x, smalles-y
		closest_prey_vector.sort()
		idx = closest_prey_vector.index(myself)

		return (idx, closest_prey_vector)
		

	def extractFormationMatrix(self,predator_vector):
		formation_matrix = []
		for p in predator_vector:
			formation_matrix.append(
				[
					abs(p[1])+abs(p[2]+1), 
					abs(p[1]+1)+abs(p[2]), 
					abs(p[1])+abs(p[2]-1), 
					abs(p[1]-1)+abs(p[2]) 
				]
			)
		return formation_matrix
    
	def processVisualInformation( self, msg ): 
		self.prey_distance_matrix = []
		if string.find( msg, '(see)' ) == 0:
			return
		# strip the '(see ' and the ')'
		msg = msg[6:-3]
		observations = string.split(msg, ') (')
		
		# get predators and preys
		preys = []
		preds = []
		for o in observations:
			(obj, x, y) = string.split(o, " ")
			print obj + " seen at (" + x + ", " + y + ")"
			if( obj == "prey" ):
				preys.append((int(x),int(y)))
			if( obj == "predator" ):
				preds.append((int(x),int(y)))
		
		for p in preys:
			prey_vector = [abs(p[0])+abs(p[1]), [(abs(p[0])+abs(p[1]), p[0], p[1])]]
			for pr in preds:
				dx = p[0] - pr[0] 	
				# transform dx into smallest distance
				if dx > math.floor(.5*gridsize):
					dx -= gridsize
				elif dx < -1*math.floor(.5*gridsize):
					dx += gridsize
				dy = p[1] - pr[1]
				# transform dy into smallest distance
				if dy > math.floor(.5*gridsize):
					dy -= gridsize
				elif dy < -1*math.floor(.5*gridsize):
					dy += gridsize
				pred_tuple = (abs(dx)+abs(dy), dx, dy)
				prey_vector[1].append(pred_tuple)
				# increase cumulative distance
				prey_vector[0] += pred_tuple[0]
			self.prey_distance_matrix.append(prey_vector)

		# sort on absolute cumulative distance		
		self.prey_distance_matrix.sort()

	def processEpisodeEnded( self ):
    	# TODO: initialize used variables (if any)
		pass
       
	def processCollision( self ):
    	# TODO: is called when predator collided or penalized
		pass

	def processPenalize( self ):
    	# TODO: is called when predator collided or penalized
		pass


# ROBRECHT CLASS
class RobrechtPredator:

    sock = None
    huntprey = None
    predators = []

    # processes the incoming visualization messages from the server
    def processVisualInformation( self, msg ):
        
        if string.find( msg, '(see)' ) == 0:
            return
        # strip the '(see ' and the ')'
        msg = msg[6:-3]
        observations = string.split(msg, ') (')
        hunted = None
        minDisToPrey = float('inf')

        self.huntprey = None
        self.predators = []

        for o in observations:
            (obj, x, y) = string.split(o, " ")
            print obj + " seen at (" + x + ", " + y + ")"
            # implementation should be done by students            
            # TODO: process these relative x and y coordinates
            if(obj=="prey"):
              preyworldview = [(-int(x), -int(y))]
              preyx = int(x)
              preyy = int(y)
              for preds in observations:
                (obj2,predx,predy) = string.split(preds, " ")
                if(obj2=="predator"):
                  gridhalf = math.floor(gridsize/2)
                  predx = int(predx)
                  predy = int(predy)
                  xdis = ((-(preyx-predx)+gridhalf)%gridsize)-gridhalf
                  ydis = ((-(preyy-predy)+gridhalf)%gridsize)-gridhalf

                  preyworldview.append((xdis, ydis))
              print "Prey world view",  preyworldview

              crtDisToPrey = 0
              for (i,j) in preyworldview:
                crtDisToPrey += abs(i)+abs(j)

              if crtDisToPrey<minDisToPrey:
                minDisToPrey = crtDisToPrey
                hunted = preyworldview
              print "Minimum distance prey", minDisToPrey, "Current distance prey", crtDisToPrey
            else:
              self.predators.append((int(x), int(y)))
        self.huntprey = hunted

    # determines the next movement command for this agent
    def determineMovementCommand( self ):
        print "View from prey",  self.huntprey
        print "Other predators", self.predators

        msg = "(move none)"
        minx = float('inf')
        miny = float('inf')
        
        (ownx, owny) = self.huntprey[0]
        ownx *= -1
        owny *= -1

        # East, West, South, North
        possiblesquares = [(ownx-1, owny), (ownx+1, owny), (ownx, owny-1), (ownx, owny+1)]
        
        for (tryx, tryy) in possiblesquares:
          if(abs(tryx)+abs(tryy)<abs(minx)+abs(miny)):
            for (x2,y2) in self.predators:
              if(tryx != x2 and tryy != y2):
                minx = tryx
                miny = tryy
        
        possiblethreats = [(float('inf'), float('inf'))]

        for (x2,y2) in self.predators:
          if(abs(x2)+abs(y2)<3):
            possiblesquares2 = [(ownx-x2-1, owny-y2), (ownx-x2+1, owny-y2), (ownx-x2, owny-y2-1), (ownx-x2, owny-y2+1)]
            minx2 = float('inf')
            miny2 = float('inf')
            for (tryx2, tryy2) in possiblesquares2:
              if(abs(tryx2)+abs(tryy2)<abs(minx2)+abs(miny2)):
                for (x3,y3) in self.predators + [(-x2,-y2)]:
                  if(tryx2 != x3 and tryy2 != y3):
                    minx2 = tryx2
                    miny2 = tryy2
            if(  (abs(minx2) < abs(miny2)) and miny2<0):
              newpred = (x2, y2-1)
              msg2 = "(move south)"
            elif((abs(minx2) < abs(miny2)) and miny2>0):
              newpred = (x2, y2+1)
              msg2 = "(move north)"
            elif(minx2>0):
              newpred = (x2+1, y2)
              msg2 = "(move west)"
            elif( minx2<0):
              newpred = (x2-1, y2)
              msg2 = "(move east)"
            else:
              newpred = (x2, y2)
              msg2 = "(move none)"
            print "Other predator as", x2,y2,msg2
            possiblethreats.append(newpred)
        
        print "Min X and Min Y", minx,miny
        print possiblethreats
        if(  (abs(minx) < abs(miny)) and miny<0):
          for (posx, posy) in possiblethreats:
            if(posy == -1 and posx == 0):
              msg = "(move none)"
            else:
              msg = "(move south)"
        elif((abs(minx) < abs(miny)) and miny>0):
          for (posx, posy) in possiblethreats:
            if(posy == 1 and posx ==0):
              msg = "(move none)"
            else:
              msg = "(move north)"
        elif(minx<0):
          for (posx, posy) in possiblethreats:
            if(posx == 1 and posy==0):
              msg = "(move none)"
            else:
              msg = "(move west)"
        elif( minx>0):
          for (posx, posy) in possiblethreats:
            if(posx == -1 and posy==0):
              msg = "(move none)"
            else:
              msg = "(move east)"
        else:
          msg = "(move none)"

        surrounding = True
        for (x2,y2) in self.huntprey[1:]:
          if(abs(x2)+abs(y2)>1):
            surrounding = False

        if(surrounding):
          if(minx>ownx and abs(miny)<2):
            msg = "(move west)"
          if(minx<ownx and abs(miny)<2):
            msg = "(move east)"
          if(miny>owny and abs(minx)<2):
            msg = "(move north)"
          if(miny<owny and abs(minx)<2):
            msg = "(move south)"

        return msg

    # determine a communication message 
    def determineCommunicationCommand( self ):
        # TODO: Assignment 3
        return ""

    # process the incoming visualization messages from the server   
    def processCommunicationInformation( self, str ):
        # TODO: Assignment 3
        pass

    def processEpisodeEnded( self ):
       # TODO: initialize used variables (if any)
       pass
       
    def processCollision( self ):
       # TODO: is called when predator collided or penalized
       pass

    def processPenalize( self ):
       # TODO: is called when predator collided or penalized
       pass

    # BELOW ARE METODS TO CALL APPROPRIATE METHODS; CAN BE KEPT UNCHANGED
    def connect( self, host='', port=4001 ):
        self.sock = socket( AF_INET, SOCK_DGRAM)                  
        self.sock.bind( ( '', 0 ) )                               
        self.sock.sendto( "(init predator)" , (host, port ) )       
        pass
  
    def mainLoop( self ):
        msg, addr = self.sock.recvfrom( 1024 )                    
        self.sock.connect( addr )                                 
        ret = 1
        while ret:
            msg = self.sock.recv( 1024 )                            
            if string.find( msg, '(quit' ) == 0 :
                # quit message
                ret = 0                                       

            elif string.find( msg, '(hear' ) == 0 :
                # process audio
                self.processCommunicationInformation( msg )

            elif string.find( msg, '(see' ) == 0 :
                # process visual
                self.processVisualInformation( msg )

                msg = self.determineCommunicationCommand( )
                if len(msg) > 0:
                    self.sock.send( msg )
        
            elif string.find( msg, '(send_action' ) == 0 :  
                msg = self.determineMovementCommand( )
                self.sock.send( msg )           

            elif string.find( msg, '(referee episode_ended)' ) == 0:  
                msg = self.processEpisodeEnded( )
         
            elif string.find( msg, '(referee collision)' ) == 0:  
                msg = self.processCollision( )

            elif string.find( msg, '(referee penalize)' ) == 0:  
                msg = self.processPenalize( )
                
            else:
                print "msg not understood " + msg
        self.sock.close()                                         
        pass
 

# ROBRECHT2 CLASS
class Robrecht2Predator:

    sock = None
    huntprey = None
    predators = []

    possiblecells = [1,2,3,4]
    following = [0]

    # processes the incoming visualization messages from the server
    def processVisualInformation( self, msg ):
        
        if string.find( msg, '(see)' ) == 0:
            return
        # strip the '(see ' and the ')'
        msg = msg[6:-3]
        observations = string.split(msg, ') (')
        hunted = None
        minDisToPrey = float('inf')

        self.huntprey = None
        self.predators = []

        for o in observations:
            (obj, x, y) = string.split(o, " ")
            print obj + " seen at (" + x + ", " + y + ")"
            # implementation should be done by students            
            # TODO: process these relative x and y coordinates
            if(obj=="prey"):
              preyworldview = [(-int(x), -int(y))]
              preyx = int(x)
              preyy = int(y)
              for preds in observations:
                (obj2,predx,predy) = string.split(preds, " ")
                if(obj2=="predator"):
                  gridhalf = math.floor(gridsize/2)
                  predx = int(predx)
                  predy = int(predy)
                  xdis = ((-(preyx-predx)+gridhalf)%gridsize)-gridhalf
                  ydis = ((-(preyy-predy)+gridhalf)%gridsize)-gridhalf

                  preyworldview.append((xdis, ydis))
              print "Prey world view",  preyworldview

              crtDisToPrey = 0
              for (i,j) in preyworldview:
                crtDisToPrey += abs(i)+abs(j)

              if crtDisToPrey<minDisToPrey:
                minDisToPrey = crtDisToPrey
                hunted = preyworldview
              print "Minimum distance prey", minDisToPrey, "Current distance prey", crtDisToPrey
            else:
              self.predators.append((int(x), int(y)))
        
        self.huntprey = hunted
        self.following =[0]
        print "Hunted", hunted
        if(self.following==[0]):
          (x,y) = hunted[0]
          print "X and Y", x,y
          if(x==1 and y==0):
            self.following = [1]
            print "Start 1"
          elif(x==-1 and y==0):
            self.following = [2]
            print "Start 2"
          elif(x==0 and y==-1):
            self.following = [3]
            print "Start 3"
          elif(x==0 and y==1):
            self.following = [4]
            print "Start 4"
        print "Possible Squares", self.possiblecells
        for (huntx, hunty) in hunted:
          if(huntx==-1 and hunty==0):
            if(self.possiblecells.count(2)>0):
              self.possiblecells.remove(2)
            else:
              self.possiblecells.append(2)
          if(huntx==1 and hunty==0):
            if(self.possiblecells.count(1)>0):
              self.possiblecells.remove(1)
            else:
              self.possiblecells.append(1)
          if(huntx==0 and hunty==-1):
            if(self.possiblecells.count(3)>0):
              self.possiblecells.remove(3)
            else:
              self.possiblecells.append(3)
          if(huntx==0 and hunty==0):
            if(self.possiblecells.count(4)>0):
              self.possiblecells.remove(4)
            else:
              self.possiblecells.append(4)
              
              # determines the next movement command for this agent
    def determineMovementCommand( self ):
        print "View from prey",  self.huntprey
        print "Other predators", self.predators

        msg = "(move none)"

        (ownx, owny) = self.huntprey[0]
        ownx *= -1
        owny *= -1
        
        print "Following", self.following
        print "Prey at", ownx, owny

        

        # Following behaviour to maintain position
        if(self.following[0] == 1):
          print "Following East"
          if(ownx==2):
            return "(move east)"
          if(owny==1):
            return "(move north)"
          if(owny==-1):
            return "(move south)"
          return "(move none)"
        elif(self.following[0] == 2):
          print "Following West"
          if(ownx==-2):
            return "(move west)"
          if(owny==1):
            return "(move north)"
          if(owny==-1):
            return "(move south)"         
          return "(move none)"
        elif(self.following[0] == 3):
          print "Following South"
          if(owny==2):
            return "(move north)"
          if(ownx==1):
            return "(move east)"
          if(ownx==-1):
            return "(move west)"        
          return "(move none)"
        elif(self.following[0] == 4):
          print "Following North"
          if(owny==-2):
            return "(move south)"
          if(ownx==1):
            return "(move east)"
          if(ownx==-1):
            return "(move west)"
          return "(move none)"

        possiblesquares = []
        # East, West, South, North
        for i in self.possiblecells:
          if(i == 1):
            possiblesquares.append((ownx-1, owny))
          elif(i == 2):
            possiblesquares.append((ownx+1, owny))
          elif(i == 3):
            possiblesquares.append((ownx, owny-1))
          elif(i == 4):
            possiblesquares.append((ownx, owny+1))
        minx = float('inf')
        miny = float('inf')

        for (tryx, tryy) in possiblesquares:
          if(abs(tryx)+abs(tryy)<abs(minx)+abs(miny)):
            minx = tryx
            miny = tryy
 
        if(abs(minx)<abs(miny)):
          if(miny>0):
            msg = "(move north)"
          else:
            msg = "(move south)"
        else:
          if(minx>0):
            msg = "(move east)"
          else:
            msg = "(move west)"

        return msg

    # determine a communication message 
    def determineCommunicationCommand( self ):
        # TODO: Assignment 3
        return ""

    # process the incoming visualization messages from the server   
    def processCommunicationInformation( self, str ):
        # TODO: Assignment 3
        pass

    def processEpisodeEnded( self ):
       # TODO: initialize used variables (if any)
       pass
       
    def processCollision( self ):
       # TODO: is called when predator collided or penalized
       print "COLLISION"
       self.following = [0]

    def processPenalize( self ):
       # TODO: is called when predator collided or penalized
       pass

    # BELOW ARE METODS TO CALL APPROPRIATE METHODS; CAN BE KEPT UNCHANGED
    def connect( self, host='', port=4001 ):
        self.sock = socket( AF_INET, SOCK_DGRAM)                  
        self.sock.bind( ( '', 0 ) )                               
        self.sock.sendto( "(init predator)" , (host, port ) )       
        pass
  
    def mainLoop( self ):
        msg, addr = self.sock.recvfrom( 1024 )                    
        self.sock.connect( addr )                                 
        ret = 1
        while ret:
            msg = self.sock.recv( 1024 )                            
            if string.find( msg, '(quit' ) == 0 :
                # quit message
                ret = 0                                       

            elif string.find( msg, '(hear' ) == 0 :
                # process audio
                self.processCommunicationInformation( msg )

            elif string.find( msg, '(see' ) == 0 :
                # process visual
                self.processVisualInformation( msg )

                msg = self.determineCommunicationCommand( )
                if len(msg) > 0:
                    self.sock.send( msg )
        
            elif string.find( msg, '(send_action' ) == 0 :  
                msg = self.determineMovementCommand( )
                self.sock.send( msg )           

            elif string.find( msg, '(referee episode_ended)' ) == 0:  
                msg = self.processEpisodeEnded( )
         
            elif string.find( msg, '(referee collision)' ) == 0:  
                msg = self.processCollision( )

            elif string.find( msg, '(referee penalize)' ) == 0:  
                msg = self.processPenalize( )
                
            else:
                print "msg not understood " + msg
        self.sock.close()                                         
        pass
 

if __name__ == "__main__":

    predator = Robrecht2Predator()
    predator.connect()
    predator.mainLoop()
