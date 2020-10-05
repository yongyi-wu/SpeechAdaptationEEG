################################################################################################
################################################################################################
################################################################################################
################################################################################################

### This analysis explores the correlation between the amplitude and CLASSIFICATION ACCURACY between the 
### reverse block exposure stimuli and the reverse test stimuli. Specifically, the correlation was performed by 
### time point and all the correlation coefficients are corrected using FDR. 

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
parietal_cluster = config.parietal_cluster

include = config.include

drop_names = config.drop_names
###################################################################
################################ events ###########################
###################################################################
Block = config.Block
event_id = config.event_id
Test = config.Test
Exposure = config.Exposure
    
### we will start with a cluster-based permutation test on the average of the fronto-central electrodes
### we will only do this analysis on the MMN data
event_test = helper.join_events(Block, Test)
event_exposure = helper.join_events(Block, Exposure)
event = event_test + event_exposure
print(event)
grand_ave = np.empty((0,8,129))
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    raw_fname = epoch_dir + "%s_epoch_M.fif" %(subj)
    ###read from saved epoched data
    raw = mne.read_epochs(raw_fname, proj = False, preload = True)

    chan_idx = [raw[event[0]].ch_names.index(ch) for ch in parietal_cluster]

    epoch = []
    for j in range(len(event)):
        epoch.append(raw[event[j]].average().data)

    ave = helper.get_mean_evoked(chan_idx, epoch)
    grand_ave = np.append(grand_ave, [ave], axis = 0)

## 26- take the time window from 0-800ms suggested in Moberly et al
times = raw.times
start = 26
end = 71
rev_test2 = grand_ave[:,2,start:]
rev_test1 = grand_ave[:,3,start:]
rev_exp_P = grand_ave[:,6,start:]
rev_exp_B = grand_ave[:,7,start:]

rev_test_diff = np.subtract(rev_test2, rev_test1)

rev_exp = np.mean(grand_ave[:,6:8,start:], axis = 1)
# np.subtract(rev_exp_P, rev_exp_B)
# np.mean(grand_ave[:,6:8,start:], axis = 1)
# rev_exp_P 
#np.subtract(rev_exp_P, rev_exp_B)
cor_mat, p_vals = helper.cor_mat(rev_test_diff, rev_exp)
# cor_mat, p_vals = helper.cor_mat(rev_test_diff, rev_exp)

fig, ax = plt.subplots()
im = ax.imshow(cor_mat, interpolation='lanczos', origin='lower', cmap='RdBu_r',
                extent=raw.times[[26, -1, 26, -1]], vmin=-1, vmax=1)

# fig, ax = plt.subplots()
# im = ax.imshow(p_adj[1], interpolation='lanczos', origin='lower', cmap='RdBu_r',
#                 extent=raw.times[[26, -1, 26, -1]], vmin=0, vmax=0.1)

ax.set_xlabel('Test (s)')
ax.set_ylabel('Exposure (s)')
ax.set_title('Correlation Map')
ax.axvline(0, color='k')
ax.axhline(0, color='k')
plt.colorbar(im, ax=ax)
plt.show()

p_rej, p_adj = helper.FDR_2D(p_vals)



