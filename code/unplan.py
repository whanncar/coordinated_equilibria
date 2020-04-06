
import copy



class Unplan:


  # public

	def __init__(self, pi, ap, state):
		self.pi = pi
		self.ap = ap
		self.state = state
		self.ltf = None


	def populate_local_threat_function(self, game, tf):
		# Instantiate ltf
		self.ltf = {}
		# Retrieve game data
		players = game.players
		actions = game.actions
		# Retrieve state
		state = self.state
		# Make ltf skeleton
		for p in players:
			self.ltf[p] = {}
			for a in actions[p]:
				self.ltf[p][a] = 0
		# Calculate obedient payoffs
		obedient_payoffs = game.get_payoffs(self.ap, state)
		# Populate ltf values
		predecessors = []
		ap_copy = copy.deepcopy(self.ap)
		for i in range(len(self.pi)):
			p = self.pi[i]
			true_action = self.ap[p]
			for a in actions[p]:
				if a == true_action:
					self.ltf[p][a] = obedient_payoffs[p]
				else:
					ap_copy[p] = a
					self.ltf[p][a] = tf.get_entry(predecessors, p, ap_copy, state)
			ap_copy[p] = true_action
			predecessors.append(p)


	def get_LP_column(self, game):
		# Instantiate empty vector
		column = []
		# Retrieve players, actions, and local threat function
		players = game.players
		actions = game.actions
		ltf = self.ltf
		# Calculate column entries
		# For each player
		for i in range(len(players)):
			p = players[i]
			actions_for_p = actions[p]
			# For each recommended action
			for j in range(len(actions_for_p)):
				a = actions_for_p[j]
				# If a is not the recommended action for p
				if a != self.ap[p]:
					# Set entry to 0 for each deviating action
					for k in range(len(actions_for_p)):
						column.append(0)
				# If a is the recommended action for p
				else:
					# Retrieve obedient payoff for p
					obedient_payoff_for_p = self.ltf[p][a]
					# For each deviating action
					for k in range(len(actions_for_p)):
						# If this is the recommended action, set entry to 0
						if k == j:
							column.append(0)
						# If this is not the recommended action, set entry to difference in payoffs
						else:
							b = actions_for_p[k]
							column.append(obedient_payoff_for_p - self.ltf[p][b])
			# Return column
			return column





	def __str__(self):
		result = self.state + " |"
		for i in range(len(self.pi)):
			player = self.pi[i]
			action = self.ap[player]
			result = result + " (" + player + ", " + action + ")"
		return result


	def zip(self):
		result = []
		result.append(self.pi)
		result.append(self.ap)
		result.append(self.state)
		result.append(self.ltf)
		return result


	def unzip(zipped_info):
		pi = zipped_info[0]
		ap = zipped_info[1]
		state = zipped_info[2]
		ltf = zipped_info[3]
		result = Unplan(pi, ap, state)
		result.ltf = ltf
		return result



