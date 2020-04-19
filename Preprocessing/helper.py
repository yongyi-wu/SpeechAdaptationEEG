import pandas as pd
import numpy as np
import random
from scipy.stats import pearsonr

def join_events(eventType1, eventType2):
      ###joins two event types in two vectors of strings 
      ###to full join into the desired events
      full_events = []
      for i in range(len(eventType1)):
            for j in range(len(eventType2)):
                  full_events.append('/'.join([eventType1[i], eventType2[j]]))
      return full_events


def pick_event_type(eventType1, eventType2, e1color = 'Crimson', e2color = 'CornFlowerBlue', e1ltyp = '-', e2ltyp = '--'):
	###Assuming eventType1 is always the block i.e., canonical and reverse
	###eventype 1 will always differ in color and eventtype2 in linestyle
	###default colors are set
	###linestyle is fixed
	event_list = join_events(eventType1, eventType2)
	color = {eventType1[0]:e1color, eventType1[1]:e2color}
	linestyles = {eventType2[0]:e1ltyp, eventType2[1]:e2ltyp}

	return event_list, color, linestyles

###calculate the evoked for events and electrodes of interest
def get_mean_diffwave(picks, epoch):
	result = []
	for idx in range(1,4,2):
		standard = epoch[idx-1]
		deviant = epoch[idx]	
		diff = np.subtract(deviant[picks,:], standard[picks,:])
		result.append(np.mean(diff, axis = 0))
	return result[0], result[1]

###get evoked averaged across electrodes. 
def get_mean_evoked(picks, epoch):
	result = []
	for idx in range(np.shape(epoch)[0]):
		e = epoch[idx]	
		result.append(np.mean(e[picks,:], axis = 0))
	return result



def permutation_test(data, statistic = 'difference', n_perm = 10000):
	##data should come in the shape of [cond1, cond2]
	##assuming np.shape(cond1) = np.shape(cond2) = [n, t]
	##the 'difference' statistic always calculates the difference of cond1-cond2 and 
	##performs a one-tailed test
	##finally the function returns a p-values 
	##Currently there are 3 test statistics: 
	##difference: mean difference between conditions
	##min: mean peak amplitude difference between conditions given a time window (this is NOT done by time points and returns only 1
	##single statistic)
	##cor: correlation between two samples
	cond1 = data[0]
	cond2 = data[1]
	n = np.shape(cond1)[0]
	p = np.shape(cond1)[1]
	p_vals = []
	test_stat = []


	if statistic == 'min':
		##testing whether the mean peak amplitude is different between conditions
		# obs = np.amin(np.mean(cond1, axis = 0)) - np.amin(np.mean(cond2, axis = 0))
		# for i in range(n_perm):
		# 	cat = np.concatenate((cond1, cond2), axis = 0)
		# 	idx = np.arange(n*2)
		# 	s = np.random.permutation(idx)
		# 	stat = np.amin(np.mean(cat[s[:n], :], axis = 0)) - np.amin(np.mean(cat[s[n:], :], axis = 0))
		# 	test_stat.append(stat)
		# p_vals = 1-np.sum(obs < test_stat)/len(test_stat)
		obs = np.mean(np.amin(cond1, axis = 1)) - np.mean(np.amin(cond2, axis = 1))
		for i in range(n_perm):
			cat = np.concatenate((np.amin(cond1, axis = 1), np.amin(cond2, axis = 1)))
			s = np.random.permutation(cat)
			stat = np.mean(s[:n]) - np.mean(s[n:])
			test_stat.append(stat)
		p_vals = 1-np.sum(obs < test_stat)/len(test_stat)

	elif statistic == 'difference':
		for t in range(p):
			for i in range(n_perm):
				s = np.random.permutation(np.concatenate((cond1[:, t], cond2[:, t])))
				stat = np.mean(s[:n]) - np.mean(s[n:])				
				test_stat.append(stat)
			obs = np.mean(cond1[:, t])-np.mean(cond2[:, t])
			p_val = 1-np.sum(obs < test_stat)/len(test_stat)
			p_vals.append(p_val)

	elif statistic == 'cor': ##not tested yet
		for t in range(p):
			for i in range(n_perm):
				s = np.random.permutation(np.concatenate((cond1[:, t], cond2[:, t])))
				stat = pearsonr(s[:n], s[n:])[0] ##not tested yet
				test_stat.append(stat)

			obs = pearsonr(cond1[:, t], cond2[:, t])[0]
			p_val = 1-np.sum(obs > test_stat)/len(test_stat)
			p_vals.append(p_val)

	else:
		raise Exception('Test statistic not yet available')

	return p_vals, obs, test_stat

def get_clusters(adjusted_p_vals):
	size = np.shape(adjusted_p_vals)[0]
	name = []
	c = []
	idx = 0
	for i in range(size):
		if adjusted_p_vals[i] == 0:
			name.append('No')
		elif adjusted_p_vals[i] > 0.05:
			name.append('Nonsig')
		else:
			name.append('Sig')

		if name[i] != 'No':
			if name[i] == name[i-1]:
				c.append(idx)
			elif name[i] != name[i-1]:
				idx = idx + 1
				c.append(idx)
		else:
			c.append(0)

	return name, np.array(c)



