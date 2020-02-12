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

subj_list = ['001', '002', '003', '004', '005', '006', '008', '009', '010', '011', '012']
n_subj = len(subj_list) 

biosemi_layout = mne.channels.read_layout('biosemi')
biosemi_layout.plot()

###############################################################################################################
###############################################################################################################
################################################  001  ########################################################
###############################################################################################################
###############################################################################################################
subj = '001'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results
#mat_name1 = ica_dir  + "%s_HEOG1.mat" %(subj)
#mat_name2 = ica_dir  + "%s_HEOG2.mat" %(subj)
#mat_name3 = ica_dir  + "%s_VEOG.mat" %(subj)
#
#EXG_dict1 = scipy.io.loadmat(mat_name1)
#EXG_dict2 = scipy.io.loadmat(mat_name2)
#EXG_dict3 = scipy.io.loadmat(mat_name3)

#if len(EXG_dict1['eog_inds_h1'])>0:
#    print(EXG_dict1['eog_inds_h1'][0])
#else: 
#    # if no automatic EOG was detected, use the first 10 ICs that are mostly
#    # correlated with EOG1
#    eog_inds = np.argsort(np.abs(EXG_dict1['eog_scores_h1']))[-1:-10:-1]
#    print("empty HEOG1 inds, automatically choose", eog_inds)
#
#if len(EXG_dict2['eog_inds_h2'])>0:
#    print(EXG_dict2['eog_inds_h2'][0])
#else: 
#    eog_inds = np.argsort(np.abs(EXG_dict2['eog_scores_h2']))[-1:-10:-1]
#    print("empty HEOG2 inds, automatically choose", eog_inds)
#
#if len(EXG_dict3['eog_inds_v'])>0:
#    print(EXG_dict3['eog_inds_v'][0])
#else: 
#    eog_inds = np.argsort(np.abs(EXG_dict3['eog_scores_v']))[-1:-10:-1]
#    print("empty VEOG inds, automatically choose", eog_inds)
###from these components and the automatic detection results, 
###we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
###after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
###note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
###when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,4,5,19]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= [0,1,2])#,6,7,8,20,21,22,23])
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  002  ########################################################
###############################################################################################################
###############################################################################################################
subj = '002'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,5,11,25]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [0,1], show = False)#,6,7,8,20,21,22,23])
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  003  ########################################################
###############################################################################################################
###############################################################################################################
subj = '003'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,3,4,5,7,10,12,13,15,19,23,24,25,30]
###Here I think 7, 23, 24, 25 are channel noise
###0, 3, 4, 13 are eye blinks
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [0,3,4,7,13,23,24,25], show = False)#,6,7,8,20,21,22,23])
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))#,6,7,8,20,21,22,23])
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2,3,4,5,7,10,12,13,15,19,23,24,25,30]###note that not all are eye movements
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  004  ########################################################
###############################################################################################################
###############################################################################################################
subj = '004'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,6,20]
###0,1 are eye
###6,20 are channel
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [0,1,6,20], show = False)#,6,7,8,20,21,22,23])
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))#,6,7,8,20,21,22,23])
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,6,20]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  005  ########################################################
###############################################################################################################
###############################################################################################################
subj = '005'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [2,4,16,31]
##31  is channel
##16 might be muscle
##2,4 are eye
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [2,4,16,31], show = False)#,6,7,8,20,21,22,23])
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))#,6,7,8,20,21,22,23])
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [2,4,31]
new_ecg_inds = []
muscle_inds = [16]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  006  ########################################################
###############################################################################################################
###############################################################################################################
###TEMPORARILY DISCARD THIS PARTICIPANT FOR NOW
subj = '006'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,3,4,5,8,10,16,18,20,22,24,25,26,28,29]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [24,25,26,28,29], show = False)
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [num]
new_ecg_inds = []
muscle_inds = []
        
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  008  ########################################################
###############################################################################################################
###############################################################################################################
subj = '008'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [1,2,10,8,11,12,15,16,17,18,21,26,30,31]
##15, 16, 30 and 31 are channel
##2,10,11,18 eye

n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [1,2,10,8,11,15,16,21,18,30,31], show = False)
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [2,10,11,15,16,18,3,0,31]
new_ecg_inds = []
muscle_inds = []
        
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  009  ########################################################
###############################################################################################################
###############################################################################################################
subj = '009'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,3,4,6,10,13,27,30,31]
##0, 1, 3, 4 are eye
##27 and 31 are channel noise
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [0,1,3,4,27,31], show = False)
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,3,4,27,31]
new_ecg_inds = []
muscle_inds = []
        
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  010  ########################################################
###############################################################################################################
###############################################################################################################
subj = '010'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)
raw.plot()

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,4,6,7,8,17,13,14,25,27,28,31]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [num], show = False)
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [num]
new_ecg_inds = []
muscle_inds = []
        
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  011  ########################################################
###############################################################################################################
###############################################################################################################
subj = '011'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,3,4,5,14,18,29]
##14 looks like muscle
##0,1,3 and 5 are eyeblinks
##18 and 29 are channel
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [0,1,3,5,18,29], show = False)
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,3,5,18,29]
new_ecg_inds = []
muscle_inds = [14]
        
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################  012  ########################################################
###############################################################################################################
###############################################################################################################
subj = '012'
print(subj)
# ============= load ICA =========================================================
ica_name = ica_dir + "%s_ica.fif" %(subj)
ica = mne.preprocessing.read_ica(ica_name)
filtered_fname = filtered_dir + "%s_filtered_raw.fif" %(subj)
raw = mne.io.read_raw_fif(filtered_fname, preload = True)

####print information about automatic rejection on the screen so I can confirm with my manual 
###results

##from these components and the automatic detection results, 
##we think nnnnn might be blinks. nnnnnn might be muscle. nnnnnn might be heart
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
picks = [0,1,2,3,7,9,11,18,19,28,29]
##0,1,2,9,11are weird
##7,19 are eye blinks
##28 and 29 are channel
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks, show = False, plot_std = False)
ica.plot_sources(raw)

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_component%s.png" %(subj, picks[i])
    fig[i].savefig(tmp_fig_name1)

fig_compare = ica.plot_overlay(raw, exclude= [0,1,2,9,7,19,28,29], show = False)
fig_compare.savefig(fig_dir  + "%s_compare.png" %(subj))
# I finally decided to only reject 0,1,2 as EOC components

# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2,7,9,19,28,29]
new_ecg_inds = []
muscle_inds = []
        
print(new_eog_inds, new_ecg_inds, muscle_inds)
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_manual_check.mat" %(subj)
print(new_mat_name)
scipy.io.savemat(new_mat_name, new_mat)