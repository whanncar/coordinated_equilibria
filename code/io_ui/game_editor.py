

import Tkinter
from Tkinter import *
import NFG
from NFG import NFG
import file_io
from file_io import load_NFG, save_NFG
import sys
import os
import functools
from functools import partial










def run(game_name, game):
	root = Tkinter.Tk()
	root.geometry('600x600')
	app = Window(game_name, game, root)
	root.mainloop()












class Window(Frame):

	def __init__(self, game_name, game, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.game = game
		self.init_window()

	def init_window(self):
		self.master.title('Game Editor')
		self.pack(fill=BOTH, expand=1)

		self.make_entry_fields()
		self.make_labels()
		self.make_buttons()
		self.make_spaces()

		self.payoff_vars = {}
		self.payoff_vars['state'] = 0
		self.payoff_vars['actions'] = {}

		self.name()


################### Entry, label, and button preparation ######################

	def make_entry_fields(self):
		self.entry_fields = {}
		self.entry_fields['name'] = Text(self, height = 1, width = 50)
		self.entry_fields['players'] = Text(self, height = 1, width = 50)
		self.entry_fields['states'] = Text(self, height = 1, width = 50)
		self.entry_fields['actions'] = {}
		self.entry_fields['payoffs'] = {}

	def make_labels(self):
		self.labels = {}
		self.labels['name'] = Label(self, text='Name: ')
		self.labels['players'] = Label(self, text='Players: ')
		self.labels['states'] = Label(self, text='States: ')
		self.labels['current state'] = Label(self, text='State: ')
		self.labels['current state value'] = Label(self, text='')
		self.labels['actions'] = {}
		self.labels['payoffs'] = {}
		self.labels['payoffs']['players_for_actions'] = []
		self.labels['payoffs']['players_actions'] = []
		self.labels['payoffs']['players_for_payoffs'] = []
		self.labels['payoffs_word'] = Label(self, text='Payoffs:')


	def make_buttons(self):
		self.buttons = {}
		self.buttons['name'] = Button(self, text="Name", command = self.name)
		self.buttons['players'] = Button(self, text="Players", command = self.players)
		self.buttons['states'] = Button(self, text="States", command = self.states)
		self.buttons['actions'] = Button(self, text="Actions", command = self.actions)
		self.buttons['payoffs'] = Button(self, text="Payoffs", command = self.payoffs)
		self.buttons['save'] = Button(self, text="Save", command = self.save)

		self.buttons['state and action togglers'] = []

		for i in range(5):
			x = Label(self, text = ' ')
			x.grid(row=0, column = i)
		self.buttons['name'].grid(row=0, column=5)
		self.buttons['players'].grid(row=1, column=5)
		self.buttons['states'].grid(row=2, column=5)
		self.buttons['actions'].grid(row=3, column=5)
		self.buttons['payoffs'].grid(row=4, column=5)
		self.buttons['save'].grid(row=5, column=5)


	def make_spaces(self):
		self.spaces = []


###############################################################################





################### Methods for retrieving input ##############################



	def get_name(self):
		return self.entry_fields['name'].get('1.0', END).strip()

	def get_players(self):
		players = self.entry_fields['players'].get('1.0', END)
		players = players.strip()
		if players == '':
			return []
		players = players.split(',')
		for i in range(len(players)):
			players[i] = players[i].strip()
		return players

	def get_states(self):
		states = self.entry_fields['states'].get('1.0', END)
		states = states.strip()
		if states == '':
			return []
		states = states.split(',')
		for i in range(len(states)):
			states[i] = states[i].strip()
		return states

	def get_actions(self):
		actions = {}
		players = self.get_players()
		for p in players:
			if p not in self.entry_fields['actions'].keys():
				actions[p] = []
				continue
			actions[p] = self.entry_fields['actions'][p].get('1.0', END)
			actions[p] = actions[p].strip()
			if actions[p] == '':
				actions[p] = []
				continue
			actions[p] = actions[p].split(',')
			for i in range(len(actions[p])):
				actions[p][i] = actions[p][i].strip()
		return actions



###############################################################################




################### UI control methods ########################################



	def hide_all(self):

		players = self.get_players()
		states = self.get_states()
		actions = self.get_actions()

		

		self.entry_fields['name'].grid_forget()
		self.entry_fields['players'].grid_forget()
		self.entry_fields['states'].grid_forget()
		for p in self.entry_fields['actions'].keys():
			self.entry_fields['actions'][p].grid_forget()

		self.labels['name'].grid_forget()
		self.labels['players'].grid_forget()
		self.labels['states'].grid_forget()
		self.labels['current state'].grid_forget()
		self.labels['current state value'].grid_forget()
		for p in self.labels['actions'].keys():
			self.labels['actions'][p].grid_forget()

		d = self.entry_fields['payoffs']
		if (len(states) > 0) and (states[self.payoff_vars['state']] in d.keys()):
			entry_exists = True
			d = d[states[self.payoff_vars['state']]]
			for i in range(len(players)):
				if actions[players[i]][self.payoff_vars['actions'][players[i]]] not in d.keys():
					entry_exists = False
					break
				d = d[actions[players[i]][self.payoff_vars['actions'][players[i]]]]
			if entry_exists:
				for player in players:
					d[player].grid_forget()


		for thing in self.labels['payoffs']['players_for_actions']:
			thing.grid_forget()
		self.labels['payoffs']['players_for_actions'] = []

		for thing in self.labels['payoffs']['players_actions']:
			thing.grid_forget()
		self.labels['payoffs']['players_actions'] = []


		for thing in self.spaces:
			thing.grid_forget()
		self.spaces = []

		for thing in self.buttons['state and action togglers']:
			thing.grid_forget()
		self.buttons['state and action togglers'] = []

		for thing in self.labels['payoffs']['players_for_payoffs']:
			thing.grid_forget()
		self.labels['payoffs']['players_for_payoffs'] = []

		self.labels['payoffs_word'].grid_forget()







	def name(self):
		self.hide_all()
		self.labels['name'].grid(row=1, column=0)
		self.entry_fields['name'].grid(row=1, column=1)


	def players(self):
		self.hide_all()
		self.labels['players'].grid(row=1, column=0)
		self.entry_fields['players'].grid(row=1, column=1)

	def states(self):
		self.hide_all()
		self.labels['states'].grid(row=1, column=0)
		self.entry_fields['states'].grid(row=1, column=1)

	def actions(self):
		self.hide_all()
		players = self.entry_fields['players'].get('1.0', END).strip()
		if players == '':
			return
		players = players.split(',')
		for i in range(len(players)):
			players[i] = players[i].strip()
		for i in range(len(players)):
			if players[i] in self.labels['actions'].keys():
				self.labels['actions'][players[i]].grid(row=i+1, column=0)
				self.entry_fields['actions'][players[i]].grid(row=i+1, column=1)
			else:
				self.labels['actions'][players[i]] = Label(self, text=players[i] + ': ')
				self.labels['actions'][players[i]].grid(row=i+1, column=0)
				self.entry_fields['actions'][players[i]] = Text(self, height = 1, width = 50)
				self.entry_fields['actions'][players[i]].grid(row=i+1, column=1)



	def payoffs(self):
		self.hide_all()		
		self.display_payoffs_for_profile()
		return




	def display_payoffs_for_profile(self):
		players = self.get_players()
		states = self.get_states()
		actions = self.get_actions()

		current_state = self.payoff_vars['state']
		current_actions = {}
		for player in players:
			if player in self.payoff_vars['actions'].keys():
				current_actions[player] = self.payoff_vars['actions'][player]
			else:
				self.payoff_vars['actions'][player] = 0
				current_actions[player] = 0

		d = self.entry_fields['payoffs']
		if states[current_state] not in d.keys():
			d[states[current_state]] = {}
		d = d[states[current_state]]
		for i in range(len(players)):
			if actions[players[i]][current_actions[players[i]]] not in d.keys():
				d[actions[players[i]][current_actions[players[i]]]] = {}
			d = d[actions[players[i]][current_actions[players[i]]]]

		for i in range(len(players)):
			if players[i] not in d.keys():
				d[players[i]] = Text(self, height = 1, width = 10)



		self.spaces.append(Label(self, text=' '))
		self.spaces[-1].grid(row=1, column=0)
		self.labels['current state'].grid(row=2, column=1)
		self.labels['current state value']['text'] = states[current_state]
		self.labels['current state value'].grid(row=2, column=2)
		if current_state > 0:
			self.buttons['state and action togglers'].append(Button(self, text="<<", command = partial(self.payoff_page_control, True, 0, True)))
			self.buttons['state and action togglers'][-1].grid(row=2, column=0)
		if current_state < len(states) - 1:
			self.buttons['state and action togglers'].append(Button(self, text=">>", command = partial(self.payoff_page_control, True, 0, False)))
			self.buttons['state and action togglers'][-1].grid(row=2, column=3)



		for i in range(len(players)):
			self.spaces.append(Label(self, text=' '))
			self.spaces[-1].grid(row=2*(i+1)+1, column = 0)
			self.labels['payoffs']['players_for_actions'].append(Label(self, text=players[i] + "'s action: "))
			self.labels['payoffs']['players_for_actions'][-1].grid(row=2*(i+1)+2, column = 1)

		for i in range(len(players)):
			self.labels['payoffs']['players_actions'].append(Label(self, text=actions[players[i]][current_actions[players[i]]]))
			self.labels['payoffs']['players_actions'][-1].grid(row=2*(i+1)+2, column = 2)


		for i in range(len(players)):
			if current_actions[players[i]] > 0:
				self.buttons['state and action togglers'].append(Button(self, text="<<", command = partial(self.payoff_page_control, False, players[i], True)))
				self.buttons['state and action togglers'][-1].grid(row=2*(i+1)+2, column=0)
			if current_actions[players[i]] < len(actions[players[i]]) - 1:
				self.buttons['state and action togglers'].append(Button(self, text=">>", command = partial(self.payoff_page_control, False, players[i], False)))
				self.buttons['state and action togglers'][-1].grid(row=2*(i+1)+2, column=3)



		offset = len(players) * 2 + 3

		self.spaces.append(Label(self, text=' '))
		self.spaces[-1].grid(row=offset, column = 0)

		self.labels['payoffs_word'].grid(row = offset + 1, column = 0)

		self.labels['payoffs']['players_for_payoffs'] = []
		for i in range(len(players)):
			self.labels['payoffs']['players_for_payoffs'].append(Label(self, text = players[i]))
			self.labels['payoffs']['players_for_payoffs'][-1].grid(row = offset + 2 + i, column = 0)


		for i in range(len(players)):
			d[players[i]].grid(row = offset + 2 + i, column = 1)





	def payoff_page_control(self, true_if_state_false_if_action, player_if_action, true_if_left_false_if_right):
		self.hide_all()
		if true_if_state_false_if_action:
			if true_if_left_false_if_right:
				self.payoff_vars['state'] = self.payoff_vars['state'] - 1
			else:
				self.payoff_vars['state'] = self.payoff_vars['state'] + 1
		else:
			if true_if_left_false_if_right:
				self.payoff_vars['actions'][player_if_action] = self.payoff_vars['actions'][player_if_action] - 1
			else:
				self.payoff_vars['actions'][player_if_action] = self.payoff_vars['actions'][player_if_action] + 1
		self.payoffs()








	def save(self):
		name = self.get_name()
		players = self.get_players()
		states = self.get_states()
		actions = self.get_actions()
		payoffs = self.get_payoff_dict(players, states, actions)
		save_NFG(NFG(players, actions, states, payoffs), name + '.nfg')


	def get_payoff_dict(self, players, states, actions):
		result = {}
		for state in states:
			result[state] = self.get_payoff_dict_for_given_state(players, state, actions)
		return result


	def get_payoff_dict_for_given_state(self, players, state, actions):
		return self.get_payoff_tree(players, state, actions, 0, {})

	def get_payoff_tree(self, players, state, actions, index, ap):
		result = {}
		if index == len(players):
			d = self.entry_fields['payoffs']
			d = d[state]
			for i in range(len(players)):
				d = d[ap[players[i]]]
			for player in players:
				user_input = d[player].get('1.0', END).strip()
				try:
					result[player] = float(user_input)
				except:
					result[player] = None
		else:
			for action in actions[players[index]]:
				ap[players[index]] = action
				result[action] = self.get_payoff_tree(players, state, actions, index + 1, ap)
				ap.pop(players[index])
		return result

###############################################################################














if __name__ == '__main__':
	game = None
	if len(sys.argv) == 1:
		run('new_game', game)
	elif len(sys.argv) == 2:
		game_name = sys.argv[1]
		try:
			game = NFG.load(game_name + '.nfg')
		except:
			print "Game file is corrupted or doesn't exist."
			exit()
		run(game_name, game)
	else:
		print "Bad usage"
