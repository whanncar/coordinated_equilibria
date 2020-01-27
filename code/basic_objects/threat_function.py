
import utils

class ThreatFunction:

	def __init__(self, game):
		# Attach game to object
		self.game = game
		# Make copy of player list
		players_copy = []
		for i in range(len(game.players)):
			players_copy.append(game.players[i])
		# Make skeleton to hold data
		self.data = {}
		for i in range(len(game.states)):
			self.data[game.states[i]] = self.make_skeleton([], players_copy)
		# Populate data with actual values
		self.populate_data()


	def populate_data(self):
		# Make permutations
		players_copy = []
		for i in range(len(self.game.players)):
			players_copy.append(self.game.players[i])
		perms = utils.get_all_permutations(players_copy)
		# Make action profiles
		actions = []
		for i in range(len(self.game.players)):
			actions.append([])
			actions_for_i = self.game.actions[self.game.players[i]]
			for j in range(len(actions_for_i)):
				actions[-1].append(actions_for_i[j])
		aps = utils.get_list_product(actions)
		# For each state
		for state in self.game.states:
			# For each permutation
			for pi in perms:
				# For each action profile
				for list_ap in aps:
					ap = {}
					for i in range(len(self.game.players)):
						ap[self.game.players[i]] = list_ap[i]
					# Get payoffs
					payoff = self.game.get_payoffs(ap, state)
					# For each prefix
					for i in range(len(pi)):
						entry = self.data[state]
						for j in range(i+1):
							entry = entry[0][pi[j]]
						entry = entry[1]
						for j in range(i):
							entry = entry[ap[pi[j]]]
						# If payoff to last guy is smaller than current value OR current value is None
						if (entry[ap[pi[i]]] is None) or (payoff[pi[i]] < entry[ap[pi[i]]]):
							# Store as new value
							entry[ap[pi[i]]] = payoff[pi[i]]


	def make_skeleton(self, previous_players, remaining_players):
		# Set up subtree for remaining players
		next_player = {}
		old_remaining_players = []
		# Fill in skeleton for each choice of next player to move
		while(len(remaining_players) > 0):
			# Temporarily modify player lists to build subtree
			chosen_player = remaining_players.pop(0)
			old_remaining_players.append(chosen_player)
			previous_players.append(chosen_player)
			# Build subtree
			next_player[chosen_player] = self.make_skeleton(previous_players, remaining_players)
			# Fix previous and remaining players
			previous_players.pop(-1)
		# Set up dictionary for organizing action profiles
		min_data = self.build_pre_min_data_structure(previous_players)
		# Package everything and return
		result = [next_player, min_data]
		return result



	def build_pre_min_data_structure(self, actors):
		# Handle stupid case
		if len(actors) == 0:
			return {}
		# Handle base case
		if len(actors) == 1:
			result = {}
			for a in self.game.actions[actors[0]]:
				result[a] = None
			return result
		# Deal with the rest
		current_actor = actors.pop(0)
		result = {}
		for a in self.game.actions[current_actor]:
			result[a] = self.build_pre_min_data_structure(actors)
		actors.insert(0, current_actor)
		return result


