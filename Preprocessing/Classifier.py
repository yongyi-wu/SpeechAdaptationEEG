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


tmp_rootdir = '/Users/charleswu/Desktop/MNE/'
raw_dir = tmp_rootdir + "raw_data/"
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 
word_epoch_dir = tmp_rootdir + "word_epoch_raw_data/"
evoked_dir = tmp_rootdir + "evoked/"
analysis_dir = tmp_rootdir + "analysis/"
classify_dir = tmp_rootdir + "classification_logi_3electro/"
fig_dir = classify_dir + "Figures/"


Mastoids = ['M1','M2']
EOG_list = ['HEOG', 'VEOG']
n_eeg_channels = 32

l_freq = 0.1
h_freq = 110.0
notch_freq = [60.0,120.0]
fname_suffix = "filter_%d_%dHz_notch_raw" %(l_freq, h_freq)
alpha = 15
event_dir = tmp_rootdir + "event_files/"
event_id = {'S1/MU2/CON': 120,
            'S1/MU2/TAR': 121,
            'S1/ZHUO2/CON': 140, 
            'S1/ZHUO2/TAR': 141, 
            'S3/MU7/CON': 320,
            'S3/MU7/TAR': 321,
            'S3/ZHUO7/CON': 340, 
            'S3/ZHUO7/TAR': 341,
            'S5/MU5/CON': 520,
            'S5/MU5/TAR': 521, 
            'S5/ZHUO5/CON':540,
            'S5/ZHUO5/TAR':541,
            'S6/MU4/CON':620,
            'S6/MU4/TAR':621,
            'S6/ZHUO4/CON':640,
            'S6/ZHUO4/TAR':641}
events ='S1/MU2/CON','S1/MU2/TAR','S1/ZHUO2/CON', 'S1/ZHUO2/TAR', 'S3/MU7/CON','S3/MU7/TAR','S3/ZHUO7/CON','S3/ZHUO7/TAR','S5/MU5/CON','S5/MU5/TAR', 'S5/ZHUO5/CON','S5/ZHUO5/TAR','S6/MU4/CON','S6/MU4/TAR','S6/ZHUO4/CON','S6/ZHUO4/TAR'

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE','POST']
n_subj = len(subj_list) 
n_sesh = len(session_list)
##read the events from the event files instead of the stim channels in the data.
for j in range(n_sesh):
    sesh = session_list[j]
    classify_scores = np.empty((0,701))
    for i in range(n_subj):
        ch_names = ['FZ', 'CZ', 'PZ']
        subj = subj_list[i]
        fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
        this_epoch = mne.read_epochs(fname, preload = True)
        epochs_classify = this_epoch[events].crop(-0.2, 0.5)
        CZ = epochs_classify['S6/ZHUO4/TAR'].ch_names.index('CZ')
        FZ = epochs_classify['S6/ZHUO4/TAR'].ch_names.index('FZ')
        PZ = epochs_classify['S6/ZHUO4/TAR'].ch_names.index('PZ')
        
        selected_data = epochs_classify.get_data()[:,[CZ,FZ,PZ],:]

        classify_event = []
        for x in map(str,epochs_classify.events[:,2]):
            classify_event.append(int(x[2]))

        X = selected_data
        y = classify_event
        clf = make_pipeline(StandardScaler(), LogisticRegression())
        time_decod = SlidingEstimator(clf, n_jobs=1, scoring='roc_auc')

        scores = cross_val_multiscore(time_decod, X, y, cv=5, n_jobs=1)
        # Mean scores across cross-validation splits
        scores = np.mean(scores, axis=0)
        classify_scores = np.append(classify_scores, [scores], axis = 0)
        score_name = classify_dir + "%s.txt" %(sesh)
        np.savetxt(score_name, classify_scores, fmt = '%1.4f')
        # Plot
        fig, ax = plt.subplots()

        ax.plot(epochs_classify.times, scores, label='score')
        ax.axhline(.5, color='k', linestyle='--', label='chance')
        ax.set_xlabel('Times')
        ax.set_ylabel('AUC')  # Area Under the Curve
        ax.legend()
        ax.axvline(.0, color='k', linestyle='-')
        ax.set_title('Sensor space decoding')
        tmp_fig_name = fig_dir + "%s_%s.png" %(subj, sesh)
        fig.savefig(tmp_fig_name)
      # size = np.array(range(epoch_size))
      # dataframe = pd.DataFrame(np.repeat([[subj],[sesh],[word]],FZ.shape[0], axis=1).T)
      # dataframe['Trial'] = np.repeat(size + 1, time)
      # dataframe['TimePoint'] = np.tile(range(-200,601),epoch_size)
      # dataframe['FZ'] = FZ*10**6 ##change the units from Volt to microvolt
      # dataframe['CZ'] = CZ*10**6
      # dataframe['PZ'] = PZ*10**6
      # dataframe.to_csv(path_or_buf = analysis_dir+'AveAmplitude_byTrial.csv', mode = 'a',header = False, 
      #              index = False)###for extracting the average amplitude

