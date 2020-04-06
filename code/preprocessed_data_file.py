
import unplan

class PreprocessedDataFile:

	def set_values(self, unplans, CE_matrix, sc_actions, sc_unplans, sc_matrix):
		self.unplans = unplans
		self.CE_matrix = CE_matrix
		self.sc_actions = sc_actions
		self.sc_unplans = sc_unplans
		self.sc_matrix = sc_matrix
		

	def zip(self):
		zipped_unplans = []
		for i in range(len(self.unplans)):
			zipped_unplans.append(self.unplans[i].zip())
		zipped_sc_unplans = []
		for i in range(len(self.sc_unplans)):
			zipped_sc_unplans.append(self.sc_unplans[i].zip())
		result = [zipped_unplans, self.CE_matrix, self.sc_actions, zipped_sc_unplans, self.sc_matrix]
		return result

	def unzip(zipped_info):
		result = PreprocessedDataFile()
		zipped_unplans = zipped_info[0]
		unplans = []
		for i in range(len(zipped_unplans)):
			unplans.add(unplan.Unplan.unzip(zipped_unplans[i]))
		zipped_sc_unplans = zipped_info[3]
		sc_unplans = []
		for i in range(len(zipped_sc_unplans)):
			sc_unplans.append(unplan.Unplan.unzip(zipped_sc_unplans[i]))
		result.set_values(unplans, zipped_info[1], zipped_info[2], sc_unplans, zipped_info[4])
		return result

