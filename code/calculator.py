
import utils

class Calculator:

	def __init__(self, game):
		self.game = game
		self.calculated_values = {}
		self.calculated_values['LP data'] = utils.prepare_LP_data(game)
	

	def get_self_contained_support(self):
		return 


	def get_unequilibrium_vertices(self):
		return None



	def get_self_contained_unequilibrium_vertices(self):
		return None
