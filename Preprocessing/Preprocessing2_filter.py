###Add comment
import mne
import numpy as np
import scipy
import scipy.io
import matplotlib.pyplot as plt

###import config and helper files
import config
import helper

tmp_rootdir  = config.tmp_rootdir
raw_dir = config.raw_dir
resampled_dir = config.resampled_dir
filtered_dir = config.filtered_dir

l_freq = 0.1
h_freq = 32

###################################################################
######################### subject #################################
###################################################################
#============================================
#subject lists, in canonical-reverse order, reverse-canonical order or full list

subj_list = config.subj_list


###################################################################
########################## eeg channel list #######################
###################################################################
eeg_chan = config.eeg_chan
EOG_list = config.EOG_list

include = config.include
print('include = ', include)

drop_names = config.drop_names
print('drop_names = ', drop_names)

###################################################################
################################ events ###########################
###################################################################

event_id = config.event_id

biosemi_layout = mne.channels.read_montage(tmp_rootdir + 'biosemi_cap_32_M_2_EOG_3.locs')
biosemi_layout.ch_names = eeg_chan
n_subj = len(subj_list) 
#============================================    
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    resampled_fname = resampled_dir + "%s_resampled_raw.fif" %(subj)
    filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
    
    raw = mne.io.read_raw_fif(resampled_fname, preload = True)
    events = mne.find_events(raw)
    
    raw.set_eeg_reference('average', projection = False)
    print('bad channels = ', raw.info['bads'])

    
    raw.filter(l_freq, h_freq)
    raw.save(filtered_fname, overwrite = True)

    

