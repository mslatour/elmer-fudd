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
    V = {}
    crtstate = []

	distance2prey = (28,28)
	distance2predator = (28,28)

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
            print obj + " seen at (" + x + ", " + y + ")"
            if(obj=='prey'):
			  self.distance2prey = (int(x)+7, int(y)+7)
              preystate += '%02d%02d' % distance2prey
            else:
              predstate += '%02d%02d' % (int(x)+7,int(y)+7)

            # implementation should be done by students
            # TODO: process these relative x and y coordinates
            state = preystate+predstate
            self.crtstate.append(state)


    # determines the next movement command for this agent
    def determineMovementCommand( self ):
		if self.distance2prey[0]+self.distance2prey[1] <= 6 and not self.qlearn:	
			self.qlearn = True
			
		if not self.qlearn
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
			self.updateQValues(len(self.crtstate)-1)
			possible_states = self.getAllPossibleStates()
			new_state = self.selectBestPossibleState(possible_states)
			new_x = int(new_state[0]+new_state[1])
			new_y = int(new_state[2]+new_state[3])
			old_x = self.distance2prey[0]
			old_y = self.distance2prey[1]
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

	# Update Q value of previous states 
	def updateQValues( self, state_index):
		if state_index > 0:
			r = -1 # reward
			Q[self.crtstate[state_index-1]] = (1-self.l)*Q.get(self.crtstate[state_index-1])+self.l*(r+self.gamma*V.get(self.crtstate[state_index]))
			self.updateQValues(state_index-1)
		else:
			pass

	def selectBestPossibleState( self, possible_states):
		pass

	def	getAllPossibleStates( self ):
		next_prey_coord = self.generateNextCoordinateStates( self.distance2prey )
		next_predator_coord = self.generateNextCoordinates( self.distance2predator )
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
		result = []
		result.append( '%02d%02d' % (coordinate[0],coordinate[1])
		result.append( '%02d%02d' % (coordinate[0],(coordinate[1]+1) % 15)
		result.append( '%02d%02d' % (coordinate[0],(coordinate[1]-1) % 15)
		result.append( '%02d%02d' % ((coordinate[0]+1) % 15,coordinate[1])
		result.append( '%02d%02d' % ((coordinate[0]-1) % 15,coordinate[1])
		return result

    # determine a communication message 
    def determineCommunicationCommand( self ):
        return ""

    # process the incoming visualization messages from the server   
    def processCommunicationInformation( self, str ):
        pass

    def processEpisodeEnded( self ):
       pass
       
    def processCollision( self ):
       pass

    def processPenalize( self ):
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
	predator = Ass1Predator()	
	predator.connect()
	predator.mainLoop()
