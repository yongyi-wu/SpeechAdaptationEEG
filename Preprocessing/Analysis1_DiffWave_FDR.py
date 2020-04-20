################################################################################################
################################################################################################
################################################################################################
################################################################################################

### This analysis is an extension of the cluster-based permutation analysis, aimed at finding the 
### specific time points where the canonical/reverse difference amplitudes differ.
### It uses an FDR correction to test all time points in the 200-300 time window suggested by Moberly et al (2014)
### to show divergence in the difference amplitude. 
### The result shows difference in both 201-240ms and 260-300ms (corresponding to the early AND late time windows)
### in Moberly et al (2014)

################################################################################################
################################################################################################
################################################################################################
################################################################################################
import mne
import numpy as np
import matplotlib.pyplot as plt

import scipy, time
import scipy.io
import scipy.stats
import pandas as pd

from mne import io
from mne.stats import permutation_cluster_test
from mne.datasets import sample
from statsmodels.stats.multitest import multipletests

###import config and helper files
import config
import helper

tmp_rootdir  = config.tmp_rootdir
raw_dir = config.raw_dir
resampled_dir = config.resampled_dir
filtered_dir = config.filtered_dir
ica_dir = config.ica_dir
epoch_dir = config.epoch_dir

##fig dirs
fig_diffcluster = config.fig_cluster

###################################################################
######################### subject #################################
###################################################################
#============================================
#subject lists, in canonical-reverse order, reverse-canonical order or full list

subj_list = config.subj_list
n_subj = len(subj_list) 

###################################################################
########################## eeg channel list #######################
###################################################################
eeg_chan = config.eeg_chan
EOG_list = config.EOG_list
FC_cluster = config.FC_cluster

include = config.include

drop_names = config.drop_names
###################################################################
################################ events ###########################
###################################################################
Block = config.Block
event_id = config.event_id
MMN = config.MMN
    
### we will start with a cluster-based permutation test on the average of the fronto-central electrodes
### we will only do this analysis on the MMN data

diff_can = []
diff_rev = []
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    raw_fname = epoch_dir + "%s_epoch.fif" %(subj)
    ###read from saved evoked data
    raw = mne.read_epochs(raw_fname, proj = False, preload = True)
    event = helper.join_events(Block, MMN)
    chan_idx = [raw[event[0]].ch_names.index(ch) for ch in FC_cluster]
    epoch = []
    for i in range(len(event)):
        epoch.append(raw[event[i]].average().data)
    can_ave, rev_ave = helper.get_mean_diffwave(chan_idx, epoch)
    diff_can.append(can_ave)
    diff_rev.append(rev_ave)

diff_can = np.array(diff_can)
diff_rev = np.array(diff_rev)

p_vals, obs, test_stat = helper.permutation_test([diff_can, diff_rev])
# p_adj = multipletests(, alpha = 0.05, method = 'fdr_bh') 
#p_adj = multipletests(p_vals[50:77], alpha = 0.05, method = 'fdr_bh')

times = raw.times
print(times[52], times[64])

window = np.arange(52, 64) #52:64, 200-300
p_final = np.zeros(np.shape(p_vals))
p_adj = multipletests(p_vals[window], alpha = 0.05, method = 'fdr_bh')
##corresponds to 200 to 300ms

p_final[window] = p_adj[1]

table, plot_p = helper.get_clusters(p_final)

#np.arange(-0.203125,0.5,0.0078125)

channel = 'FC_cluster'

plt.title('Channel : Fronto_central_cluster')
plt.plot(times, diff_can.mean(axis=0), color = 'Crimson')
plt.plot(times, diff_rev.mean(axis=0), color = 'CornFlowerBlue')


for idx in range(len(np.unique(plot_p))):
    cluster = np.where(plot_p == idx)[0]
    print(cluster)
    
    if idx > 0 and table[cluster[0]] == 'Sig':
        h = plt.axvspan(times[cluster[0]], times[cluster[-1]+1],
                        color='r', alpha=0.3)
    elif idx > 0 and table[cluster[0]] == 'Nonsig':
        h = plt.axvspan(times[cluster[0]], times[cluster[-1]+1],
                                color=(0.3, 0.3, 0.3), alpha=0.3)




# h = plt.axvspan(times[59], times[64],
#                         color='r', alpha=0.3)
        
plt.legend(['Canonical_Difference_wave', 'Reverse_Difference_wave', 'FDR p-value < 0.05', 'nonsignificant'], loc = 'upper left')

          #label="Difference wave contrast")
plt.ylabel("Difference waves amplitudes (uV)")
plt.xlabel("time (s)")
plt.yticks(np.arange(-1e-06,1.25e-06,25e-08), np.arange(-1,1.25,0.25))
figname = fig_diffcluster + 'FDR_diff_200_300.png'
print(figname)
plt.savefig(figname)
plt.show()
plt.close('all')
    

