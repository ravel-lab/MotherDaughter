#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=32G -P jravel-lab -q threaded.q -pe thread 16 -N blast -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-1

source /usr/local/packages/usepackage/share/usepackage/use.bsh

cd /local/scratch/mfrance/MMOTH/09_phylogency

#infile=`sed -n -e "$SGE_TASK_ID p" target.lst`

source /home/mfrance/.bashrc

blastp -evalue 0.00001 -num_threads 16 -query goodProteins.fasta -db MMOTH_mags -outfmt=6 -out MMOTH_allvall.txt
