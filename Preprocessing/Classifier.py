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


tmp_rootdir = '/Users/jessicaahn/Desktop/'
# raw_dir = tmp_rootdir + "resampled_data/"
# filtered_dir = tmp_rootdir + "filtered_raw_data/"
# ica_dir = tmp_rootdir + "ica_raw_data/"
# word_epoch_dir = tmp_rootdir + "word_epoch_raw_data/"
# evoked_dir = tmp_rootdir + "evoked/"
# analysis_dir = tmp_rootdir + "analysis/"
classify_dir = tmp_rootdir + "MNE/classification_logi_3electro/"
fig_dir = classify_dir + "Figures/"
resampled_dir = tmp_rootdir + 'MNE/resampled_data/'

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

n_subj = len(subj_list) 
# n_sesh = len(session_list)
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

    # print(epochs)
    beer = epochs['can/beer'].crop(-0.2, 0.5)

    pier = epochs['can/pier'].crop(-0.2, 0.5)

    beer_raw = beer.get_data()

    pier_raw = pier.get_data()
    print('beer raw shape: ' , beer_raw.shape)

    X = np.concatenate((beer_raw, pier_raw))

    Y = np.repeat([0,1], [np.shape(beer_raw)[0], np.shape(pier_raw)[0]], axis = 0)

    clf = make_pipeline(StandardScaler(), LogisticRegression())
    time_decod = SlidingEstimator(clf, n_jobs = 1, scoring = 'roc_auc')
    scores = cross_val_multiscore(time_decod, X, Y, cv = 5, n_jobs = 1)
    scores = np.mean(scores, axis = 0)
    classify_scores[:,i] = scores
    ave_score_by_subj.append(np.mean(scores))

    # FZ = epochs['deviant/can'].ch_names.index('A32')
    #
    # beer = epochs['can/beer'].ch_names.index('A32')
    #
    # pier = epochs['can/pier'].ch_names.index('A32')

    # selected_data = epochs_classify.get_data()[:,[FZ],:]
    #
    # classify_event = []
    # for x in map(str,epochs_classify.events[:,2]):
    #     classify_event.append(int(x[2]))

    # X = selected_data
    # # y = classify_event
    # clf = make_pipeline(StandardScaler(), LogisticRegression())
    # time_decod = SlidingEstimator(clf, n_jobs=1, scoring='roc_auc')

    # scores = cross_val_multiscore(time_decod, X, y, cv=5, n_jobs=1)
    # Mean scores across cross-validation splits
    # scores = np.mean(scores, axis=0)
    # classify_scores = np.append(classify_scores, [scores], axis = 0)

    # score_name = classify_dir + "%s.txt" %(sesh)
    # np.savetxt(score_name, scores, fmt = '%1.4f')

    # Plot
    # fig, ax = plt.subplots()

    # ax.plot(beer_raw.times, scores, label='score')
    # ax.axhline(.5, color='k', linestyle='--', label='chance')
    # ax.set_xlabel('Times')
    # ax.set_ylabel('AUC')  # Area Under the Curve
    # ax.legend()
    # ax.axvline(.0, color='k', linestyle='-')
    # ax.set_title('Sensor space decoding')
    # tmp_fig_name = fig_dir + "%s_%s.png" %(subj)
    # fig.savefig(tmp_fig_name)
      # size = np.array(range(epoch_size))
      # dataframe = pd.DataFrame(np.repeat([[subj],[sesh],[word]],FZ.shape[0], axis=1).T)
      # dataframe['Trial'] = np.repeat(size + 1, time)
      # dataframe['TimePoint'] = np.tile(range(-200,601),epoch_size)
      # dataframe['FZ'] = FZ*10**6 ##change the units from Volt to microvolt
      # dataframe['CZ'] = CZ*10**6
      # dataframe['PZ'] = PZ*10**6
      # dataframe.to_csv(path_or_buf = analysis_dir+'AveAmplitude_byTrial.csv', mode = 'a',header = False, 
      #              index = False)###for extracting the average amplitude

score_by_time_frame = classify_scores.mean(axis=1)
score_name = classify_dir + "average_score_by_timepoint.txt"
np.savetxt(score_name, score_by_time_frame, fmt = '%1.4f')

plt.plot(subj_list, ave_score_by_subj)
plt.suptitle('Mean Score average by Subject')
plt.show()
