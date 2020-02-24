
import utils

class Calculator:

	def __init__(self, game):
		self.game = game
		self.calculated_values = {}
		# Get full LP matrix
		self.calculated_values['LP data'] = utils.prepare_LP_data(game)
		# Get self contained support and LP matrix
		self_contained_stuff = utils.prepare_self_contained_LP_data(self.game)
		self.calculated_values['self contained support'] = self_contained_stuff['actions']
		self.calculated_values['self contained LP data'] = self_contained_stuff['LP']


	def get_unplans(self):
		result = []
		unplans = self.calculated_values['LP data'][0]
		for i in range(len(unplans)):
			result.append(str(unplans[i]))
		return result


	def get_self_contained_unplans(self):
		result = []
		unplans = self.calculated_values['self contained LP data'][0]
		for i in range(len(unplans)):
			result.append(str(unplans[i]))
		return result


	def get_self_contained_support(self):
		return self.calculated_values['self contained support']




	def get_unequilibrium_vertices(self):
		if 'unequilibrium vertices' not in self.calculated_values.keys():
			self.calculated_values['unequilibrium vertices'] = utils.get_vertices(self.calculated_values['LP data'][1])
		return self.calculated_values['unequilibrium vertices']



	def get_self_contained_unequilibrium_vertices(self):
		if 'self contained vertices' not in self.calculated_values.keys():
			self.calculated_values['self contained vertices'] = utils.get_vertices(self.calculated_values['self contained LP data'][1])
		return self.calculated_values['self contained vertices']
