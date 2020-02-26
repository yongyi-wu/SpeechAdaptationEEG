import mne
import numpy as np
import scipy, time
import scipy.io
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sys

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

import mne
from mne.datasets import sample
from mne.decoding import (SlidingEstimator, GeneralizingEstimator,
                          cross_val_multiscore, LinearModel, get_coef)

#NOTE : replace ... with your user name of your lap top
tmp_rootdir = '/Users/.../Desktop/'

#path to resampled data
resampled_dir = tmp_rootdir + 'MNE/resampled_data/'

#path to store classifcation scores
classify_dir = tmp_rootdir + "MNE/classification_logi_3electro/"
fig_dir = classify_dir + "Figures/"

Mastoids = ['M1','M2']
EOG_list = ['HEOG', 'VEOG']
n_eeg_channels = 32


subj_list = ['001', '002', '003', '004', '005', '008', '009', '011', '012']
n_subj = len(subj_list) 
eeg_chan = []
eeg_chan = eeg_chan + ['A' + str(i+1) for i in range(32)]
chnames = eeg_chan + ['EXG' + str(i+1) for i in range(5)]
blocks = ['can', 'rev']
stimuli = ['standard', 'deviant']
biosemi_layout = mne.channels.read_montage(tmp_rootdir +'SpeechAdaptationEEG/Preprocessing/biosemi_cap_32_M_2_EOG_3.locs')
print( 'biosemi : ', biosemi_layout)
biosemi_layout.ch_names = chnames
print('chnames: ', chnames)
event_id = {'standard/can':65321,
            'deviant/can':65322,
            'standard/rev':65341,
            'deviant/rev':65342,
            'can/beer':65391,
            'can/pier':65392,
            'canTest1':65401,
            'canTest2':65402,
            'rev/beer':65491,
            'rev/pier':65492,
            'revTest1':65501,
            'revTest2':65502
            }


##read the events from the event files instead of the stim channels in the data.

n_subj = len(subj_list)
classify_scores = np.zeros((91, 9))
ave_score_by_subj = []
# classify_scores = np.
#============================================    
for i in range(n_subj):
    subj = subj_list[i]

    resampled_fname = resampled_dir + "%s_resampled_raw.fif" %(subj)
    
    raw = mne.io.read_raw_fif(resampled_fname, preload = True)
    events = mne.find_events(raw)

    raw.set_eeg_reference('average', projection = True)
    print('Raw chNames : ' ,raw.ch_names)
    baseline = (-0.2, 0.0)
    epochs = mne.Epochs(raw, events = events, event_id=event_id, 
                        tmin = -0.2, tmax = 0.5, baseline=baseline, preload= True)

    FZ = epochs['standard/rev'].ch_names.index('A32')

    beer = epochs['can/beer'].crop(-0.2, 0.5)

    pier = epochs['can/pier'].crop(-0.2, 0.5)

    beer_raw = beer.get_data()[:, [FZ], :]

    pier_raw = pier.get_data()[:, [FZ], :]

    print('beer raw shape: ', beer_raw.shape)

    X = np.concatenate((beer_raw, pier_raw))

    Y = np.repeat([0,1], [np.shape(beer_raw)[0], np.shape(pier_raw)[0]], axis = 0)

    clf = make_pipeline(StandardScaler(), LogisticRegression())
    time_decod = SlidingEstimator(clf, n_jobs = 1, scoring = 'roc_auc')
    scores = cross_val_multiscore(time_decod, X, Y, cv = 5, n_jobs = 1)
    scores = np.mean(scores, axis = 0)
    classify_scores[:,i] = scores
    ave_score_by_subj.append(np.mean(scores))

score_name = classify_dir + "score_by_timepoint.txt"
np.savetxt(score_name, classify_scores, fmt = '%1.4f')

plt.plot(subj_list, ave_score_by_subj)
plt.suptitle('Mean Score average by Subject')
plt.show()
