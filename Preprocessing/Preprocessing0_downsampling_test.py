###Add comment
import mne
import numpy as np
import scipy
import scipy.io

tmp_rootdir = '/Users/charleswu/Desktop/MMN/'
raw_dir = tmp_rootdir + "raw_data/"
resampled_dir = tmp_rootdir + 'resampled_data/'
filtered_dir = tmp_rootdir + "filtered_raw_data/"
resampled_events_dir = tmp_rootdir + "resampled_events/"

Mastoids = ['EXG1','EXG2']
#EOG_list = [u'LhEOG', u'RhEOG', u'LvEOG1', u'LvEOG2', u'RvEOG1']
EOG_list = ['EXG3', 'EXG4', 'EXG5']
#ECG_list = [u'ECG']
#ECG_list = ['ECG']

# drop_names = []
# for i in range(7):
#     drop_names.append("misc%d"%(i+1))

#events = ['1','12','14','32','34','52','54','62','64']      
# the trigger is now status 
#exclude_list = Mastoids + EOG_list + drop_names + trigger_list #+ ECG_list

# subject
#============================================
#subj_id_seq = [1,2,3,4,5,6,7,8,10,11,12,13]    
#subj_list = ['Extra1','Extra2'] 
#for i in subj_id_seq:
#    subj_list.append('Subj%d' % i)
subj_list = ['001','002','003','004', '005', '008', '009', '011', '012'] 
n_subj = len(subj_list)
#########################################################################################################
##################There seems to be something wrong with 007, check later#####################
#########################################################################################################

EX_chlist = ['B', 'C', 'D', 'E', 'F', 'G', 'H']
EX = []
for letter in EX_chlist:
    EX = EX + [letter+str(i+1) for i in range(32)]
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

#============================================    
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    raw_fname = raw_dir + "%s.bdf" %(subj)
    resampled_fname = resampled_dir + "%s_resampled_raw.fif" %(subj)
    resampled_events = resampled_dir + "%s_resampled_events.fif" %(subj)
    
    raw = mne.io.read_raw_bdf(raw_fname, preload = True, eog = EOG_list, exclude = EX)
    events = mne.find_events(raw)
    print('Number of events before resampling:', len(events))
    print('# channels = ', str(len(raw.ch_names)))
    raw_resampled_1000, events_resampled_1000 = raw.copy().resample(1000, npad = 'auto', events = events)
    
    print('Number of events after resampling:', len(events_resampled_1000))
    events_resampled_1000
    raw_resampled_1000.save(resampled_fname, overwrite = True)
    events_resampled_1000.save(resampled_events, overwrite = True)
    
    #raw.plot()
