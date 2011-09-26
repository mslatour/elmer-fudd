#!/usr/bin/python

from socket import *
import string
import random
import math

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
	grid_size = 15

	# When initialized:
	# A matrix with a row for each prey, where each row contains:
	# [
	# 	total_dist, 	The cumulative distance of all predators to the prey
	#	myPredCoords	The relative coordinates of the prey viewed from me
	#	iPredCoords		The relative coordinates of the prey viewed from predator i.
	#	....	The relative coordinates of the prey viewed from predator i+1, i+2, ...
	# ]
	prey_distance_matrix = []
	
	def determineMovementCommand( self ):
		msg = "(move none)"

		prey_vector = self.getClosestPreyMatrix(self.prey_distance_matrix)
		formation_matrix = self.extractFormationMatrix(prey_vector)

		print myself

		if abs(myself[0]) > abs(myself[1]):
			if myself[0] > 0:
				msg = "(move east)"
			else:
				msg = "(move west)"
		else:
			if myself[1] > 0:
				msg = "(move north)"
			else:
				msg = "(move south)"  

		print msg
		return msg

	def getClosestPreyVector(prey_matrix):
		pass

	def extractFormationMatrix(prey_vector):
		formation_matrix = []
		for( i in range(1,len(prey_vector)-1) ):
			formation_matrix.append(
				[
					abs(prey_vector[i][0])+abs(rey_vector[i][1]+1),
					abs(prey_vector[i][0]+1)+abs(prey_vector[i][1]),
					abs(prey_vector[i][0])+abs(prey_vector[i][1]-1),
					abs(prey_vector[i][0]-1)+abs(prey_vector[i][1])
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
			self.prey_distance_matrix.append([abs(p[0])+abs(p[1]), p])			
			for pr in preds:
				dx = p[0] - pr[0] 	
				if dx > math.floor(.5*gridsize):
					dx -= gridsize
				elif dx < math.floor(.5*gridsize):
					dx += gridsize
				dy = p[1] - pr[1]
				if dy > math.floor(.5*gridsize):
					dy -= gridsize
				elif dy < math.floor(.5*gridsize):
					dy += gridsize
				self.prey_distance_matrix[-1].append((dx,dy))
				self.prey_distance_matrix[-1][0] += abs(dx)+abs(dy)
			
		self.prey_distance_matrix.sort()

		#print str(self.prey_distance_matrix)
	
	def processEpisodeEnded( self ):
    	# TODO: initialize used variables (if any)
		pass
       
	def processCollision( self ):
    	# TODO: is called when predator collided or penalized
		pass

	def processPenalize( self ):
    	# TODO: is called when predator collided or penalized
		pass

if __name__ == "__main__":

    predator = Assignment1Predator()
    predator.connect()
    predator.mainLoop()
