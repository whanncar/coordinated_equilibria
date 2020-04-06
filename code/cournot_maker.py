

import NFG, file_io, sys

def make_cournot(num):
	players = ['one', 'two']
	states = ['unique']
	actions = {}
	actions['one'] = []
	actions['two'] = []
	for i in range(num+1):
		actions['one'].append(str(i))
		actions['two'].append(str(i))
	payoffs = {}
	payoffs['unique'] = {}
	for i in range(num+1):
		payoffs['unique'][str(i)] = {}
		for j in range(num+1):
			payoffs['unique'][str(i)][str(j)] = {}
			price = 1 - (float(i) + float(j))/num
			if price < 0:
				price = 0
			payoffs['unique'][str(i)][str(j)]['one'] = price * float(i) / num
			payoffs['unique'][str(i)][str(j)]['two'] = price * float(j) / num
	game = NFG.NFG(players, actions, states, payoffs)
	return game


if __name__ == '__main__':
	num = int(sys.argv[-1])
	filename = 'cournot_' + str(num) + '.nfg'
	file_io.save_NFG(make_cournot(num), filename)
