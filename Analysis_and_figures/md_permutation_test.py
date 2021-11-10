#!/usr/bin/env python3

#importing packages to be used
import pandas as pd
import numpy as np
import sys
import seaborn as sns
import  matplotlib.pyplot as plt
from scipy import stats


#removing the annoying warning that pandas has for some reason
pd.options.mode.chained_assignment = None  # default='warn'

def yue_distance(mother, daughter):
    #creating a counting variable to index the median list
    taxon_count = 0    
    #creating lists to iterativly store output
    p_times_q = []
    p_minus_q_sq = []    
    #looping through the row and calculating product and difference squared between row data and median data
    for comp_abund in mother:
        #calculate p * q
        p_times_q.append(daughter[taxon_count]*comp_abund)
        #calculate p-q squared
        p_minus_q_sq.append((daughter[taxon_count]-comp_abund)**2)
        taxon_count += 1    
    #calculate sum p* q
    product = np.nansum(p_times_q)   
    #calculate sum p-q squared
    diff_sq = np.nansum(p_minus_q_sq)
    #calculate yue_med_dist
    yue_daughter_dist = product / (diff_sq + product)
    return yue_daughter_dist

def calculate_md_dist(data_all,family_list):

    md_dist_df = pd.DataFrame(columns=['Mother','Daughter','YD'])

    row_count = 0

    for family in family_list:

        family_data=data_all[data_all['family_id']==family]

        daughter_data = family_data[family_data['moda_id']=='D']
        mother_data = family_data[family_data['moda_id']=='M']
        mother_rel = mother_data[mother_data.columns[18:]].iloc[0]
        mother_id = mother_data[mother_data.columns[4]].iloc[0]
        
        for daughter in daughter_data.iterrows():

            daughter_rel = daughter[1][18:]
            daughter_id = daughter[1][4]

            yd = yue_distance(mother_rel,daughter_rel)

            md_dist_df.loc[row_count] = [mother_id,daughter_id,yd]
            row_count+=1

    return(md_dist_df)



#reading in all the mother daughter data
data_all = pd.read_csv('mdpairs_data.csv',sep=",")

#converting the read count data to relative abundance data
data_meta = data_all[data_all.columns[0:18]]
data_micro = data_all[data_all.columns[18:]]

drop_samples = data_micro[data_micro.sum(axis=1)<500].index

data_micro = data_micro.drop(drop_samples,axis=0)
data_meta = data_meta.drop(drop_samples,axis=0)


study_wide_rel_taxa = data_micro.sum(axis=0)
study_wide_rel_taxa = study_wide_rel_taxa.div(study_wide_rel_taxa.sum())
drop_taxa = study_wide_rel_taxa[study_wide_rel_taxa<0.0001].index
data_micro = data_micro.drop(drop_taxa,axis=1)

low_count_families = ['8079','8084','8103','12001']

data_micro = data_micro[~data_meta['family_id'].isin(low_count_families)]
data_meta = data_meta[~data_meta['family_id'].isin(low_count_families)]

data_micro_rel = data_micro.div(data_micro.sum(axis=1),axis=0)

data_all = pd.concat([data_meta,data_micro_rel],axis=1)

families = list(set(data_all['family_id']))

md_dist_df_OBSERVED = calculate_md_dist(data_all,families)


#######Permuting the daughter and mother dataset independently and randomly

mother_dataset = data_all[data_all['moda_id']=='M']
daughter_dataset = data_all[data_all['moda_id']=='D']

mother_meta = mother_dataset[mother_dataset.columns[0:18]].reset_index(drop=True)
mother_micro = mother_dataset[mother_dataset.columns[18:]]
daughter_meta = daughter_dataset[daughter_dataset.columns[0:18]].reset_index(drop=True)
daughter_micro = daughter_dataset[daughter_dataset.columns[18:]]

permutation_rep = 0

md_dist_df_PERM = pd.DataFrame()
while permutation_rep < 100:

    mother_rand = mother_micro.sample(frac=1,replace=False,axis=0).reset_index(drop=True)
    daughter_rand = daughter_micro.sample(frac=1,replace=False,axis=0).reset_index(drop=True)
    mother_rand = pd.concat([mother_meta,mother_rand],axis=1,ignore_index=True)
    daughter_rand = pd.concat([daughter_meta,daughter_rand],axis=1,ignore_index=True)

    data_rand = pd.concat([mother_rand,daughter_rand],axis=0)
    data_rand.columns = data_all.columns

    md_dist_df_PERMrep = calculate_md_dist(data_rand,families)
    md_dist_df_PERM[permutation_rep] = md_dist_df_PERMrep['YD'].values

    permutation_rep +=1

md_dist_df_PERM.to_csv('md_perm_test_PERMs.csv',sep=",",index=None)
md_dist_df_OBSERVED.to_csv('md_perm_test_OBSERVED.csv',sep=",",index=None)