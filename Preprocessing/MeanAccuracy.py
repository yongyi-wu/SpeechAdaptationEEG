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
import scipy.interpolate


#NOTE : replace ... with your user name of your lap top
tmp_rootdir = '/Users/.../Desktop/MNE/'

classify_dir = tmp_rootdir + 'classification_logi_3electro/score_by_timepoint.txt'

raw_accuracy = np.loadtxt(classify_dir)
mean_accuracy = np.mean(raw_accuracy, axis = 1)
def mean_confidence_interval(data, confidence=0.95):
    ###assuming the input is an np array
    n = len(data)
    # m, se = np.mean(data, axis = 0), scipy.stats.sem(data)
    m, se = data, scipy.stats.sem(data)
    #h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-se, m+se##change this to h if you want CIs.

mean_accuracy_sum = mean_confidence_interval(mean_accuracy)

time = np.add(range(701), 1)
g = plt.figure(1, figsize=(7, 2.5))

def plot_mean_and_CI(mean, lb, ub, color_mean=None, color_shading=None):
    # plot the shaded range of the confidence intervals
    x = np.linspace(-200, 500, 91)
    plt.fill_between(x, ub, lb,
                     color=color_shading, alpha=.5)
    # plot the mean on top
    plt.plot(x, mean, color_mean)
    plt.plot(x, mean, '-x')
    
fig = plt.figure(1, figsize=(10, 5.5))
plot_mean_and_CI(mean_accuracy_sum[0], mean_accuracy_sum[1], mean_accuracy_sum[2], color_mean='b', color_shading='b')
fig.savefig(classify_dir + 'Score By Timeframe.png')
