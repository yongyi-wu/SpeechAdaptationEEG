# SpeechAdaptationEEG

This is one of Charles Wu's dissertation project investigating how the brain responses to the same sounds as a function of different speech manipulation. 

# Getting started with Python-MNE for EEG analysis

## Introduction
If you are doing research using EEG, chances are you will need special libraris or packages to conduct your analysis. Common packages such as [EEGLAB](https://sccn.ucsd.edu/eeglab/index.php) and [Fieldtrip](http://www.fieldtriptoolbox.org/) are both Matlab-based toolboxes for analyzing EEG/MEG data. 

Here I introduce a new python-based library called [MNE](https://mne.tools/stable/index.html), which I personally believe is a more flexible and powerful tool for performing EEG/MEG analysis. Especially if you prefer to code in Python and have basic knowledge of EEG, MNE would be very easy to navigate. 

## Python basics
If you have never used Python before, don't panic! Python is a very intuitive and easy language for beginners. There's an [open-source programming course](https://www.cs.cmu.edu/~112/index.html) using Python at my home institution Carnegie Mellon to help you get started. 

Other useful resources for coding in Python include using [Jupyter Notebook](https://jupyter.org/) (Jupyter notebook can not only render markdown files such as this one but can also run R or Python code and put graphs in Jupyter Notebook to share it with other people!), [visualization with Matplotlib](https://matplotlib.org/), [visualization with Seaborn](https://seaborn.pydata.org/), [machine learning in Python](https://towardsdatascience.com/beginners-guide-to-machine-learning-with-python-b9ff35bc9c51) etc.

I would also strongly recommend building virtual environment using [virtualenv](https://medium.com/@__pamaron__/understanding-and-use-python-virtualenvs-from-data-scientist-perspective-bfed61faeb3f). Different tasks might require that you use different versions of the same package. Using virtual environment gives you flexibility to maintain multiple versions of the same package in separate places so you won't have the headache of downgrading and upgrading packages all the time. 

Before you install the MNE package, check [this](https://mne.tools/stable/install/mne_python.html) to make sure that you have the appropriate Python version and all the MNE dependencies installed! 

Note that you can type in your terminal

`pip show python`

or if you have anaconda

`conda search python`

to check your current version of Python or any other software on your computer.

Also read [here](https://mne.tools/stable/install/index.html) to learn more about using mne and enhance your analysis experience.  

For most of the code that you run, you can just use terminal and type
`python filename` 
to run the file. But if you need to debug your code or interact with your plots, using an IDE would be helpful. For example, Jupyter notebook would be a great choice to debug and plot. [Spyder](https://www.spyder-ide.org/), which is what I use, is also a great tool. 

## EEG basics
I find [this](https://imotions.com/blog/eeg/) blog to be a good general introduction to EEG signals in the brain. It covers a wide range of topics with brief texts from basic neuroscience knowledge to EEG hardware details, all the way to preprocessing and data analysis. Reading this would be very helpful, especially the preprocessing section, for you to understand why we do the preprocessing steps in our code. 

## EEG preprocessing

You can play around with some sample data that comes with the MNE package like [this](https://mne.tools/stable/auto_examples/io/plot_read_epochs.html#sphx-glr-auto-examples-io-plot-read-epochs-py)
But I have also uploaded my data to Box and shared with you so you can just download my data and work with it directly! All of the code you use can be found in the "Preprocessing" folder with individual python scripts for each step, including the config file and helper file with helper functions

#### Downsampled raw data
The raw form of the EEG data (stored as .bdf binary files right off the Biosemi software) was first downsampled and processed, since there were human errors during recording such as changing the sampling rate and adding channels that were not used. All raw data were downsampled to 128 Hz with only 32 EEG channels(A1-A32) + 5 external channels were included. This code for this step was not uploaded because raw data files can be very large and working with them takes a long time. So I completed this step and stored the data in conventional MNE format, .fif. Therefore, the data that you have access to are .fif data after the downsampling and filtering. Please also note that I also identified EEG channels that are extremely noisy and mark them as bad channels stored in the resampled data. You can examine these channels by first reading the resampled data as 'raw' and then use the line
`raw.info['bads']` in your IDE(Jupyter or Spyder)
to examine these channels for each participants. 

#### Visualizing raw data
All the folder paths, parameters, events, channels etc are specified in the config.py folder such that you only need to change them in one place. 

The plots generated will be stored in separate folders and you will need to generate these folders first before you can run the code. Check the config file for 'fig_dir' to see which folder names you need. 

Once you download the Resampled_Raw.zip file that contains all the downsampled data, you can first visualize it using the Preprocessing1_visualization.py file. Note that in this file, you can change the event type that you are trying to plot at the end of the file, by specifying 'MMN', 'Test' or 'Exposure'. 

You can also uncomment the section where plots for each subject are generated if you would like to examine each individual's averaged EEG data. 

Note that you can also change the electrode(s) that you want to plot. The default channel is 'A31', which is right at the top of your scalp and this is one of the electrodes of interest. You can also change this by using a different electrode or adding multiple electrodes, in which case an average across the electrodes will be plotted. For example, in the config file, I specified a fronto-central cluster which we can examine later. So you can use those electrodes in the config file and plot an average across them. 

It'd be great to plot the data every step along the way so you can see how the data change. Make sure you change the figure name so that the figures are not overwritten when you plot after every step. 







