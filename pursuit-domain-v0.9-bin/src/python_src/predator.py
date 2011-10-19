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


# MAIN CLASS
class Ass2Predator:
	sock = None
	
	l = 0.9
	gamma = 1
	epsilon = 0.1
	Q = {}
	crtstate = []
	
	qlearn = False

	distance2prey = (28,28)
	distance2predator = (28,28)
	preycoordinates = (0,0)
	predatorcoordinates = (0,0)

    # processes the incoming visualization messages from the server
	def processVisualInformation( self, msg ):
		if string.find( msg, '(see)' ) == 0:
			return
		# strip the '(see ' and the ')'
		msg = msg[6:-3]
		observations = string.split(msg, ') (')
		preystate = ''
		predstate = ''
		for o in observations:
			(obj, x, y) = string.split(o, " ")
			#print obj + " seen at (" + x + ", " + y + ")"
			if(obj=='prey'):
				self.distance2prey = (abs(int(x)), abs(int(y)))
				preystate += '%02d%02d' % (int(x)+7, int(y)+7)
				self.preycoordinates = (int(x), int(y))
			else:
				predstate += '%02d%02d' % (int(x)+7,int(y)+7)
				self.predatorcoordinates = (int(x), int(y))
		state = preystate+predstate
		self.crtstate.append(state)
		
    # determines the next movement command for this agent
	def determineMovementCommand( self ):
		if self.distance2prey[0]+self.distance2prey[1] <= 6 and not self.qlearn:
			print 'Start QLEARN'
			self.qlearn = True

		if not self.qlearn:
			msg = self.movepreQ(self.preycoordinates, self.predatorcoordinates)		
		else:
			if self.distance2prey[0]+self.distance2prey[1] > 9:
				self.updateQValues(-2)
			else:
				self.updateQValues(-1)

			if random.random() < self.epsilon:
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
			else:
				possible_states = self.getAllPossibleStates()
				new_state = self.selectBestPossibleState(possible_states)
				new_x = int(new_state[0]+new_state[1])-7
				new_y = int(new_state[2]+new_state[3])-7
				old_x = self.preycoordinates[0]
				old_y = self.preycoordinates[1]
				
				if new_x > old_x:
					msg = "(move east)"
				elif new_x < old_x:
					msg = "(move west)"
				elif new_y > old_y:
					msg = "(move north)"
				elif new_y < old_y:
					msg = "(move south)"
				else:
					msg = "(move none)"
		return msg

	# move, when Qlearning is not yet activated	
	def movepreQ(self, myself, mypred):
		# determine collision-free move.
		# returns 'msg' which is a string describing the move 

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

	# Update Q value of previous states 
	def updateQValues( self, reward):
		for state_index in range(len(self.crtstate), 1,-1):
			self.Q[self.crtstate[state_index-1]] = ( (1-self.l)*self.Q.get(self.crtstate[state_index-1],0)
				+ self.l*(reward+self.gamma*self.Q.get(self.crtstate[-1],0)) )

	def selectBestPossibleState( self, possible_states):
		max_states = []
		max_q = float('-inf')
		for state in possible_states:
			if self.Q.get(state,0) == max_q:
				max_states.append(state)
			elif self.Q.get(state,0) > max_q:
				max_states = [state]
				max_q = self.Q.get(state,0)
		return max_states[random.randint(0, len(max_states)-1)]

	def	getAllPossibleStates( self ):
		next_prey_coord = ( self.generateNextCoordinateStates( 
			( int(self.crtstate[-1][0:2]), int(self.crtstate[-1][2:4]) ) 
		))
		next_predator_coord = ( self.generateNextCoordinateStates(
			( int(self.crtstate[-1][4:6]), int(self.crtstate[-1][6:8]) )
		))
		return self.permutate( next_prey_coord, next_predator_coord )

	# Return all combinations of list1 and list2
	def permutate( self, list1, list2 ):
		if len(list1) > 0:
			elem1 = list1.pop()
			result = self.permutate(list1, list2)
			for elem2 in list2:
				result.append(elem1+elem2)
			return result
		else:
			return []

	# Given a coordinate, generate all possible next coordinate states
	def generateNextCoordinateStates( self, coordinate ):
		return ([
			'%02d%02d' % (coordinate[0],coordinate[1]),
			'%02d%02d' % (coordinate[0],(coordinate[1]+1) % 15),
			'%02d%02d' % (coordinate[0],(coordinate[1]-1) % 15),
			'%02d%02d' % ((coordinate[0]+1) % 15,coordinate[1]),
			'%02d%02d' % ((coordinate[0]-1) % 15,coordinate[1])
		])

	# determine a communication message 
	def determineCommunicationCommand( self ):
		return ""

	# process the incoming visualization messages from the server   
	def processCommunicationInformation( self, str ):
		pass

	def processEpisodeEnded( self ):
		self.updateQValues(0)
		print 'Stop QLEARN and empty state stack'
		self.qlearn = False
		self.crtstate = [] 
	
	def processCollision( self ):
		self.updateQValues(-20)
	
	def processPenalize( self ):
		self.updateQValues(-10)

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



if __name__ == "__main__":
	predator = Ass2Predator()	
	predator.connect()
	predator.mainLoop()
