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
fig_dir_mmn = config.fig_dir_mmn

###################################################################
######################### subject #################################
###################################################################
#============================================
#subject lists, in canonical-reverse order, reverse-canonical order or full list

can_rev = config.can_rev
rev_can = config.rev_can
subj_list = config.subj_list
n_subj = len(subj_list) 


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


colors = dict(Can="Crimson", Rev="CornFlowerBlue")
linestyles = dict(Standard='-', Deviant='--')

chan = 'A31'

MMN = config.MMN

biosemi_layout = mne.channels.read_montage(tmp_rootdir + 'biosemi_cap_32_M_2_EOG_3.locs')
biosemi_layout.ch_names = eeg_chan

evoked_subj = dict()
evoked = dict()

n_subj = len(subj_list) 
#============================================    
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    resampled_fname = resampled_dir + "%s_resampled_raw.fif" %(subj)
    
    raw = mne.io.read_raw_fif(resampled_fname, preload = True)
    events = mne.find_events(raw, shortest_event = 1)
    raw.pick_types(include = eeg_chan, exclude = raw.info['bads'])

    raw.filter(0.1, 32)
    raw.set_eeg_reference('average', projection = False)
    
    #raw.filter(l_freq, h_freq)
        
    baseline = (-0.2, 0.0)
    epochs = mne.Epochs(raw, picks = chan, events = events, event_id=event_id, 
                        tmin = -0.2, tmax = 0.5, baseline=baseline)

    for j in range(len(MMN)):
        evoked_subj[MMN[j]] = epochs[MMN[j]].average()
        if i == 0:
            evoked[MMN[j]] = [evoked_subj[MMN[j]]]
        else:
            evoked[MMN[j]].append(evoked_subj[MMN[j]])

    fig = mne.viz.plot_compare_evokeds(evoked_subj, 
                                 show_sensors = False,
                                 picks = chan,
                                 colors = colors,
                                 linestyles = linestyles,
                                 title = 'Subject_%s_%s'%(subj, chan),
                                 show=False)
    fig_savename = fig_dir_mmn + '%s_MMN_%s.png' %(subj, chan)
    fig.savefig(fig_savename)

block_mmn = dict()
for j in range(len(MMN)):
    block_mmn[MMN[j]] = mne.grand_average(evoked[MMN[j]])

fig1 = mne.viz.plot_compare_evokeds(block_mmn, 
                             show_sensors = False,
                             picks = chan,
                             colors = colors,
                             linestyles = linestyles,
                             title = 'Average_FZ',
                             show = False)
fig_savename = fig_dir_mmn + 'ave_MMN_%s.png'%(chan)
fig1.savefig(fig_savename)

