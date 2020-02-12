"""
Created on Mon Dec.9, 2019
ICA Step (2)
We need to inspect the independent components and decide which are bad.
# ===================
Dec. 9, 2019, All subjects except 6,7,10 were preprocessed with ICA. 
# ===================

@author: Charles Wu
"""
import mne
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mne.preprocessing import ICA
import scipy.io
import scipy.stats
import time

tmp_rootdir = '/Users/charleswu/Desktop/MMN/'
raw_dir = tmp_rootdir + "raw_data/"
resampled_dir = tmp_rootdir + 'resampled_data/'
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 

fig_dir = tmp_rootdir + "ica_fig/"
epoch_dir = tmp_rootdir + "epoch_data/"

subj_list = ['001', '002', '003', '004', '005', '008', '009', '011', '012']
n_subj = len(subj_list) 
event_id = {'standard/can':65321,
            'deviant/can':65322,
            'standard/rev':65341,
            'deviant/rev':65342,
            'CanExpSet':65391,
            'CanExpSat':65392,
            'CanTest1':65401,
            'CanTest2':65402,
            'RevExpSet':65491,
            'RevExpSat':65492,
            'RevTest1':65501,
            'RevTest2':65502
            }
eeg_chan = []
eeg_chan = eeg_chan + ['A' + str(i+1) for i in range(32)]
chnames = eeg_chan + ['EXG' + str(i+1) for i in range(5)]
biosemi_layout = mne.channels.read_montage(tmp_rootdir + 'biosemi_cap_32_M_2_EOG_3.locs')
biosemi_layout.ch_names = chnames
alpha = 10

for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    # ============= load ICA =========================================================
    ica_raw_name = ica_dir  + "%s_after_ica_raw.fif" %(subj)
    raw = mne.io.Raw(ica_raw_name, preload = True)
    raw.set_montage(biosemi_layout)
    events = mne.find_events(raw)

    tmin, tmax = -0.6, 0.6
    baseline = (-0.2, 0.0)
    ##the baseline period is set to equal to the length of the epoch. The epoch is set to be longer
    ##than usual because of the potential time-frequency analysis that comes later. 
    epochs = mne.Epochs(raw, events=events, baseline = baseline, event_id=event_id, tmin=tmin,
                        tmax=tmax)
    ##In this step, we will also reject the bad trials that have 3 standard deviations
    ##from the average
    picks = np.arange(32)
    epoch_mat = epochs.get_data()[:,picks,:]
    ##epoch_mat is 3-D where 0 is n_events, 1 is n_channels and 2 is n_time points
    #The following code rejects epochs that are alpha std beyong the average. Serves as an 
    #Automatic trial rejection step
    ranges_each_trial = np.max(epoch_mat, axis = 2) - np.min(epoch_mat, axis = 2)
    ranges_zscore = scipy.stats.zscore(ranges_each_trial, axis = 0)
    bad_trials = np.any(ranges_zscore > alpha, axis = 1)
    print("# bad_trials %d" %bad_trials.sum())
    epochs.drop(np.where(bad_trials == 1)[0])
    epoch_fname = epoch_dir + "%s_epoch.fif" %(subj)
    epochs.save(epoch_fname)

