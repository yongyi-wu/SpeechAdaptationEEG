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
fig_dir = tmp_rootdir + "exploratory_plot/"

l_freq = 2
h_freq = 32
notch_freq = [60.0, 120.0]
Mastoids = ['EXG1','EXG2']
#EOG_list = [u'LhEOG', u'RhEOG', u'LvEOG1', u'LvEOG2', u'RvEOG1']
EOG_list = ['EXG3', 'EXG4', 'EXG5']
#ECG_list = [u'ECG']
#ECG_list = ['ECG']

# drop_names = []
# for i in range(7):
#     drop_names.append("misc%d"%(i+1))

trigger_list = [130816]
#events = ['1','12','14','32','34','52','54','62','64']      
# the trigger is now status 
#exclude_list = Mastoids + EOG_list + drop_names + trigger_list #+ ECG_list

# subject
#============================================
#subj_id_seq = [1,2,3,4,5,6,7,8,10,11,12,13]    
#subj_list = ['Extra1','Extra2'] 
#for i in subj_id_seq:
#    subj_list.append('Subj%d' % i)
#subj_list = ['001', '002', '003', '004', '005', '006', '008', '009', '010', '011', '012']   #T2, A

evoked_dict = dict()
colors = dict(can="Crimson", rev="CornFlowerBlue")
linestyles = dict(standard='-', deviant='--')

chan = 'A31'

subj_list = ['001', '002', '003', '004', '005', '008', '009', '011']
n_subj = len(subj_list) 
eeg_chan = []
eeg_chan = eeg_chan + ['A' + str(i+1) for i in range(32)]
chnames = eeg_chan + ['EXG' + str(i+1) for i in range(5)]
blocks = ['can', 'rev']
stimuli = ['standard', 'deviant']
biosemi_layout = mne.channels.read_montage(tmp_rootdir + 'biosemi_cap_32_M_2_EOG_3.locs')
biosemi_layout.ch_names = chnames
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
#============================================    
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    resampled_fname = resampled_dir + "%s_resampled_raw.fif" %(subj)
    
    raw = mne.io.read_raw_fif(resampled_fname, preload = True)
    events = mne.find_events(raw)
    
    raw.set_eeg_reference('average', projection = True)
    
    raw.filter(l_freq, h_freq)
        
    baseline = (-0.2, 0.0)
    epochs = mne.Epochs(raw, events = events, event_id=event_id, 
                        tmin = -0.2, tmax = 0.5, baseline=baseline)
    evoked_dict["standard/can"] = epochs['standard/can'].average()
    evoked_dict["standard/rev"] = epochs['standard/rev'].average()
    evoked_dict["deviant/can"] = epochs['deviant/can'].average()
    evoked_dict["deviant/rev"] = epochs['deviant/rev'].average()
    
    #picks = range(32)
#    picks = [epochs.ch_names.index('A31'),
#             epochs.ch_names.index('A32'),
#             epochs.ch_names.index('A1'),
#             epochs.ch_names.index('A30'),
#             epochs.ch_names.index('A4'),
#             epochs.ch_names.index('A27'),
#             epochs.ch_names.index('A5'),
#             epochs.ch_names.index('A26'),
#             epochs.ch_names.index('A2'),
#             epochs.ch_names.index('A29')]

    picks = [epochs.ch_names.index(chan)]
    fig = mne.viz.plot_compare_evokeds(evoked_dict, 
                                 #picks=pick_CZ, 
                                 picks = picks,
                                 show_sensors = False,
                                 colors = colors,
                                 linestyles = linestyles,
                                 title = 'Subject_%s'%(subj))
    fig_savename = fig_dir + '%s_MMN.png' %(subj)
    fig.savefig(fig_savename)

evoked_dict = dict()

for sd in stimuli:
    for block in blocks:
        for i in range(n_subj):
            subj = subj_list[i]
            filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
            raw = mne.io.read_raw_fif(filtered_fname, preload = True)
            events = mne.find_events(raw)
            baseline = (-0.2, 0.0)
            epochs = mne.Epochs(raw, events = events, event_id=event_id, tmin = -0.2, tmax = 0.5, baseline=baseline)
            if i == 0:
                evoked = [epochs['%s/%s'%(sd,block)].average()]
            else:
                evoked.append(epochs['%s/%s'%(sd,block)].average())
        sd_block = mne.grand_average(evoked)
        evoked_dict['%s/%s'%(sd,block)] = sd_block
        
colors = dict(can="Crimson", rev="CornFlowerBlue")
linestyles = dict(standard='-', deviant='--')
picks = [epochs.ch_names.index(chan)]

fig = mne.viz.plot_compare_evokeds(evoked_dict, 
                             #picks=pick_CZ, 
                             picks = picks,
                             show_sensors = False,
                             colors = colors,
                             linestyles = linestyles,
                             title = 'Average_FZ')
fig_savename = fig_dir + 'ave_MMN.png'
fig.savefig(fig_savename)


####The code below plots the signal for the entire scalp, which we won't need right now.
####Ignore the code below for now. 

from mne.channels.layout import find_layout
layout = find_layout(raw.info)
pos = layout.pos.copy()
left = 0.03
right = 0.03
down = 0.05
up = 0.05

pos[13,0]=pos[13,0] + right ##have to mannually change the position of 
##the elctrodes for plotting

pos[0,0] = pos[0,0] + 2*right
pos[0,1] = pos[0,1] - down

pos[3,0] = pos[3,0] - left

pos[6,0] = pos[6,0] + right

pos[5,1] = pos[5,1] - down

pos[1,0] = pos[1,0] +right
pos[1,1] = pos[1,1] - down

pos[2,1] = pos[2,1] - down

pos[29,0] = pos[29,0] - 0.09
pos[29,1] = pos[29,1] - down

pos[26,0] = pos[26,0] + right

pos[28,0] = pos[28,0] - left

pos[27,1] = pos[27,1] - down

pos[23,0] = pos[23,0] - left

f = plt.figure()
f.set_size_inches(10,60)

ylims = (-1.1,1.1)
ymax = np.min(np.abs(np.array(ylims)))

colors = {"can": "crimson", "rev": 'steelblue'}

for pick, (pos_, ch_name) in enumerate(zip(pos, raw.ch_names)):
    pos_[2] = pos_[2] + 0.04
    ax = plt.axes(pos_)
    mne.viz.plot_compare_evokeds(evoked_block, picks = pick, axes=ax,
                         ylim=dict(eeg=ylims),
                         show=False,
                         colors = colors,
                         show_sensors=False,
                        show_legend=False,
                         title='');
    ax.set_xticklabels(())
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_yticks((-1, 1))
    ax.set_xticks((-0.2, -0.1, 0,0.1, 0.2, 0.3, 0.4, 0.5))
    ax.spines["left"].set_bounds(-1, 1)
    ax.set_ylim(ylims)
    ax.set_yticklabels('')
    ax.text(-.1, 1, ch_name, transform=ax.transAxes)

ax.legend(loc='right', bbox_to_anchor=(6, 10))
f.savefig(tmp_rootdir + 'TOPO_ERP.png', dpi = 600)
#picks = range(32)

