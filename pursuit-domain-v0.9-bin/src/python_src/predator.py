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
# MAIN CLASS
class QPredator:

    sock = None
    Qlearn = False
    Q = {}
    crtstate = ''
    prevstate = '' 
    distance2prey = 0 
   
    mindis = 7

    r = -1

    # Learning parameters
    alpha = 0.99
    gamma = 1
    l = 0.9
    epsilon = 0.1
    preyx = 0
    preyy = 0

    tau = 0.999
    episodesran = 0

    def __init__(self, Q):
      self.Q = Q

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
            self.preyx = int(x)
            self.preyy = int(y)

            #print self.distance2prey
            if(self.distance2prey<self.mindis): 
              self.Qlearn = True
            preystate += '%02d%02d' % (int(x)+7, int(y)+7)
          else:
            predstate += '%02d%02d' % (int(x)+7,int(y)+7)
        state = preystate+predstate
        self.crtstate = state


    # determines the next movement command for this agent
    def determineMovementCommand( self ):

      if(not (self.Qlearn) or (self.Qlearn and self.prevstate=='')):
        if(self.preyy>self.preyx):
          if(self.preyx>0):
            msg = "(move east)"
          else:
            msg = "(move west)"

        elif(self.preyx>self.preyy):
          if(self.preyy>-1):
            msg = "(move north)"
          else:
            msg = "(move south)"
        else:
          msg = "(move none)"
      else:
        if(random.random()<self.epsilon):
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
        if(self.distance2prey>self.mindis+1):
          self.Qlearn = False
          self.r = -200
          
        self.Q[self.prevstate] = self.Q.get(self.prevstate,0)+ self.alpha*(self.r+self.gamma*(self.Q.get(self.crtstate,0)-self.Q.get(self.prevstate,0)))
      
        if(self.distance2prey>self.mindis+1):
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

       self.episodesran +=1
       if(self.episodesran % 1000 == 0):
         p = open("Qmatrices/CrtQ", "wb")
         pickle.dump(self.Q, p)
         p.close()      
       self.tau *= self.tau
       self.epsilon *= self.tau

       if(self.episodesran % 5000 == 0):
         self.mindis += 0
    
    def processCollision( self ):
       # TODO: is called when predator collided or penalized
       self.r = -1
       self.Q[self.prevstate] = self.Q.get(self.prevstate,0)+ self.alpha*(self.r+self.gamma*(self.Q.get(self.crtstate,0)-self.Q.get(self.prevstate,0)))

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



if __name__ == "__main__":
	predator = QPredator2()	
	predator.connect()
	predator.mainLoop()
