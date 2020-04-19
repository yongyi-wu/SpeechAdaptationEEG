###This file will save all epoched data as well as 
###evoked data for the events of interest
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

times = raw.times
#np.arange(-0.203125,0.5,0.0078125)
T_obs, clusters, cluster_p_values, H0 = \
    permutation_cluster_test([diff_can, diff_rev], n_permutations=5,
                             tail=1, n_jobs=1)
channel = 'FC_cluster'

#plt.subplot(212)
    # else:
    #     plt.axvspan(times[c.start], times[c.stop - 1], color=(0.3, 0.3, 0.3),
    #                 alpha=0.3)
#hf = 
#plt.subplot(211)
plt.title('Channel : Fronto_central_cluster')
plt.plot(times, diff_can.mean(axis=0), color = 'Crimson')
plt.plot(times, diff_rev.mean(axis=0), color = 'CornFlowerBlue')
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] <= 0.05:
        h = plt.axvspan(times[c.start], times[c.stop - 1],
                        color='r', alpha=0.3)
plt.legend(['Canonical_Difference_wave', 'Reverse_Difference_wave', 'cluster p-value < 0.05'], loc = 'upper left')

         #label="Difference wave contrast")
plt.ylabel("Difference waves amplitudes (uV)")
plt.xlabel("time (s)")
plt.yticks(np.arange(-1e-06,1.25e-06,25e-08), np.arange(-1,1.25,0.25))
figname = fig_diffcluster + 'Cluster_Diff.png'
print(figname)
#plt.savefig(figname)
plt.show()
plt.close('all')
    

