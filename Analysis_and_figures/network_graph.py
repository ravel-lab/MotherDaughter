#!/usr/bin/python3

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

network_data = pd.read_csv("MMOTH_recent_trans999.csv",sep=",")

stacked_fig, stacked_axs = plt.subplots(1,1, figsize=(10,10), facecolor='w', edgecolor='k')
stacked_fig.subplots_adjust(left=0.1,right=0.9,bottom=0.1,top=0.9,hspace = 0.4, wspace=0.4)

G=nx.from_pandas_edgelist(network_data, 'DB', 'Reads')

nx.draw_spring(G, with_labels=True,ax=stacked_axs)

stacked_fig.savefig("MMOTH_recent_trans.pdf")