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
fig_dir_test = config.fig_dir_test
fig_dir_exposure = config.fig_dir_exposure

###################################################################
######################### subject #################################
###################################################################
#============================================
#subject lists, in canonical-reverse order, reverse-canonical order or full list

can_rev = config.can_rev
rev_can = config.rev_can
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

Block = config.Block
chan = 'A31'

biosemi_layout = mne.channels.read_montage(tmp_rootdir + 'biosemi_cap_32_M_2_EOG_3.locs')
biosemi_layout.ch_names = eeg_chan

###function for plotting, with event type and channels.
###multiple channels will be averaged 
def plot_ERP(eType, figName, picks = 'A31'):
    ####This function plots both ERP plots for each subject
    ####And the averaged ERP across all subjects
    if eType == 'MMN':
        eventType2 = config.MMN
        fig_dir = fig_dir_mmn
    elif eType == 'Test':
        eventType2 = config.Test
        fig_dir = fig_dir_test
    elif eType == 'Exposure':
        eventType2 = config.Exposure
        fig_dir = fig_dir_exposure
    else:
        raise Exception('Event type does not exist')

    if figName == 'resampled':
        raw_dir = resampled_dir
    elif figName == 'filtered':
        raw_dir = filtered_dir
    else: 
        raise Exception('Preprocessing step does not exist')

    event_pick, colors, linestyles = helper.pick_event_type(Block, eventType2)
    print(event_pick)
    evoked_subj = dict()
    evoked = dict()
    n_subj = len(subj_list) 

    ###define the paths to save the plots, depending on which event type to plot
    #============================================  
    #start the plotting by each subject  
    for i in range(n_subj):
        subj = subj_list[i]
        print(subj)
        raw_fname = raw_dir + "%s_%s_raw.fif" %(subj, figName)
        
        raw = mne.io.read_raw_fif(raw_fname, preload = True)
        events = mne.find_events(raw, shortest_event = 1)
        raw.pick_types(include = eeg_chan, exclude = raw.info['bads'])

        #raw.filter(0.1, 32)
        #raw.set_eeg_reference('average', projection = False)
            
        baseline = (-0.2, 0.0)
        epochs = mne.Epochs(raw, picks = picks, events = events, event_id=event_id, 
                            tmin = -0.2, tmax = 0.5, baseline=baseline)

        for j in range(len(event_pick)):
            evoked_subj[event_pick[j]] = epochs[event_pick[j]].average()
            if i == 0:
                evoked[event_pick[j]] = [evoked_subj[event_pick[j]]]
            else:
                evoked[event_pick[j]].append(evoked_subj[event_pick[j]])

        #uncomment if you want plots for each subject
        # fig = mne.viz.plot_compare_evokeds(evoked_subj, 
        #                              show_sensors = False,
        #                              picks = picks,
        #                              colors = colors,
        #                              linestyles = linestyles,
        #                              title = 'Subject_%s_%s_%s'%(subj, picks, figName),
        #                              show=False)
        # fig_savename = fig_dir + '%s_%s_%s.png' %(subj, figName, picks)
        # fig.savefig(fig_savename)

    ##plot an averaged ERP 
    block_etype = dict()
    for j in range(len(event_pick)):
        block_etype[event_pick[j]] = mne.grand_average(evoked[event_pick[j]])

    fig1 = mne.viz.plot_compare_evokeds(block_etype, 
                                 show_sensors = False,
                                 picks = picks,
                                 colors = colors,
                                 linestyles = linestyles,
                                 title = 'Average_%s_%s_%s'%(picks, eType, figName),
                                 show = False)
    fig_savename = fig_dir + 'ave_%s_%s.png'%(picks, figName)
    fig1.savefig(fig_savename)

if __name__ == '__main__':
    ###Execute the function and pick the event type and channel that you are interested in
    plot_ERP('Exposure', 'resampled')

