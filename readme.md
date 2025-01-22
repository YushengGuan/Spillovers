# Supplementary Materials to *Solar and Wind Technological Spillovers towards the Global Renewable Energy Tripling Target*
Authors: Yusheng Guan, Kangxin An, Shihui Zhang, Can Wang  
Contact: canwang@tsinghua.edu.cn

## 1. Brief introduction
- *Dataset.xlsx* contains all raw data collected from IRENA after our pre-processing.  
The data are used directly by the executive files.  
**ATTENTION**Do not change the file directly if you want to run the executive files.  
- *main.py* is the overall executive python file to run all files.
- *Regression.py* is the executive python file to regress the learning curve models in our study.
- *Figure_{number}.py* is the independent executive python file to generate figures in out study.
- *Results* is a folder containing all regression results.
- *CGEinputs* is a folder containing parts of the parameters of the GHEER model.
- *CGEresults* is a folder containing the outputs of the GHEER model.
- *worldmap_gapde* is the base files of the world maps in some figures.
- *Figs* is the outcome path of all figures generated.  
If you want to run all files, please kindly just run *main.py*.  
Reminder: Do not change the files directly if you want to run the executive files.  
If you have any questions, please contact us by email.

## 2. Programing environment
- python 3.10
  - pandas 2.1.0
  - numpy 1.26.4
  - statsmodels 0.14.2
  - matplotlib 3.7.2
  - seaborn 0.12.2
  - geopandas 0.14.4
