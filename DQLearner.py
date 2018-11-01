import numpy as np
import keras
import h5py
from collections import deque
from keras.layers import Input, Conv2D, Flatten, Dense, concatenate
from keras.models import Model
from keras.optimizers import RMSprop 
import random

class DQLearner(object):
	"""docstring for DQLearner"""
	def __init__(self):
		self.gamma = 0.95 
		self.epsilon = 0.1
		self.learning_rate = 0.0002
		self.memory = []
		self.model = self.get_model()
		self.action_size = 2

	def __str__(self):
		return "This is deep q learning module\n"

	def get_model(self):
		inp1 = Input(shape=(12, 12, 1))
		inp2 = Input(shape=(12, 12, 1))
		inp3 = Input(shape=(2, 1))

		x1 = Conv2D(16, (4, 4), strides=(2, 2), activation='relu')(inp1)
		x1 = Conv2D(32, (2, 2), strides=(1, 1), activation='relu')(x1)
		x1 = Flatten()(x1)
		x2 = Conv2D(16, (4, 4), strides=(2, 2), activation='relu')(inp2)
		x2 = Conv2D(32, (2, 2), strides=(1, 1), activation='relu')(x2)
		x2 = Flatten()(x2)
		x3 = Flatten()(inp3)
		x = concatenate([x1, x2, x3])
		x = Dense(128, activation='relu')(x)
		x = Dense(64, activation='relu')(x)
		x = Dense(2, activation='linear')(x)

		model = Model(inputs=[inp1, inp2, inp3], outputs=[x])
		model.compile(optimizer=RMSprop(lr=self.learning_rate), loss='mse')

		return model

	def act(self,state):
		if np.random.rand() <= self.epsilon:
			return random.randrange(self.action_size)
		act_values = self.model.predict(state)
		return np.argmax(act_values[0])

	def push(self,state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))


	def fit(self,batch_size):
		minibatch = random.sample(self.memory, batch_size)
		for state, action, reward, next_state, done in minibatch:
			new_reward = reward
			if not done:
				new_reward = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
			target = self.model.predict(state)
			target[0][action] = new_reward
			self.model.fit(state, target, epochs=1, verbose=0)



	def load(self, name):
		self.model.load_weights(name)

	def save(self, name):
		self.model.save_weights(name)
