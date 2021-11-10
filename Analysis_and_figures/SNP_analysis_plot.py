#!/usr/bin/env python3

#importing packages to be used
import pandas as pd
import numpy as np
import sys
import seaborn as sns
import  matplotlib.pyplot as plt
from scipy import stats
import matplotlib.patches as mpatches

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})

snp_data = pd.read_csv("MMOTH_recentTrans_SNPs.csv",sep=",")

stacked_fig, stacked_axs = plt.subplots(1,1, figsize=(6,6), facecolor='w', edgecolor='k')
stacked_fig.subplots_adjust(left=0.175,right=0.98,bottom=0.125,top=0.95,hspace = 0.25, wspace=0.25)

Match_color_scheme = {'Match':'#6fbd84','NoMatch':'#999999'}

sns.boxplot(x="Same_family", y="SNPs_per_Mb", data=snp_data,whis=0.75,fliersize=0.0, palette=Match_color_scheme,ax=stacked_axs,orient='v',notch=True)
sns.swarmplot(x="Same_family", y="SNPs_per_Mb", data=snp_data,size=5, color="k", linewidth=0,ax=stacked_axs,orient='v')
stacked_axs.set_axisbelow(True)
stacked_axs.yaxis.grid(True)
stacked_axs.set_ylim(0,1100)
stacked_axs.set_ylabel("No. SNPs per Mbp",fontsize=20) 
stacked_axs.set_xticklabels(['Same\nFamily','Different\nFamily'],fontsize=16)
stacked_axs.set_yticks([0,200,400,600,800,1000])
stacked_axs.set_yticklabels([0,200,400,600,800,1000],fontsize=16)
stacked_axs.set_xlabel("",fontsize=20)

stacked_fig.savefig("MMOTH_recTrans_SNPs.pdf")
