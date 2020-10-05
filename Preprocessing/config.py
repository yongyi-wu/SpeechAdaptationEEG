###All the folder paths you need
tmp_rootdir = '/Users/charleswu/Desktop/MMN/'
raw_dir = tmp_rootdir + "raw_data/"
resampled_dir = tmp_rootdir + 'resampled_data/'
filtered_dir = tmp_rootdir + 'filtered_raw_data/'
resampled_events_dir = tmp_rootdir + 'resampled_events/'
ica_dir = tmp_rootdir + 'ica_raw_data/'
epoch_dir = tmp_rootdir + 'epoch_data/'
evoked_dir = tmp_rootdir + 'evoked_data/'

###folder paths for storing figures/plots
fig_dir = tmp_rootdir + 'SpeechAdaptationEEG/Plots/'
fig_dir_test = fig_dir + 'test_plot_indiv/'
fig_dir_exposure = fig_dir + 'exposure_plot_indiv/'
fig_dir_mmn = fig_dir + 'mmn_plot_indiv/'
fig_evoked_dir = fig_dir + 'plot_evoked/'
fig_cluster = fig_dir + 'diffwave_cluster/'
fig_decoding_ave = fig_dir + 'decoding_ave/'
fig_decoding_indiv = fig_dir + 'decoding_indiv/'

###################################################################
######################### subject #################################
###################################################################
#============================================

#subject lists, in canonical-reverse order, reverse-canonical order or full list

#can_rev = ['001', '002','003','004', '005', '007', '006', '008', '009', '010', '011', '012', '015', '016', '021'] #014 rejected
can_rev = ['001', '002','003','004', '005', '007', '006', '008', '009', '010', '011', '015', '016', '021'] #014 rejected
###subj 12 rejected when using average mastoid reference between 12 has really noisy M2. 
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

###fronto-central electrodes used in Moberly et al., 2014
FC_cluster = ['A31', 'A32', 'A4', 'A27', 'A5', 'A26', 'A8', 'A23'] #'A2', 'A29'

include = eeg_chan + Mastoids + EOG_list + trigger

drop_names = ['GSR1', 'GSR2', 'Erg1', 'Erg2', 'Resp', 'Plet', 'Temp']
for i in range(5, 8):
    drop_names.append("EXG%d"%(i+1))

###parietal electrodes used in Toscano & Mcmurray, 2010
#parietal_cluster = ['A4', 'A27', 'A31', 'A8', 'A32', 'A23', 'A12', 'A13', 'A19', 'A7', 'A24', 'A11', 'A20']
##parietal electrodes used Toscano & McMurray, 2010: F3, F4, Fz, C3, Cz, C4, P3, Pz, P4, T3, T4, T5, T6
parietal_cluster = ['A12', 'A13', 'A19']
##parietal electrodes used Toscano & McMurray, 2010: P3, Pz, P4

###################################################################
######################## events of interest #######################
###################################################################
event_id = {'Can/Standard':65321,
            'Can/Deviant':65322,
            'Rev/Standard':65341,
            'Rev/Deviant':65342,
            'Can/ExpBeer':65391,
            'Can/ExpPier':65392,
            'Can/Test1':65401,
            'Can/Test2':65402,
            'Rev/ExpBeer':65491,
            'Rev/ExpPier':65492,
            'Rev/Test1':65501,
            'Rev/Test2':65502
            }

###two blocks of canonical and reverse
Block = ['Can', 'Rev']

####3 event types, exposure, test and mmn stimuli. 
Exposure = ['ExpPier',
            'ExpBeer']

Test = ['Test2',
        'Test1']

MMN = ['Standard',
       'Deviant']

trigger_list = [130816]

blocks = ['can', 'rev']
stimuli = ['standard', 'deviant']
