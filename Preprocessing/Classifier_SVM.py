import numpy as np
import mne
import matplotlib.pyplot as plt
from mne.decoding import cross_val_multiscore, SlidingEstimator
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC

#NOTE : replace ... with your user name of your lap top
tmp_rootdir = '/Users/.../Desktop/'

#path to resampled data
resampled_dir = tmp_rootdir + 'MNE/resampled_data/'

#path to store classifcation scores
classify_dir = tmp_rootdir + "MNE/classification_svm_3electro/"
fig_dir = classify_dir + "Figures/"

n_eeg_channels = 32 #32 channels
subj_list = ['001', '002', '003', '004', '005', '008', '009', '011', '012']
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
classify_scores = np.zeros((91, 9))
for i in range(n_subj):
    subj = subj_list[i]

    resampled_fname = resampled_dir + "%s_resampled_raw.fif" %(subj)
    raw = mne.io.read_raw_fif(resampled_fname, preload = True)
    events = mne.find_events(raw)
    raw.set_eeg_reference('average', projection = True)
    baseline = (-0.2, 0.0)
    #Epochs objects are a data structure for representing and analyzing equal-duration chunks of the EEG/MEG signal
    epochs = mne.Epochs(raw, events = events, event_id=event_id,
                        tmin = -0.2, tmax = 0.5, baseline=baseline, preload= True)
    FZ = epochs['standard/rev'].ch_names.index('A32')
    beer = epochs['can/beer'].crop(-0.2, 0.5)
    pier = epochs['can/pier'].crop(-0.2, 0.5)
    beer_raw = beer.get_data()[:, [FZ], :]
    pier_raw = pier.get_data()[:, [FZ], :]

    X = np.concatenate((beer_raw, pier_raw))
    Y = np.repeat([0, 1], [np.shape(beer_raw)[0], np.shape(pier_raw)[0]], axis=0)
    # Split dataset into training set and test set
    #70% training and 30% test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=109)

    #Linear SVM classifier
    clf = make_pipeline(LinearSVC())
    time_decod = SlidingEstimator(clf, n_jobs=1, scoring='roc_auc')
    scores = cross_val_multiscore(time_decod, X, Y, cv = 5, n_jobs = 1)
    scores = np.mean(scores, axis=0)
    classify_scores[:, i] = scores



score_name = classify_dir + "score_by_timepoint.txt"
np.savetxt(score_name, classify_scores, fmt = '%1.4f')













