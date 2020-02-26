####this script reads the classification accuracies of subjects and calcaultes
####the average classification accuracy as well as the estimated confidence
####interval. Since we are estimating the mean of the classification accuracy
####we can assume that the mean is normally distributed and use a normal
####distribution to estimate the CI

import mne
import numpy as np
import scipy, time
import scipy.io
import scipy.stats as st
import matplotlib
import matplotlib.pyplot as plt

tmp_rootdir = '/Users/jessicaahn/Desktop/MNE/'
classify_dir = tmp_rootdir + 'classification_logi_3electro/score_by_timepoint.txt'

# fname_pre = classify_dir + 'PRE.txt'
# fname_post = classify_dir + 'POST.txt'
# raw_accuracy_pre = np.loadtxt(fname_pre)
# raw_accuracy_post = np.loadtxt(fname_post)

# mean_accuracy_pre = np.mean(raw_accuracy_pre, axis = 0)
# mean_accuracy_post = np.mean(raw_accuracy_post, axis = 0)
raw_accuracy = np.loadtxt(classify_dir)
mean_accuracy = np.mean(raw_accuracy, axis = 1)
def mean_confidence_interval(data, confidence=0.95):
    ###assuming the input is an np array
    n = len(data)
    # m, se = np.mean(data, axis = 0), scipy.stats.sem(data)
    m, se = data, scipy.stats.sem(data)
    #h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-se, m+se##change this to h if you want CIs.
# pre_sum = mean_confidence_interval(raw_accuracy_pre)
# post_sum = mean_confidence_interval(raw_accuracy_post)
mean_accuracy_sum = mean_confidence_interval(mean_accuracy)
print(mean_accuracy_sum)

time = np.add(range(701), 1)
g = plt.figure(1, figsize=(7, 2.5))

def plot_mean_and_CI(mean, lb, ub, color_mean=None, color_shading=None):
    # plot the shaded range of the confidence intervals
    x = np.subtract(range(mean.shape[0]), 200)
    plt.fill_between(np.subtract(range(mean.shape[0]), 200), ub, lb,
                     color=color_shading, alpha=.5)
    # plot the mean on top
    plt.plot(x, mean, color_mean)
    
fig = plt.figure(1, figsize=(10, 5.5))
# plot_mean_and_CI(pre_sum[0], pre_sum[1], pre_sum[2], color_mean='k', color_shading='k')
# plot_mean_and_CI(post_sum[0], post_sum[1], post_sum[2], color_mean='b', color_shading='b')
# fig.savefig(classify_dir + 'compare_svm_allelectro.png')

plot_mean_and_CI(mean_accuracy_sum[0], mean_accuracy_sum[1], mean_accuracy_sum[2], color_mean='b', color_shading='b')
fig.savefig(classify_dir + 'Score By Timeframe.png')
