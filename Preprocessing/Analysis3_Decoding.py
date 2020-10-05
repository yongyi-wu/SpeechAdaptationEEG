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

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

import mne
from mne.datasets import sample
from mne.decoding import (SlidingEstimator, GeneralizingEstimator,
                          cross_val_multiscore, LinearModel, get_coef)
###import config and helper files
import config
import helper

tmp_rootdir  = config.tmp_rootdir + 'SpeechAdaptationEEG/'
raw_dir = config.raw_dir
resampled_dir = config.resampled_dir
filtered_dir = config.filtered_dir
ica_dir = config.ica_dir
epoch_dir = config.epoch_dir

##fig dirs
fig_decoding_ave = config.fig_decoding_ave
fig_decoding_indiv = config.fig_decoding_indiv
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

for j in Block:
    print(j)
    classify_scores = np.empty((0,129))
    for i in range(n_subj):
        subj = subj_list[i]
        print(subj)
        raw_fname = epoch_dir + "%s_epoch_M.fif" %(subj)
        ###read from saved epoched data
        raw = mne.read_epochs(raw_fname, proj = False, preload = True)
        event_test = helper.join_events([j], Test)
        print(event_test)
        chan_idx = [raw[event_test[0]].ch_names.index(ch) for ch in parietal_cluster]

        test2 = raw[event_test[0]].get_data()[:,chan_idx,:]
        test1 = raw[event_test[1]].get_data()[:,chan_idx,:]
        t2, t1 = np.shape(test2)[0], np.shape(test1)[0]
        print(t2, t1)

        X = np.concatenate((test2, test1), axis = 0)
        y = [0] * t2 + [1] * t1
        print('X = ', np.shape(X))
        print('y = ', np.shape(y))

        clf = make_pipeline(StandardScaler(), LogisticRegression())
        time_decod = SlidingEstimator(clf, n_jobs = 1, scoring = 'roc_auc')

        scores = cross_val_multiscore(time_decod, X, y, cv = 10, n_jobs=1)

        scores = np.mean(scores, axis = 0)
        classify_scores = np.append(classify_scores, [scores], axis = 0)
        score_name = tmp_rootdir + '%s.txt' %(j)
        np.savetxt(score_name, classify_scores, fmt = '%1.4f')
        
        fig, ax = plt.subplots()

        ax.plot(raw.times, scores, label='score')
        ax.axhline(.5, color='k', linestyle='--', label='chance')
        ax.set_xlabel('Times')
        ax.set_ylabel('AUC')  # Area Under the Curve
        ax.legend()
        ax.axvline(.0, color='k', linestyle='-')
        ax.set_title('Sensor space decoding_%s' %(j))
        tmp_fig_name = fig_decoding_indiv + "%s_%s.png" %(subj, j)
        fig.savefig(tmp_fig_name)
        plt.close()

fname_can = tmp_rootdir + 'Can.txt'
fname_rev = tmp_rootdir+ 'Rev.txt'

raw_accuracy_can = np.loadtxt(fname_can)
raw_accuracy_rev = np.loadtxt(fname_rev)

mean_accuracy_can = np.mean(raw_accuracy_can, axis = 0)
mean_accuracy_rev = np.mean(raw_accuracy_rev, axis = 0)


can_sum = helper.mean_confidence_interval(raw_accuracy_can)
rev_sum = helper.mean_confidence_interval(raw_accuracy_rev)

time = raw.times
g = plt.figure(1, figsize=(7, 2.5))

fig = plt.figure(1, figsize=(10, 5.5))
helper.plot_mean_and_CI(can_sum[0], can_sum[1], can_sum[2], color_mean='r', color_shading='r')
helper.plot_mean_and_CI(rev_sum[0], rev_sum[1], rev_sum[2], color_mean='b', color_shading='b')

fig.savefig(fig_decoding_ave + 'Parietal.png')


