#uses SUMOHelper.py and DQlearner.py
# getReward issue!
from SUMOHelper import SUMOHelper
from DQLearner import DQLearner

agent = DQLearner()
try:
	agent.load('models/models/trained_model1541685813.2214334.h5')
except:
	print('No trained models found!')

sm = SUMOHelper("/usr/bin/sumo-gui","data/config.sumocfg")
# print(sm, agent)
print(sm.traci)
# sm.start()

episodes = 3
batch_size = 32

for e in range(episodes):
	print("EPISODE ",e)
	sm.start()
	step = 0
	waiting_time = 0
	reward1,reward2,total_reward = 0,0,0
	action = 0

	tls = sm.getTrafficLights()
	simulation = sm.getSimulation()
	tls.setPhase("0",0)
	tls.setPhaseDuration("0",200)

	while simulation.getMinExpectedNumber()>0 and step < 1000:
		sm.step()
		state = sm.getState()
		action = agent.act(state)
		step,new_state,reward,waiting_time = sm.simulate(waiting_time,action,state[2],tls,step)
		agent.push(state, action, reward, new_state, False)
		if(len(agent.memory) > batch_size):
			agent.fit(batch_size)

	mem = agent.memory[-1]
	del agent.memory[-1]
	agent.memory.append((mem[0], mem[1], reward, mem[3], True))
	print('episode - ' + str(e) + ' total waiting time - ' + str(waiting_time))
	sm.close()


		





