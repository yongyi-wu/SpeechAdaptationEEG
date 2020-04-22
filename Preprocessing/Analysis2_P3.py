################################################################################################
################################################################################################
################################################################################################
################################################################################################

### This analysis explores the time windows for the down-weighting effect as suggested by 
### Toscano & Mcmurray, 2010: P3, 300m-800m seems sensitive to the category distinctions, which
### is useful in this context because of the behavioral down-weighting we observe in previous DBSL
### studies. An additional exploratory analysis of the N1 window was also done. 

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
    
### we will start with a cluster-based permutation test on the average of the fronto-central electrodes
### we will only do this analysis on the MMN data

grand_ave = np.empty((0,4,129))
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    raw_fname = epoch_dir + "%s_epoch_M.fif" %(subj)
    ###read from saved epoched data
    raw = mne.read_epochs(raw_fname, proj = False, preload = True)
    event = helper.join_events(Block, Test)
    chan_idx = [raw[event[0]].ch_names.index(ch) for ch in parietal_cluster]
    epoch = []
    for i in range(len(event)):
        epoch.append(raw[event[i]].average().data)
    ave = helper.get_mean_evoked(chan_idx, epoch)
    grand_ave = np.append(grand_ave, [ave], axis = 0)

##64:129 take the time window from 300-800ms suggested in Toscano & Mcmurray, 2010
start = 64
end = 129
can_test2 = grand_ave[:,0,start:end]
can_test1 = grand_ave[:, 1, start:end]
rev_test2 = grand_ave[:,2,start:end]
rev_test1 = grand_ave[:,3,start:end]

can_diff = np.subtract(can_test2, can_test1)
rev_diff = np.subtract(rev_test2, rev_test1)

p_val, obs, test_stat = helper.permutation_test([can_diff, rev_diff], statistic = 'mean')
print(p_val) 
## with p = 0.008

####Look at 75-127ms for N1 responses
start = 35
end = 42
can_N_test2 = grand_ave[:,0,start:end]
can_N_test1 = grand_ave[:, 1, start:end]
rev_N_test2 = grand_ave[:,2,start:end]
rev_N_test1 = grand_ave[:,3,start:end]

can_diff = np.subtract(can_N_test2, can_N_test1)
rev_diff = np.subtract(rev_N_test2, rev_N_test1)

p_val, obs, test_stat = helper.permutation_test([can_diff, rev_diff], statistic = 'mean')


