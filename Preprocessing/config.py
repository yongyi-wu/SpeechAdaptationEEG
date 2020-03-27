tmp_rootdir = '/Users/charleswu/Desktop/MMN/'
raw_dir = tmp_rootdir + "raw_data/"
resampled_dir = tmp_rootdir + 'resampled_data/'
filtered_dir = tmp_rootdir + "filtered_raw_data/"
resampled_events_dir = tmp_rootdir + "resampled_events/"
fig_dir_test = tmp_rootdir + "Plots/test_plot_indiv/"
fig_dir_exposure = tmp_rootdir + "Plots/exposure_plot_indiv/"
fig_dir_mmn = tmp_rootdir + "Plots/mmn_plot_indiv/"

###################################################################
######################### subject #################################
###################################################################
#============================================
#subject lists, in canonical-reverse order, reverse-canonical order or full list

can_rev = ['001', '002','003','004', '005', '007', '006', '008', '009', '010', '011', '012',
'014', '015', '016', '021'] 
rev_can = ['022', '024', '025', '027', '029', '030', '031', '032', '033']
# '028' does not have events recorded
#rev_can = ['029', '030', '031', '032', '033']
subj_list = can_rev + rev_can
Examine = ['004', '005', '006', '009', '010', '012', '014', '016', '019']
###################################################################
########################## eeg channel list #######################
###################################################################
eeg_chan = []
eeg_chan = eeg_chan + ['A' + str(i+1) for i in range(32)]
Mastoids = ['EXG1','EXG2']
EOG_list = ['EXG3', 'EXG4', 'EXG5']
trigger = ['Status']

include = eeg_chan + Mastoids + EOG_list + trigger

drop_names = ['GSR1', 'GSR2', 'Erg1', 'Erg2', 'Resp', 'Plet', 'Temp']
for i in range(5, 8):
    drop_names.append("EXG%d"%(i+1))

###################################################################
######################## events of interest #######################
###################################################################
event_id = {'Can/Standard':65321,
            'Can/Deviant':65322,
            'Rev/Standard':65341,
            'Rev/Deviant':65342,
            'Can/ExpSet':65391,
            'Can/ExpSat':65392,
            'Can/Test1':65401,
            'Can/Test2':65402,
            'Rev/ExpSet':65491,
            'Rev/ExpSat':65492,
            'Rev/Test1':65501,
            'Rev/Test2':65502
            }

###two blocks of canonical and reverse
Block = ['Can', 'Rev']

####3 event types, exposure, test and mmn stimuli. 
Exposure = ['ExpSat',
            'ExpSet']

Test = ['Test1',
        'Test2']

MMN = ['Standard',
       'Deviant']

trigger_list = [130816]

blocks = ['can', 'rev']
stimuli = ['standard', 'deviant']
