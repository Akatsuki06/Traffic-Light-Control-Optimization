import os
import sys

if 'SUMO_HOME' in os.environ:
 tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
 sys.path.append(tools)
else:   
 sys.exit("please declare environment variable 'SUMO_HOME'")



import traci
import numpy as np

class SUMOHelper:
	"""Class to deal with sumo apis"""
	def __init__(self,binary_path,sumo_cfg_path):
		super(SUMOHelper, self).__init__()
		self.traci = traci	
		self.sumoBinary = binary_path
		self.sumoCmd = [self.sumoBinary, "-c", sumo_cfg_path]


	def start(self):
		self.traci.start(self.sumoCmd) 

	def __str__(self):
		return "This is custom SUMO module\n"

	def getTrafficLights(self):
		return self.traci.trafficlight

	def getSimulation(self):
		return self.traci.simulation

	def step(self):
		self.traci.simulationStep()

	def getWaitingTime(self):
		routes = ['1si','2si','3si','4si']
		wt = 0
		for r  in routes:
			wt+=self.traci.edge.getLastStepHaltingNumber(r)

		return wt


	def getReward1(self):
		return self.traci.edge.getLastStepVehicleNumber(
                    '1si') + self.traci.edge.getLastStepVehicleNumber('2si')

	def getReward2(self):
		return self.traci.edge.getLastStepVehicleNumber(
                    '3si') + self.traci.edge.getLastStepVehicleNumber('4si')

	def simulate(self,waiting_time,action,light,tls,step):

		if(action == 0 and light[0][0][0] == 0):# Transition Phase
		    for i in range(6):
		        step += 1
		        tls.setPhase('0', 1)
		        waiting_time += self.getWaitingTime()
		        self.step()
		    for i in range(10):
		        step += 1
		        tls.setPhase('0', 2) 
		        waiting_time += self.getWaitingTime()
		        self.step()
		    for i in range(6):
		        step += 1
		        tls.setPhase('0', 3)
		        waiting_time += self.getWaitingTime()
		        self.step()

		    # Action Execution
		    reward1 = self.getReward1()
		    reward2 = self.getReward2()
		    for i in range(10):
		        step += 1
		        tls.setPhase('0', 4)
		        reward1 += self.getReward1()
		        reward2 += self.getReward2()
		        waiting_time += self.getWaitingTime()
		        self.step()

		if(action == 0 and light[0][0][0] == 1): # Action Execution, no state change
		    reward1 = self.getReward1()
		    reward2 = self.getReward2()
		    for i in range(10):
		        step += 1
		        tls.setPhase('0', 4)
		        reward1 += self.getReward1()
		        reward2 += self.getReward2()
		        waiting_time += self.getWaitingTime()
		        self.step()

		if(action == 1 and light[0][0][0] == 0):
		    reward2 = self.getReward1()#getReward2()
		    reward1 = self.getReward2()
		    for i in range(10):
		        step += 1
		        reward2 += self.getReward1()
		        reward1 += self.getReward2()
		        tls.setPhase('0', 0)
		        waiting_time += self.getWaitingTime()
		        self.step()

		if(action == 1 and light[0][0][0] == 1):
		    for i in range(6):
		        step += 1
		        tls.setPhase('0', 5)
		        waiting_time += self.getWaitingTime()
		        self.step()
		    for i in range(10):
		        step += 1
		        tls.setPhase('0', 6)
		        waiting_time += self.getWaitingTime()
		        self.step()
		    for i in range(6):
		        step += 1
		        tls.setPhase('0', 7)
		        waiting_time += self.getWaitingTime()
		        self.step()

		    reward2 = self.getReward1()
		    reward1 = self.getReward2()
		    for i in range(10):
		        step += 1
		        tls.setPhase('0', 0)
		        reward2 += self.getReward1()
		        reward1 += self.getReward2()
		        waiting_time += self.getWaitingTime()
		        self.step()

		state = self.getState()
		reward = reward1-reward2
		return step,state,reward,waiting_time

	def getState(self):
	    cellLength = 7
	    offset = 11
	    speedLimit = 14

	    junctionPosition = traci.junction.getPosition('0')[0]
	    vehicles_road1 = traci.edge.getLastStepVehicleIDs('1si')
	    vehicles_road2 = traci.edge.getLastStepVehicleIDs('2si')
	    vehicles_road3 = traci.edge.getLastStepVehicleIDs('3si')
	    vehicles_road4 = traci.edge.getLastStepVehicleIDs('4si')

	    positionMatrix = [[0]*12 for y in range(12)] 
	    velocityMatrix = [[0]*12 for y in range(12)]
	   
	    for v in vehicles_road1:
	        ind = int(
	            abs((junctionPosition - traci.vehicle.getPosition(v)[0] - offset)) / cellLength)
	        if(ind < 12):
	            positionMatrix[2 - traci.vehicle.getLaneIndex(v)][11 - ind] = 1
	            velocityMatrix[2 - traci.vehicle.getLaneIndex(
	                v)][11 - ind] = traci.vehicle.getSpeed(v) / speedLimit

	    for v in vehicles_road2:
	        ind = int(
	            abs((junctionPosition - traci.vehicle.getPosition(v)[0] + offset)) / cellLength)
	        if(ind < 12):
	            positionMatrix[3 + traci.vehicle.getLaneIndex(v)][ind] = 1
	            velocityMatrix[3 + traci.vehicle.getLaneIndex(
	                v)][ind] = traci.vehicle.getSpeed(v) / speedLimit

	    junctionPosition = traci.junction.getPosition('0')[1]
	    for v in vehicles_road3:
	        ind = int(
	            abs((junctionPosition - traci.vehicle.getPosition(v)[1] - offset)) / cellLength)
	        if(ind < 12):
	            positionMatrix[6 + 2 -
	                           traci.vehicle.getLaneIndex(v)][11 - ind] = 1
	            velocityMatrix[6 + 2 - traci.vehicle.getLaneIndex(
	                v)][11 - ind] = traci.vehicle.getSpeed(v) / speedLimit

	    for v in vehicles_road4:
	        ind = int(
	            abs((junctionPosition - traci.vehicle.getPosition(v)[1] + offset)) / cellLength)
	        if(ind < 12):
	            positionMatrix[9 + traci.vehicle.getLaneIndex(v)][ind] = 1
	            velocityMatrix[9 + traci.vehicle.getLaneIndex(
	                v)][ind] = traci.vehicle.getSpeed(v) / speedLimit

	    light = []
	    if(traci.trafficlight.getPhase('0') == 4):
	        light = [1, 0]
	    else:
	        light = [0, 1]

	    position = np.array(positionMatrix)
	    position = position.reshape(1, 12, 12, 1)

	    velocity = np.array(velocityMatrix)
	    velocity = velocity.reshape(1, 12, 12, 1)

	    lgts = np.array(light)
	    lgts = lgts.reshape(1, 2, 1)

	    return [position, velocity, lgts]


	def close(self):
		self.traci.close(wait=False)

