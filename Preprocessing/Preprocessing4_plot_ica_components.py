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

l_freq = 0.1
h_freq = 40
notch_freq = [60.0, 120.0]
Mastoids = ['EXG1','EXG2']
EOG_list = ['EXG3', 'EXG4', 'EXG5']

fig_dir = tmp_rootdir + "ica_fig/"

subj_list = ['001', '002', '003', '004', '005', '006', '008', '009', '010', '011', '012']
n_subj = len(subj_list) 

biosemi_layout = mne.channels.read_layout('biosemi')
biosemi_layout.plot()

##it would be a much better idea to fun the following in an ide or jupyter.
for i in range(n_subj):
    subj = subj_list[i]
    print(subj)
    # ============= load ICA =========================================================
    ica_name = ica_dir + "%s_ica.fif" %(subj)
    ica = mne.preprocessing.read_ica(ica_name)

    ##check and see what the automatically detected components are
    fig = ica.plot_components()
    figure1 = fig[0]
    figure2 = fig[1]
    ##what we have here is a list of figures because they are broken into two subfigures
    tmp_fig_name1 = fig_dir  + "%s_component_plot0-19.png" %(subj)
    tmp_fig_name2 = fig_dir  + "%s_component_plot20-31.png" %(subj)
    #figure1.savefig(tmp_fig_name1)
    #figure2.savefig(tmp_fig_name2)