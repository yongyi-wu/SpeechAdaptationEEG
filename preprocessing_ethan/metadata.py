# SUBJECTS

def create_subject_list(start, end): # [start:end], both sides inclusive
    L = []
    for i in range(start, end+1): 
        L.append('0'*(3-len(str(i)))+str(i))
    return L

subject_list = create_subject_list(1, 33)
subject_list.remove('017') # not exists
subject_list.remove('030') # not exists


# FILE PATHS

import os

rootdir = 'F:/HoltLab/' # please change to a self-defined rood directory
# data
datadir = rootdir+'data/'
raw_dir = datadir+'raw/'
resampled_dir = datadir+'resampled/'
filtered_dir = datadir+'filtered_raw/'
ica_dir = datadir+'ica/'
ica_after_dir = datadir+'raw_after_ica/'
epoch_dir = datadir+'epoch/'
# visualizations
vizdir = rootdir+'visualizations/'
ica_viz_dir = vizdir+'ica/'
# create directories
for directory in [datadir, raw_dir, resampled_dir, filtered_dir, ica_dir, ica_after_dir, epoch_dir, vizdir, ica_viz_dir]: 
    if (not os.path.exists(directory)): 
        os.mkdir(directory)

def create_filename_dict(subjects, directory, suffix): # (key, entry) = (subject id, file path)
    d = {}
    for subject in subjects: 
        d[subject] = directory+subject+suffix
    return d

subjects = subject_list
raw_files = create_filename_dict(subjects, raw_dir, '.bdf')
resampled_files = create_filename_dict(subjects, resampled_dir, '_resampled_raw.fif')
filtered_files = create_filename_dict(subjects, filtered_dir, '_filtered_raw.fif')
ica_files = create_filename_dict(subjects, ica_dir, '_ica.fif')
ica_after_files = create_filename_dict(subjects, ica_after_dir, '_after_ica.fif')
epoch_files = create_filename_dict(subjects, epoch_dir, '_epoch.fif')
viz_files = create_filename_dict(subjects, vizdir, '')


# CHANNELS

import mne

mastoids = ['EXG1','EXG2']
EOG_channels = ['EXG3', 'EXG4', 'EXG5']
EEG_channels = ['A'+str(i+1) for i in range(32)]
EXG_channels = mastoids+EOG_channels
bad_channels = ['EXG6', 'EXG7', 'EXG8', 'GSR1', 'GSR2', 'Erg1', 'Erg2', 'Resp', 'Plet', 'Temp']

def read_montage(filename): # adapted from previous implementation by Charles Wu
    biosemi_layout = mne.channels.read_montage(datadir+filename)
    biosemi_layout.ch_names = EEG_channels+EXG_channels
    return biosemi_layout

def read_custom_montage(filename): # read_custom_montage() is in the new version of MNE
    ch_names1 = mne.channels.read_montage(datadir+filename).ch_names
    biosemi_layout = mne.channels.read_custom_montage(datadir+filename)
    for i in range(37): 
        name1 = ch_names1[i]
        index2 = biosemi_layout.ch_names.index(name1)
        biosemi_layout.ch_names[index2] = 'A'+str(i+1)

biosemi_layout = read_montage('biosemi_cap_32_M_2_EOG_3.locs')
# biosemi_layout = read_custom_montage('biosemi_cap_32_M_2_EOG_3.locs')


# EVENTS AND CONDITIONS

stimuli = ['standard', 'deviant']
blocks = ['can', 'rev']
conditions = [stimulus+'/'+block for stimulus in stimuli for block in blocks]
event_id = {
    'standard/can':65321,
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
(tmin, tmax) = (-0.2, +0.5)


# VISUALIZATION THEMES

colors = {
    'can': 'Crimson', 
    'rev': 'CornFlowerBlue'
}
linestyles = {
    'standard': '-', 
    'deviant': '--'
}