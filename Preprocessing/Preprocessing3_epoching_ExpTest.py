###This file will save all epoched data as well as 
###evoked data for the events of interest
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
ica_dir = config.ica_dir
epoch_dir = config.epoch_dir
evoked_dir = config.evoked_dir

##fig dirs
fig_dir_mmn = config.fig_dir_mmn
fig_dir_test = config.fig_dir_test
fig_dir_exposure = config.fig_dir_exposure

fig_evoked_dir = config.fig_evoked_dir


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
FC_cluster = config.FC_cluster
parietal_cluster = config.parietal_cluster

include = config.include

drop_names = config.drop_names
###################################################################
################################ events ###########################
###################################################################
Block = config.Block
event_id = config.event_id

biosemi_layout = mne.channels.read_montage(tmp_rootdir + 'biosemi_cap_32_M_2_EOG_3.locs')
biosemi_layout.ch_names = eeg_chan
n_subj = len(subj_list) 
    
def save_evoked(eType, picks = 'A31', save_epoch = False):
    ####This function saves and plots epoched data for all subjects
    ####picks is the channel name and chan is the channel list
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
        raw_fname = ica_dir + "%s_after_ica_raw.fif" %(subj)
        
        raw = mne.io.Raw(raw_fname, preload = True)
        events = mne.find_events(raw, shortest_event = 1)
        raw.set_eeg_reference(['EXG1', 'EXG2'], projection = False) ###use the average of two mastoids 
        ###as reference like in Toscano McMurray 2010 rather than the average. 
        raw.pick_types(include = eeg_chan, exclude = raw.info['bads'])

        #raw.filter(0.1, 32)
        #raw.set_eeg_reference('average', projection = False)
            
        baseline = (-0.2, 0.0)
        epochs = mne.Epochs(raw, events = events, event_id=event_id, 
                            tmin = -0.2, tmax = 0.8, baseline=baseline)
        epoch_fname = epoch_dir + '%s_epoch_M.fif' %(subj) 
        if save_epoch == True:
            epochs.save(epoch_fname)


        for j in range(len(event_pick)):
            evoked_subj[event_pick[j]] = epochs[event_pick[j]].average()
            if i == 0:
                evoked[event_pick[j]] = [evoked_subj[event_pick[j]]]
            else:
                evoked[event_pick[j]].append(evoked_subj[event_pick[j]])

        #uncomment if you want plots for each subject
        fig = mne.viz.plot_compare_evokeds(evoked_subj, 
                                     show_sensors = False,
                                     picks = picks,
                                     colors = colors,
                                     linestyles = linestyles,
                                     title = 'Subject%s_parietal_%s'%(subj, eType),
                                     show=False)
        fig_savename = fig_dir + '%s_%s_parietal_cluster.png' %(subj, eType)
        fig.savefig(fig_savename)

    ##plot an averaged ERP 
    block_etype = dict()
    for j in range(len(event_pick)):
        block_etype[event_pick[j]] = mne.grand_average(evoked[event_pick[j]])

    fig1 = mne.viz.plot_compare_evokeds(block_etype, 
                                 show_sensors = False,
                                 picks = picks,
                                 colors = colors,
                                 linestyles = linestyles,
                                 title = 'Average_parietal_cluster_%s'%(eType),
                                 show = False)
    fig_savename = fig_evoked_dir  + 'ave_%s_parietal_cluster.png'%(eType)
    fig1.savefig(fig_savename)

if __name__ == '__main__':
    ###Execute the function and pick the event type and channel that you are interested in
    save_evoked('Exposure', picks = parietal_cluster)
    

