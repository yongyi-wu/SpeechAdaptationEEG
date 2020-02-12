# -*- coding: utf-8 -*-
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

subj_list = ['001', '002', '003', '004', '005', '008', '009', '011', '012']
n_subj = len(subj_list) 


for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
    raw = mne.io.read_raw_fif(filtered_fname, preload = True)
    # ============= load ICA =========================================================
    ica_name = ica_dir + "%s_ica.fif" %(subj)
    ica = mne.preprocessing.read_ica(ica_name)
    
    new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
    new_mat = scipy.io.loadmat(new_mat_name)

    if len(new_mat['new_eog_inds'])>0:
        new_eog_inds = new_mat['new_eog_inds'][0].astype(np.int)
    else:
        new_eog_inds = []
    if len(new_mat['new_ecg_inds'])>0:
        new_ecg_inds = new_mat['new_ecg_inds'][0].astype(np.int)
    else:
        new_ecg_inds = []
    if len(new_mat['muscle_inds'])>0:
        muscle_inds = new_mat['muscle_inds'][0].astype(np.int)
    else:
        muscle_inds = []    
    
    union = np.union1d(muscle_inds, np.union1d(new_eog_inds, new_ecg_inds))
    exclude = union.astype(np.int).tolist()
    print(exclude)
    ica.exclude = exclude

    raw_after_ica = ica.apply(raw,exclude = ica.exclude)  
                
    # since I didn't have bad channels in my data I will not interpolate the bad channels. 
        
    ica_raw_name = ica_dir  + "%s_after_ica_raw.fif" %(subj)
    raw_after_ica.save(ica_raw_name, overwrite = True)  
