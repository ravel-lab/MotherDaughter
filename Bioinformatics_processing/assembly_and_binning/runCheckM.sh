#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=8G -P jravel-lab -q threaded.q -pe thread 8 -N MD_checkm -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-1

infile=`sed -n -e "$SGE_TASK_ID p" Liners_folder.txt`

source /usr/local/packages/usepackage/share/usepackage/use.bsh

use python-2.7
which checkm

cd /local/groupshare/ravel/mfrance/MMOTH/06_mags/Liners

checkm lineage_wf -t 8 -x .fa --tab_table -f $Liners_bin_stats.tsv  Liners_bins Liners_bins/checkm
