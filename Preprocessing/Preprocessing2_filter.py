###Add comment
import mne
import numpy as np
import scipy
import scipy.io
import matplotlib.pyplot as plt

tmp_rootdir = '/Users/charleswu/Desktop/MMN/'
raw_dir = tmp_rootdir + "raw_data/"
resampled_dir = tmp_rootdir + 'resampled_data/'
filtered_dir = tmp_rootdir + "filtered_raw_data/"
l_freq = 0.1
h_freq = 40
Mastoids = ['EXG1','EXG2']
#EOG_list = [u'LhEOG', u'RhEOG', u'LvEOG1', u'LvEOG2', u'RvEOG1']
EOG_list = ['EXG3', 'EXG4', 'EXG5']
#ECG_list = [u'ECG']
#ECG_list = ['ECG']

# drop_names = []
# for i in range(7):
#     drop_names.append("misc%d"%(i+1))

trigger_list = [130816]

subj_list = ['001', '002', '003', '004', '005', '008', '009', '011']

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

n_subj = len(subj_list) 
#============================================    
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    resampled_fname = resampled_dir + "%s_resampled_raw.fif" %(subj)
    filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
    
    raw = mne.io.read_raw_fif(resampled_fname, preload = True)
    events = mne.find_events(raw)
    
    raw.set_eeg_reference('average', projection = True)
    
    raw.filter(l_freq, h_freq)
    raw.save(filtered_fname, overwrite = True)

    

