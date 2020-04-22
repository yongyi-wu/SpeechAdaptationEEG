import pandas as pd
import numpy as np
import random

from scipy.stats import pearsonr
import scipy, time
import scipy.io
import scipy.stats

from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt

def join_events(eventType1, eventType2):
      ###joins two event types in two vectors of strings 
      ###to full join into the desired events
      full_events = []
      for i in eventType1:
            for j in eventType2:
                  full_events.append('/'.join([i, j]))
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
		test_stat = []
		for i in range(n_perm):
			cat = np.concatenate((np.amin(cond1, axis = 1), np.amin(cond2, axis = 1)))
			s = np.random.permutation(cat)
			stat = np.mean(s[:n]) - np.mean(s[n:])
			test_stat.append(stat)
		p_vals = 1-np.sum(obs < test_stat)/len(test_stat)

	if statistic == 'mean':
		##testing whether the mean amplitude is different between conditions
		# obs = np.amin(np.mean(cond1, axis = 0)) - np.amin(np.mean(cond2, axis = 0))
		# for i in range(n_perm):
		# 	cat = np.concatenate((cond1, cond2), axis = 0)
		# 	idx = np.arange(n*2)
		# 	s = np.random.permutation(idx)
		# 	stat = np.amin(np.mean(cat[s[:n], :], axis = 0)) - np.amin(np.mean(cat[s[n:], :], axis = 0))
		# 	test_stat.append(stat)
		# p_vals = 1-np.sum(obs < test_stat)/len(test_stat)
		obs = np.mean(np.mean(cond1, axis = 1) - np.mean(cond2, axis = 1))
		test_stat = []
		for i in range(n_perm):
			cat = np.concatenate((np.mean(cond1, axis = 1), np.mean(cond2, axis = 1)))
			s = np.random.permutation(cat)
			stat = np.mean(s[:n]) - np.mean(s[n:])
			test_stat.append(stat)
		p_vals = 1-np.sum(obs < test_stat)/len(test_stat)

	elif statistic == 'difference':
		###Note that for difference and cor statistic, the obs and test-stats are only returned
		###for the last iteration so they are not for every time point
		for t in range(p):
			test_stat = []
			obs = np.mean(cond1[:, t])-np.mean(cond2[:, t])
			for i in range(n_perm):
				s = np.random.permutation(np.concatenate((cond1[:, t], cond2[:, t])))
				stat = np.mean(s[:n]) - np.mean(s[n:])				
				test_stat.append(stat)
			p_val = 1-np.sum(obs < test_stat)/len(test_stat)
			p_vals.append(p_val)

	elif statistic == 'cor': ##not tested yet
		for t in range(p):
			test_stat = []
			obs = pearsonr(cond1[:, t], cond2[:, t])[0]
			for i in range(n_perm):
				s = np.random.permutation(np.concatenate((cond1[:, t], cond2[:, t])))
				stat = pearsonr(s[:n], s[n:])[0] ##not tested yet
				test_stat.append(stat)

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


def cor_mat(e1, e2):
	### assuming both e1 and e2 are n * t matrices where n = subject n
	### t = time points of EEG data
	t1 = np.shape(e1)[1]
	t2 = np.shape(e2)[1]
	matrix = np.empty([t1, t2])
	p_vals = np.empty([t1, t2])

	for i in reversed(range(t1)):
		for j in range(t2):
			matrix[i, j], p_vals[i, j] = pearsonr(e1[:, i], e2[:, j])
	return matrix, p_vals

def FDR_2D(p_vals):
	d = np.shape(p_vals)[0]
	p = p_vals.flatten()
	p_rej, p_adj, p1, p2 = multipletests(p)
	p_rej = np.reshape(p_rej, (d, d))
	p_adj = np.reshape(p_adj, (d, d))
	return p_rej, p_adj


def mean_confidence_interval(data, confidence=0.95):
    ###assuming the input is an np array
    n = len(data)
    m, se = np.mean(data, axis = 0), scipy.stats.sem(data)
    #h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-se, m+se##change this to h if you want CIs.


def plot_mean_and_CI(mean, lb, ub, color_mean=None, color_shading=None):
    # plot the shaded range of the confidence intervals
    x = np.subtract(range(mean.shape[0]), 200)
    plt.fill_between(np.subtract(range(mean.shape[0]), 200), ub, lb,
                     color=color_shading, alpha=.5)
    # plot the mean on top
    plt.plot(x, mean, color_mean)


