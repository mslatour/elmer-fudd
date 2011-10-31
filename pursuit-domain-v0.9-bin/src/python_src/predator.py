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
class QPredator:

    sock = None
    Qlearn = False
    Q = {}
    crtstate = ''
    prevstate = '' 
    distance2prey = 0 
    
    r = -1

    # Learning parameters
    alpha = 0.9
    gamma = 0.9
    l = 0.9
    epsilon = 0.1


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
            self.distance2prey = abs(int(x))+ abs(int(y))
            #print self.distance2prey
            if(self.distance2prey<7): 
              self.Qlearn = True
            preystate += '%02d%02d' % (int(x)+7, int(y)+7)
          else:
            predstate += '%02d%02d' % (int(x)+7,int(y)+7)
        state = preystate+predstate
        self.crtstate = state


            #print obj + " seen at (" + x + ", " + y + ")"
            # implementation should be done by students            
            # TODO: process these relative x and y coordinates

    # determines the next movement command for this agent
    def determineMovementCommand( self ):

      if(not (self.Qlearn) or (self.Qlearn and self.prevstate=='')):
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
        a =  self.getA()
        if(a==1):
          msg = "(move south)"
        elif(a==2):
          msg = "(move north)"
        elif(a==3):
          msg = "(move west)"
        elif(a==4):
          msg = "(move east)"
        else:
          msg = "(move none)"
        self.crtstate = self.crtstate+str(a)

        # Q-update
        if(self.distance2prey>8):
          self.Qlearn = False
          self.r = -200
          
        self.Q[self.prevstate] = self.Q.get(self.prevstate,0)+ self.alpha*(self.r+self.gamma*(self.Q.get(self.crtstate,0)-self.Q.get(self.prevstate,0)))
      
        if(self.distance2prey>8):
          self.prevstate = ''
      if(self.Qlearn): self.prevstate = self.crtstate

      self.r=-1
      return msg

    def getA(self):

      # lookup 5 (s,a) pairs in Q
      Qvals = range(0,5)
      for i in range(0,5):
          Qvals[i] = self.Q.get(self.crtstate+str(i+1),0)
      # Find maximum Q-values
      maxQ = float('-inf')
      Qacts = []
      for i in range(0,5):
        if(maxQ<Qvals[i]):
          Qacts = [i+1]
          maxQ = Qvals[i]
        elif(maxQ==Qvals[i]):
          Qacts.append(i+1)

      # return random maxQ action
      return random.choice(Qacts)

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
       self.Qlearn = False
       self.prevstate = ''
       self.crtstate = ''
       self.r = -1
       
    def processCollision( self ):
       # TODO: is called when predator collided or penalized
       self.r = -1000

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
class QPredator2:

    sock = None
    Qlearn = False
    Q = {}
    crtstate = ''
    prevstate = ''
    prevprevstate = ''
    predprev = (0,0)
    distance2prey = 0 
    episodes = 0
    preyx = 0
    preyy = 0
    r = -1
    aCorrection = (0,0)

    # Learning parameters
    alpha = 0.9
    gamma = 0.9
    l = 0.9
    epsilon = 0.1

    # processes the incoming visualization messages from the server
    def processVisualInformation( self, msg ):
		if string.find( msg, '(see)' ) == 0:
			return
		# strip the '(see ' and the ')'
		msg = msg[6:-3]
		observations = string.split(msg, ') (')
		preystate = ""
		predstate = ""
		for o in observations:
			(obj, x, y) = string.split(o, " ")
			if(obj=='prey'):
				self.distance2prey = abs(int(x))+ abs(int(y))
				preystate += '%02d%02d' % (int(x)+7, int(y)+7)
				self.preyx = int(x)
				self.preyy = int(y)
				if(self.distance2prey<7): 
					self.Qlearn = True
			else:
				predstate += '%02d%02d' % (int(x)+7,int(y)+7)
				# Extract move made in previous state by other predator
				# and append it to the previous state description
				if not self.prevstate == '':
					if self.predprev[1] > (int(y)+self.aCorrection[1]): # south
						self.prevstate += "0"
					elif self.predprev[1] < (int(y)+self.aCorrection[1]): # north
						self.prevstate += "1"
					elif self.predprev[0] > (int(x)+self.aCorrection[0]): # west
						self.prevstate += "2"
					elif self.predprev[0] < (int(x)+self.aCorrection[0]): # east
						self.prevstate += "3"
					elif self.predprev[0] == (int(x)+self.aCorrection[0]): # none
						self.prevstate += "4"
					else:
						print "Cannot find predator direction"
						print "Relative predator coordinates: (%d, %d)" % (int(x), int(y))
						print "Correction based on my action: (%d,%d)" % (self.aCorrection[0], self.aCorrection[1])
						print "Corrected relative predator coordinates: (%d,%d)" % (int(x)+self.aCorrection[0],int(y)+self.aCorrection[1])
						print "Old relative predator coordinates: (%d,%d)" % (self.predprev[0], self.predprev[1])
				self.predprev = (int(x), int(y))
		state = preystate+predstate
		self.crtstate = state

	# determines the next movement command for this agent
    def determineMovementCommand( self ):
        if(not (self.Qlearn) or (self.Qlearn and self.prevstate=='')):
		  # If this predator is already close enough, 
		  # stay there and wait for the other
          if(abs(self.preyy)>=abs(self.preyx)):
            if(self.preyx>0):
              msg = "(move east)"
              self.aCorrection = (1,0)
            else:
              msg = "(move west)"
              self.aCorrection = (-1,0)

          elif(abs(self.preyx)>abs(self.preyy)):
            if(self.preyy>-1):
              msg = "(move north)"
              self.aCorrection = (0,1)
            else:
              msg = "(move south)"
              self.aCorrection = (0,-1)
        else:
            if(random.random()<self.epsilon):
              a = random.randint(0, 4)                   
              if(a == 0):
                msg = "(move south)"
                self.aCorrection = (0,-1)
              elif(a == 1):
                msg = "(move north)"
                self.aCorrection = (0,1)
              elif(a == 2):
                msg = "(move west)"
                self.aCorrection = (-1,0)
              elif(a == 3):
                msg = "(move east)"
                self.aCorrection = (1,0)
              elif(a == 4):
                msg = "(move none)"
                self.aCorrection = (0,0)
            else:
              a =  self.getA()
              if(a==0):
                self.aCorrection = (0,-1)
                msg = "(move south)"
              elif(a==1):
                self.aCorrection = (0,1)
                msg = "(move north)"
              elif(a==2):
                self.aCorrection = (-1,0)
                msg = "(move west)"
              elif(a==3):
                self.aCorrection = (1,0)
                msg = "(move east)"
              else:
                self.aCorrection = (0,0)
                msg = "(move none)"

            self.crtstate = self.crtstate+str(a)
            # Q-update
            if(self.distance2prey>8):
              self.Qlearn = False
              self.r = -200
            
            if len(self.prevprevstate) == 10:
              self.Q[self.prevprevstate] = self.Q.get(self.prevprevstate,0)+ self.alpha*(self.r+self.gamma*(self.Q.get(self.prevstate,0)-self.Q.get(self.prevprevstate,0)))
      
            if(self.distance2prey>8):
              self.prevprevstate = ''
              self.prevstate = ''
        if(self.Qlearn):
          # Store partial prevstate, predator move will be 
          # appended in the next visual processing
          if len(self.prevstate) == 10:
            self.prevprevstate = self.prevstate
          self.prevstate = self.crtstate

        self.r=-1
        return msg

    def getA(self):
			# lookup 5 (s,a) pairs in Q
			Qvals = {}
			for i in range(0,5):
				for j in range(0,5):
					Qvals[(i,j)] = self.Q.get(self.crtstate+str(i)+str(j),0)
			# Find maximum Q-values
			maxQ = float('-inf')
			Qacts = []
			for k in Qvals:
				if(maxQ<Qvals[k]):
					Qacts = [k[0]]
					maxQ = Qvals[k]
				elif(maxQ==Qvals[k]):
					Qacts.append(k[0])
			
			# return random maxQ action
			return random.choice(Qacts)

    def printState(self, label, state):
		a2str = {"0":"South","1":"North","2":"West","3":"East","4":"None"}
		print label
		print "########################"
		if not state == '':
			print "State: %s" % state
			print "Prey x: %s\nPrey y: %s" % (state[0:2], state[2:4])
			print "Predator x: %s\nPredator y: %s" % (state[4:6], state[6:8])
			if 8 in range(len(state)):
				print "My action: %s" % a2str[state[8]]
			else:
				print "My action: ?"
			if 9 in range(len(state)):
				print "Predator action: %s" % a2str[state[9]]
			else:
				print "Predator action: ?"
		else:
			print "EMPTY"
		print "########################\n"

    # determine a communication message 
    def determineCommunicationCommand( self ):
        # TODO: Assignment 3
        return ""

    # process the incoming visualization messages from the server   
    def processCommunicationInformation( self, str ):
        # TODO: Assignment 3
        pass

    def processEpisodeEnded( self ):
        self.Qlearn = False
        self.prevstate = ''
        self.crtstate = ''
        self.r = -1
        self.episodes = self.episodes + 1
        if self.episodes % 100 == 0:
            print self.episodes
        self.epsilon *= 0.999
       
    def processCollision( self ):
       # TODO: is called when predator collided or penalized
       self.r = -1

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
	
	l = 0.99
	gamma = 0.5
	epsilon = 0.01
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
			return self.movepreQ(self.preycoordinates, self.predatorcoordinates)		
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
		self.updateQValues(-1000)
		self.qlearn = False
		self.crtstate = []
	
	def processPenalize( self ):
		self.updateQValues(-20)

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
	predator = QPredator2()	
	predator.connect()
	predator.mainLoop()
