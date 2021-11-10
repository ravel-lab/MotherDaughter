#!/usr/bin/env python3

#importing packages to be used
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
import sys
import matplotlib
import seaborn as sns
import random
import matplotlib.patches as mpatches


#taxa color dictionary
taxa_color_scheme = {'Lactobacillus_crispatus':'#ff0000','Gardnerella_vaginalis':'#20b2aa','g_Lactobacillus':'#eef06c',
                     'Lactobacillus_iners':'#ff8c00','Lactobacillus_gasseri':'#7fff00','Lactobacillus_jensenii':'#333333',
                     'Enterococcus_faecalis':'#bbffff','Raoultella_planticola':'#ffc2ff','g_Peptoniphilus':'#CCCC00',
                     'Sneathia_sanguinegens':'#c7aa8f','Atopobium_vaginae':'#0000cd','g_Atopobium':'#0000cd',
                     'Lacotbacillus_helveticus':'#00ccff','Mageeibacillus_indolicus':'#3cb371','g_Anaerococcus':'#87cefa','g_Gardnerella':'#20b2aa',
                     'Megasphaera_genomosp.':'#0000ff','Streptococcus_agalactiae':'#ff738a','g_Megasphaera':'#008B45',
                     'Streptococcus_oralis':'#ff66ff','Prevotella_bivia':'#bfbfbf','Aerococcus_christensenii':'#bebebe',
                     'Anaerococcus_tetradius':'#87cefa','g_Gemella':'#daa520','Prevotella_genogroup_1':'#b0b0b0','Prevotella_disiens':'#9bbade',
                     'Lactobacillus_vaginalis':'#ffffff','other':'#808080','Bifidobacterium_longum':'#c1ffc1','Prevotella_buccalis':'#debdff',
                     'Bifidobacterium_breve':'#c1ffc1','Eggerthella':'#DE7710','Mycoplasma_hominis':'#10DE4E',
                     'Porphyromonas_uenonis':'#DE4310','Eubacterium_saphenum':'#8F10DE','Fusobacterium_nucleatum':'#CD853F',
                     'Fusobacterium_gonidiaformans':'#CD853F','Streptococcus_anginosus':'#ffc0cb','Peptostreptococcus_anaerobius':'#DEDB10',
                     'Arcanobacterium_phocae':'#8c10de','Bacteroides_uniformis':'#de1058','Ureaplasma_parvum':'#9999ff','Prevotella_corporis':'#ad8bab',
                     'Peptoniphilus_harei':'#CCCC00','Mobiluncus_mulieris':'#f08080','Megasphaera_sp._type_2':'#008B45',
                     'BVAB1':'#b31900','BVAB2':'#3bb16f','g_Escherichia.Shigella':'#12456b','Peptoniphilus_lacrimalis':'#803849',
                     'Veillonella_montpellierensis':'#ff8c69','Prevotella_genogroup_3':'#b36200','Parvimonas_micra':'#cdcd00',
                     'Corynebacterium_accolens':'#ffff00','Finegoldia_magna':'#800080','Prevotella_genogroup_2':'#b0b0b0','Propionibacterium':'#5f7362',
                     'Staphylococcus_epidermidis':'#ffffff','Prevotella_timonensis':'#f8fca9','g_Streptococcus':'#ffc0cb','g_Bifidobacterium':'#c1ffc1','g_Enterococcus':'#bbffff'
                     ,'g_Staphylococcus':'#800080','g_Finegoldia':'#800080','g_Prevotella':'#ffd9b3','g_Sneathia':'#d1e8eb','g_Aerococcus':'#e8e1ba'
                     ,'g_Leptotrichia':'#7ca386','g_Veillonella':'#499996','g_Dialister':'#997dbd','g_Corynebacterium_1':'#ffff00'
                     ,'g_Varibaculum':'#094717','g_Delftia':'#090c47','g_Corynebacterium_1':'#ffff00','Prevotella_amnii':'#ac8fc7','Sneathia_amnii':'#6963ff'}

def get_color(taxa):

    chars = '0123456789ABCDEF'

    if taxa in taxa_color_scheme:
        
        taxa_color = taxa_color_scheme[taxa]

    else:
        taxa_color_scheme[taxa] = '#'+''.join(random.sample(chars,6))
        taxa_color = taxa_color_scheme[taxa]

    return taxa_color


matplotlib.rc('font', serif='Helvetica Neue')
matplotlib.rc('text', usetex=True)

data_all = pd.read_csv("mdpairs_data.csv")

data_meta = data_all[data_all.columns[0:19]]
data_micro = data_all[data_all.columns[19:]]

study_wide_rel_taxa = data_micro.sum(axis=0)
study_wide_rel_taxa = study_wide_rel_taxa.div(study_wide_rel_taxa.sum())
drop_taxa = study_wide_rel_taxa[study_wide_rel_taxa<0.0001].index
data_micro = data_micro.drop(drop_taxa,axis=1)
top_columns = data_micro.sum(axis=0).sort_values(ascending=False).head(19).index

data_micro_rel = data_micro.div(data_micro.sum(axis=1),axis=0)

data_all = pd.concat([data_meta,data_micro_rel],axis=1)

families = list(set(data_all['reorder']))

#setting up the plot to be a 6x8 matrix 
stacked_fig, stacked_axs = plt.subplots(9,5, figsize=(19,16), facecolor='w', edgecolor='k')
stacked_fig.subplots_adjust(left=0.04,right=0.96,bottom=0.04,top=0.96,hspace=0.5, wspace=0.3)

stacked_axs = stacked_axs.ravel()


bar_width = 0.5
plot_count=0
legend_entries = {}

#creating a list of the family ids
mg_color_dict = {1: '#000000', 0: '#ffffff'}

for family_id in families:

    print(family_id)
        
    #subsetting the data to just have this subject
    data_sub_rel = data_all.loc[data_all['reorder'] == family_id]

    data_sub_micro = data_sub_rel[data_sub_rel.columns[19:]]

    #subsetting the dataframe to only include the columns with the top 15 summed relative abundance for the subject's data

    data_sub_micro = data_sub_micro[top_columns]

    data_sub_micro['other'] = data_sub_micro.apply(lambda row: 1.0 - row.sum(), axis=1)

    data_sub_rel = pd.concat([data_sub_rel[data_sub_rel.columns[0:19]],data_sub_micro],axis=1,sort=False)

    data_sub_rel['bottom_count'] = pd.Series([0.0 for x in range(len(data_sub_rel.index))], index=data_sub_rel.index)

    for taxa in range(19,39):

        taxa = data_sub_rel.columns[taxa]

        taxa_color = get_color(taxa)

        if taxa not in legend_entries:

            legend_entries[taxa] = taxa_color_scheme[taxa]
        
        stacked_axs[plot_count].barh(data_sub_rel['x_bar'],data_sub_rel[taxa],height=bar_width,left=data_sub_rel['bottom_count'],color=taxa_color,clip_on=False)
        
        data_sub_rel['bottom_count'] = data_sub_rel['bottom_count'] + data_sub_rel[taxa]

    stacked_axs[plot_count].set_xticks([0.0,0.2,0.4,0.6,0.8,1.0], minor=False)
    stacked_axs[plot_count].set_xlim(0,1)
    stacked_axs[plot_count].set_xticklabels(['0.0','0.2','0.4','0.6','0.8','1.0'],minor=False,fontsize=16)

    #if plot_count in [0,1,2,3,4]:
    #    stacked_axs[plot_count].set_xlabel('Relative abundance',fontsize=16)

    stacked_axs[plot_count].set_yticks(data_sub_rel.x_bar.tolist())
    xlabs = data_sub_rel.moda_id.tolist()
    #xlabs = [w.replace('.0','') for w in xlabs]
    stacked_axs[plot_count].set_yticklabels(xlabs,fontsize=16)
    stacked_axs[plot_count].set_ylabel(family_id,fontsize=20,rotation=0,verticalalignment="center",ha='right',position=[0,0.5],clip_on=False)

    stacked_axs[plot_count].xaxis.grid(color='gray')
    stacked_axs[plot_count].set_axisbelow(True)
    for row in data_sub_rel.iterrows():
        row=row[1]
        stacked_axs[plot_count].plot([1.025],row["x_bar"],c=mg_color_dict[row['MG_selected']],clip_on=False,linestyle="",marker="d")

    plot_count += 1 

patch_list = []
for taxa in legend_entries:
    data_key = mpatches.Patch(color=legend_entries[taxa],label=taxa)
    patch_list.append(data_key)

for blank_plot in [42,43,44]:
    stacked_fig.delaxes(stacked_axs.flatten()[blank_plot])


taxa_labels = [r'\textit{G. vaginalis}',r'\textit{L. iners}',r'\textit{A. vaginae}',r'\textit{L. crispatus}',r'\textit{S. sanguinegens}',r'\textit{L. jensenii}',r'\textit{Ca.} L. vaginae',r'\textit{Corynebacterium}',r'\textit{Finegoldia}',r'BVAB2',r'\textit{Streptococcus}',r'\textit{P. timonensis}',r'\textit{Prevotella}',r'\textit{Bifidobacterium}',r'\textit{Coriobacteriaceae}',r'\textit{Anaerococcus}',r'\textit{Peptoniphilus}',r'\textit{Megasphaera}',r'\textit{P. bivia}',r'Other']

stacked_fig.legend(handles=patch_list,labels=taxa_labels,loc=(0.425,0.03),ncol=5,fontsize=17,columnspacing=1,handletextpad=0.5,handlelength=1.5)
stacked_fig.savefig('Figure1_MD_barcharts_all.pdf')

