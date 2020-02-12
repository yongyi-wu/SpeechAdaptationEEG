import mne
import numpy as np
import scipy
from mne.preprocessing import ICA, create_eog_epochs, create_ecg_epochs
import scipy.io

tmp_rootdir = '/Users/charleswu/Desktop/MMN/'
raw_dir = tmp_rootdir + "raw_data/"
resampled_dir = tmp_rootdir + 'resampled_data/'
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 

l_freq = 0.1
h_freq = 40
notch_freq = [60.0, 120.0]
Mastoids = ['EXG1','EXG2']
EOG_list = ['EXG3', 'EXG4', 'EXG5']

eeg_chan = []
eeg_chan = eeg_chan + ['A' + str(i+1) for i in range(32)]
chnames = eeg_chan + ['EXG' + str(i+1) for i in range(5)]
decim = 10

biosemi_layout = mne.channels.read_montage(tmp_rootdir + 'biosemi_cap_32_M_2_EOG_3.locs')
biosemi_layout.ch_names = chnames

trigger_list = [130816]

subj_list = ['001', '002', '003', '004', '005', '006', '008', '009', '010', '011', '012']

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

for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
    raw = mne.io.read_raw_fif(filtered_fname, preload = True)
    
    exclude_list = raw.info['ch_names'][-16:]
    print('exclude', exclude_list)

    # compute the ica components, if the number of IC components are smaller than the full rank
    # ICA works much better
    ica = ICA(n_components = None, max_iter = 10000, random_state = 10)
    # which sensors to use
    # compute the ica components ( slow ), no rejection was applied
    #reject = dict(eeg = 00e-6) 
    raw.set_montage(biosemi_layout)
    print(raw.info['dig'])
    ica.fit(raw, picks = eeg_chan, decim = decim)
    
    ica_out_fname = ica_dir + "%s_ica.fif" %(subj)
    #ica.save(ica_out_fname)

#    ###automatic EOG detection using correlation
#    eog_epochs_h1 = create_eog_epochs(raw, ch_name =EOG_list[0]) ##run this file with both vertical and 
#    ##horizontal EOG to see if the correlated components are different. 
#    eog_inds_h1, eog_scores_h1 = ica.find_bads_eog(eog_epochs_h1, ch_name =EOG_list[0])   
#
#    eog_epochs_h2 = create_eog_epochs(raw, ch_name =EOG_list[1])
#    eog_inds_h2, eog_scores_h2 = ica.find_bads_eog(eog_epochs_h2, ch_name =EOG_list[1]) 
#
#    eog_epochs_v = create_eog_epochs(raw, ch_name =EOG_list[2])
#    eog_inds_v, eog_scores_v = ica.find_bads_eog(eog_epochs_v, ch_name =EOG_list[2])     
#
#    
#    # =================== save the results =====================================
#    mat_name = ica_dir + "%s_HEOG1.mat" %(subj)
#    mat_dict = dict(eog_inds_h1 = eog_inds_h1, eog_scores_h1 = eog_scores_h1)
#                    #(ecg_inds = ecg_inds, ecg_scores = ecg_scores)
#    scipy.io.savemat(mat_name, mat_dict)
#
#    mat_name = ica_dir + "%s_HEOG2.mat" %(subj)
#    mat_dict = dict(eog_inds_h2 = eog_inds_h2, eog_scores_h2 = eog_scores_h2)
#                    #(ecg_inds = ecg_inds, ecg_scores = ecg_scores)
#    scipy.io.savemat(mat_name, mat_dict)
#
#    mat_name = ica_dir + "%s_VEOG.mat" %(subj)
#    mat_dict = dict(eog_inds_v = eog_inds_v, eog_scores_v = eog_scores_v)
#                    #(ecg_inds = ecg_inds, ecg_scores = ecg_scores)
#    scipy.io.savemat(mat_name, mat_dict)
