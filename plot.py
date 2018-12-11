# to plot results
import matplotlib.pyplot as plt
import pandas as pd


def plot_trained():
	df_trained = pd.read_csv('trained_data.csv')
	plt.plot(df_trained['episode'],df_trained['waiting_time'],'b-',label="Trained")
	plt.xlabel('episode')
	plt.ylabel('waiting time (s)')
	plt.show()

def plot_untrained():
	df_untrained = pd.read_csv('untrained_data.csv')
	plt.plot(df_untrained['episode'],df_untrained['waiting_time'],'r-',label="Untrained")
	plt.xlabel('episode')
	plt.ylabel('waiting time (s)')
	plt.show()


# plot_untrained()

def plot_trained_vs_untrained_reward():
	df_trained = pd.read_csv('trained_data.csv')
	df_untrained = pd.read_csv('untrained_data.csv')

	plt.plot(df_trained['episode'],-df_trained['reward'],'b-',label="Trained")
	plt.plot(df_untrained['episode'],-df_untrained['reward'],'r-',label="Untrained")
	plt.xlabel('episode')
	plt.ylabel('reward')
	plt.show()

	avg_reward_T = -sum(df_trained['reward'])
	avg_reward_U = -sum(df_untrained['reward'])
	print("reward T",avg_reward_T," avg_reward_U ",avg_reward_U, "difference ",avg_reward_T-avg_reward_U)


plot_trained_vs_untrained_reward()


def plot_trained_vs_untrained_wt():		
	df_trained = pd.read_csv('trained_data.csv')
	df_untrained = pd.read_csv('untrained_data.csv')

	plt.plot(df_trained['episode'],df_trained['waiting_time'],'b-',label="Trained")
	plt.plot(df_untrained['episode'],df_untrained['waiting_time'],'r-',label="Untrained")
	plt.xlabel('episode')
	plt.ylabel('waiting time(s)')
	plt.show()

	# total_time_trained =  sum(df_trained['waiting_time'])
	# total_time_untrained = sum(df_untrained['waiting_time'])
	# print(total_time_untrained,total_time_trained,total_time_untrained- total_time_trained)

	# time : 1016174 866401 149773


