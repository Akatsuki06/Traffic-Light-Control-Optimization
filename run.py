#uses SUMOHelper.py and DQlearner.pydoc
# http://www.sumo.dlr.de/daily/pydoc/traci.html
from SUMOHelper import SUMOHelper
from DQLearner import DQLearner
import time
import pandas as pd

agent = DQLearner()
sm = SUMOHelper("/usr/bin/sumo-gui","data/config.sumocfg")

data = []
episodes = 25
batch_size = 64
trained = True

if trained:
	file_name = 'trained_data_128.csv'
	agent.load('models/trained_model.h5')
	print("Trained model loaded")
else:
	file_name = 'untrained_data_128.csv'
	print('No trained models found! Running without trained models.')


for e in range(episodes):
	print("EPISODE ",e)
	sm.start()
	
	step = 0
	waiting_time = 0
	action = 0

	tls = sm.getTrafficLights()
	simulation = sm.getSimulation()
	tls.setPhase("0",0)
	tls.setPhaseDuration("0",200)
	print("step", step)

	while simulation.getMinExpectedNumber()>0 and step < 1000:#no of vehicles in simulation env
		sm.step()
		state = sm.getState()
		action = agent.act(state)
		step,new_state,reward,waiting_time = sm.simulate(waiting_time,action,state[2],tls,step)
		agent.push(state, action, reward, new_state, False)
		if(len(agent.memory) > batch_size):
			agent.fit(batch_size)
		# print("waiting_time: ",waiting_time)

	mem = agent.memory[-1]
	del agent.memory[-1]
	agent.memory.append((mem[0], mem[1], reward, mem[3], True))
	print('episode - ' + str(e) + ' total waiting time - ' + str(waiting_time))
	data.append((e,waiting_time,reward))


# agent.save("trained_model{0}.h5".format(str(time.time())))


df = pd.DataFrame(data,columns=['episode', 'waiting_time', 'reward'])
# df.to_csv(file_name,index=False)
sm.close()
print(data)






