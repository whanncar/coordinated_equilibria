



class Unplan:

	def __init__(self, tf, pi, ap, state):
		self.tf = tf
		self.pi = pi
		self.ap = ap
		self.state = state


	def prepare_threat_function_values(self):
		baby_threat_function = {}
		prefix = []
		# For each prefix of pi
		for i in range(len(self.pi)):
			# Get the actions for players that go before current player
			baby_ap = {}
			for early_player in prefix:
				baby_ap[early_player] = self.ap[early_player]
			# Grab current player and current player's actions
			current_player = self.pi[i]
			actions = self.tf.game.actions[current_player]
			# For each action that current player could deviate to, store threat value
			baby_threat_function[current_player] = {}
			for j in range(len(actions)):
				b = actions[j]
				baby_ap[current_player] = b
				baby_threat_function[current_player][b] = self.tf.get_entry(prefix, current_player, baby_ap, self.state)
			# Add current player to prefix
			prefix.append(current_player)
		return baby_threat_function





	def get_LP_column(self):
		result = []
		players = self.tf.game.players
		# Compute obedience payoffs
		payoffs = self.tf.game.get_payoffs(self.ap, self.state)
		# Compute relevant threat function values:
		baby_tf = self.prepare_threat_function_values()
		# For each player
		for i in range(len(players)):
			p = players[i]
			actions = self.tf.game.actions[p]
			# For each recommended action for this player
			for j in range(len(actions)):
				a = actions[j]
				# For each action that this player can deviate to
				for k in range(len(actions)):
					b = actions[k]
					# If this is not recommended action or recommended action is same as defiant action
					if (a != self.ap[p]) or (a == b):
						# Set value to 0
						result.append(0)
					# Otherwise
					else:
						# Store benefit from obedience
						payoffs[p] - baby_tf[p][b]
		return result





