
import NFG
import threat_function



def test():
	states = ['a', 'b']
	players = ['row', 'col']
	actions = {}
	actions['row'] = ['C', 'D']
	actions['col'] = ['E', 'F']
	payoffs = {}
	payoffs['a'] = {}
	payoffs['b'] = {}
	payoffs['a']['C'] = {}
	payoffs['a']['D'] = {}
	payoffs['b']['C'] = {}
	payoffs['b']['D'] = {}
	payoffs['a']['C']['E'] = {}
	payoffs['a']['C']['E']['row'] = 1
	payoffs['a']['C']['E']['col'] = 2
	payoffs['a']['C']['F'] = {}
	payoffs['a']['C']['F']['row'] = 3
	payoffs['a']['C']['F']['col'] = 4
	payoffs['a']['D']['E'] = {}
	payoffs['a']['D']['E']['row'] = 5
	payoffs['a']['D']['E']['col'] = 6
	payoffs['a']['D']['F'] = {}
	payoffs['a']['D']['F']['row'] = 7
	payoffs['a']['D']['F']['col'] = 8
	payoffs['b']['C']['E'] = {}
	payoffs['b']['C']['E']['row'] = 9
	payoffs['b']['C']['E']['col'] = 10
	payoffs['b']['C']['F'] = {}
	payoffs['b']['C']['F']['row'] = 11
	payoffs['b']['C']['F']['col'] = 12
	payoffs['b']['D']['E'] = {}
	payoffs['b']['D']['E']['row'] = 13
	payoffs['b']['D']['E']['col'] = 14
	payoffs['b']['D']['F'] = {}
	payoffs['b']['D']['F']['row'] = 15
	payoffs['b']['D']['F']['col'] = 16
	game = NFG.NFG(players, actions, states, payoffs)
	tf = threat_function.ThreatFunction(game)
	return tf
