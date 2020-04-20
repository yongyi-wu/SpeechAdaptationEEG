################################################################################################
################################################################################################
################################################################################################
################################################################################################

### This analysis is a first step, confirmatory analysis to check the existent of an MMN effect at least
### in the canonical block (test stimuli differing along the secondary dimension). It finds the mean peak amplitudes
### in the time window 150-350ms after stimulus onset in the canonical_standard and canonical_deviant conditions 
### and then permute each individual's peak amplitude to generate the null distribution. 
### Finally, it compares the observed statistic with the null distribution and make an inferential statement about 
### whether the observed difference is significantly different than 0 or not. 
### The result show a marginal significance between the mean peak amplitude of standard and deviant trials in the canonical
### block 

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

grand_ave = np.empty((0,4,91))
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    raw_fname = epoch_dir + "%s_epoch.fif" %(subj)
    ###read from saved epoched data
    raw = mne.read_epochs(raw_fname, proj = False, preload = True)
    event = helper.join_events(Block, MMN)
    chan_idx = [raw[event[0]].ch_names.index(ch) for ch in FC_cluster]
    epoch = []
    for i in range(len(event)):
        epoch.append(raw[event[i]].average().data)
    ave = helper.get_mean_evoked(chan_idx, epoch)
    grand_ave = np.append(grand_ave, [ave], axis = 0)

##45:71 take the time window from 150-350ms suggested in Moberly et al
start = 45
end = 71
can_stand = grand_ave[:,0,start:end]
can_dev = grand_ave[:, 1, start:end]
rev_stand = grand_ave[:,2,start:end]
rev_dev = grand_ave[:,3,start:end]

p_val, obs, test_stat = np.array(helper.permutation_test([can_dev, can_stand], statistic = 'min'))
print(p_val) 
## calculate the mean peak amplitude first and find a marginal difference between can and rev peak amplitudes
###p = 0.059. Note that the pvals are stochastic and I didn't fix a random state here so it will be slight different every time I run it. 


