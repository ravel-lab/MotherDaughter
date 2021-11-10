#!/usr/bin/env python3

#importing packages to be used
import pandas as pd
import numpy as np
import sys
import seaborn as sns
import  matplotlib.pyplot as plt
from scipy import stats
import matplotlib.patches as mpatches


#reading in the data
permutations = pd.read_csv("md_perm_test_PERMs.csv",sep=",")
observed = pd.read_csv("md_perm_test_OBSERVED.csv",sep=",")

#establishing the plot
stacked_fig, stacked_axs = plt.subplots(1,2, figsize=(12,7), facecolor='w', edgecolor='k')
stacked_fig.subplots_adjust(left=0.1,right=0.98,bottom=0.125,top=0.95,hspace = 0.25, wspace=0.25)
stacked_axs = stacked_axs.ravel()


#drawing plot of observed distributions of similarity between M and D delineated by D CST
CST_color_scheme = {'I':'#FE0308','III':'#FF7200','IV':'#221886','V':'#FAE50D'}
sns.boxplot(x="DaughterCST", y="YD", data=observed,whis=0.75,fliersize=0.0, palette=CST_color_scheme,ax=stacked_axs[0],orient='v',notch=True)
sns.swarmplot(x="DaughterCST", y="YD", data=observed,size=5, color="k", linewidth=0,ax=stacked_axs[0],orient='v')
stacked_axs[0].set_axisbelow(True)
stacked_axs[0].yaxis.grid(True)
stacked_axs[0].set_ylim(0,1)
stacked_axs[0].set_ylabel("Similarity (Yue-Clayton)",fontsize=20) 
stacked_axs[0].set_xticklabels(['I','III','IV','V'],fontsize=16)
stacked_axs[0].set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
stacked_axs[0].set_yticklabels([0.0,0.2,0.4,0.6,0.8,1.0],fontsize=16)
stacked_axs[0].set_xlabel("Daughter CST",fontsize=20)

#summarizing the permutation data as a histogram with 10 bins between 0 and 1, summarizing observed data in the same way
def column_2_hist(column):
    counts = pd.cut(column,bins=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],labels=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5],ordered=True).value_counts()
    return counts

perm_sum = pd.DataFrame()
col_count = 0
for column in permutations:

    perm_sum[col_count] = column_2_hist(permutations[column])
    col_count+=1

perm_sum = perm_sum.sort_index(ascending=True).T
mean = perm_sum.mean()
perc10 = perm_sum.quantile(0.025)
perc90 = perm_sum.quantile(0.975)

observed_hist = column_2_hist(observed['YD']).sort_index(ascending=True)

perm_stats = pd.concat([mean,perc10,perc90],axis=1)
perm_stats.columns = ['mean','perc10','perc90']
#perm_stats['Conf95'] = perm_stats['sem']*1.96

perm_stats['Observed'] = observed_hist
#plotting the summarized data

points1 = stacked_axs[1].scatter(x=perm_stats.index,y=perm_stats['mean'],c="#000000",s=45,zorder=2)
point2 = stacked_axs[1].scatter(x=perm_stats.index,y=perm_stats['Observed'],c="#fcda3f",s=120,marker="*",zorder=3)
stacked_axs[1].set_axisbelow(True)
stacked_axs[1].yaxis.grid(True,zorder=0)
stacked_axs[1].vlines(x=perm_stats.index,ymin=perm_stats['perc10'],ymax=perm_stats['perc90'],colors='#000000',linewidth=2.0,zorder=2)
stacked_axs[1].set_ylim(0,22)
stacked_axs[1].set_ylabel("Mother-Daughter Pairs",fontsize=20) 
stacked_axs[1].set_xticks([0,1,2,3,4,5,6,7,8,9,10])
stacked_axs[1].set_xticklabels([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],fontsize=16)
stacked_axs[1].set_yticks([0,4,8,12,16,20])
stacked_axs[1].set_yticklabels([0,4,8,12,16,20],fontsize=16)
stacked_axs[1].set_xlabel("Similarity (Yue-Clayton)",fontsize=20)

#output
stacked_axs[0].text(-1.2,1,s="A",fontsize=30,clip_on=False,ha="left")
stacked_axs[1].text(-2,22,s="B",fontsize=30,clip_on=False,ha="left")

stacked_axs[1].legend(handles=[points1,point2],labels=['Ave 100 Perm.','Observed'],loc=[0.525,0.78],fontsize=16,handletextpad=-0.4,scatteryoffsets=[0.5,0.5],frameon=False)

stacked_fig.savefig("MMOTH_observed_YD.pdf")