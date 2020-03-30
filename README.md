# SpeechAdaptationEEG

This is one of Charles Wu's dissertation project investigating how the brain responses to the same sounds as a function of different speech manipulation. 

# Getting started with Python-MNE for EEG analysis

## Introduction
If you are doing research using EEG, chances are you will need special libraris or packages to conduct your analysis. Common packages such as [EEGLAB](https://sccn.ucsd.edu/eeglab/index.php) and [Fieldtrip](http://www.fieldtriptoolbox.org/) are both Matlab-based toolboxes for analyzing EEG/MEG data. 

Here I introduce a new python-based library called [MNE](https://mne.tools/stable/index.html), which I personally believe is a more flexible and powerful tool for performing EEG/MEG analysis. Especially if you prefer to code in Python and have basic knowledge of EEG, MNE would be very easy to navigate. 

## Python basics
If you have never used Python before, don't panic! Python is a very intuitive and easy language for beginners. There's an [open-source programming course](https://www.cs.cmu.edu/~112/index.html) using Python at my home institution Carnegie Mellon to help you get started. 

Other useful resources for coding in Python include using [Jupyter Notebook](https://jupyter.org/) (This document was written in Jupyter notebook. But you can also run R or Python code and put graphs in Jupyter Notebook to share it with other people!), [visualization with Matplotlib](https://matplotlib.org/), [visualization with Seaborn](https://seaborn.pydata.org/), [machine learning in Python](https://towardsdatascience.com/beginners-guide-to-machine-learning-with-python-b9ff35bc9c51) etc.

I would also strongly recommend building virtual environment using [virtualenv](https://medium.com/@__pamaron__/understanding-and-use-python-virtualenvs-from-data-scientist-perspective-bfed61faeb3f). Different tasks might require that you use different versions of the same package. Using virtual environment gives you flexibility to maintain multiple versions of the same package in separate places so you won't have the headache of downgrading and upgrading packages all the time. 

Before you install the MNE package, check [this](https://mne.tools/stable/install/mne_python.html) to make sure that you have the appropriate Python version and all the MNE dependencies installed! 

Note that you can type in your terminal

`pip show python`

or if you have anaconda

`conda search python`

to check your current version of Python or any other software on your computer.

Also read [here](https://mne.tools/stable/install/index.html) to learn more about using mne and enhance your analysis experience.  

## EEG basics
I find [this](https://imotions.com/blog/eeg/) blog to be a good general introduction to EEG signals in the brain. It covers a wide range of topics with brief texts from basic neuroscience knowledge to EEG hardware details, all the way to preprocessing and data analysis. Reading this would be very helpful, especially the preprocessing section, for you to understand why we do the preprocessing steps in our code. 

## EEG preprocessing

#### Downsampled raw data
The raw form of the EEG data (stored as .bdf binary files right off the Biosemi software) was first downsampled and processed, since there were human errors during recording such as changing the sampling rate and adding channels that were not used. All raw data were downsampled to 128 Hz and only 32 EEG channels(A1-A32) + 5 external channels were included. This code for this step was not uploaded because raw data files can be very large and working with them takes a long time. So I completed this step and stored the data in conventional MNE format, .fif. Therefore, the data that you have access to are .fif data after the downsampling and filtering. 
