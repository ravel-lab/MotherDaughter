#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=8G -P jravel-lab -q all.q -N hr_mmoth -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-47

infile=`sed -n -e "$SGE_TASK_ID p" MD_barcodes.txt`

raw_dir=/local/groupshare/ravel/mfrance/MMOTH/01_raw
human_genome_dir=/local/groupshare/ravel/mfrance/human_removal/source_hg38
out_dir=/local/scratch/mfrance/MMOTH/

zcat $raw_dir/source/${infile}_R1.fastq.gz > $out_dir/${infile}_R1.fq
zcat $raw_dir/source/${infile}_R2.fastq.gz > $out_dir/${infile}_R2.fq

#bmtagger.sh -b $human_genome_dir/GRch38_p12.bitmask -x $human_genome_dir/GRch38_p12.srprism -T /local/scratch/mfrance/hr/ -q 1 -1 $out_dir/${infile}_R1.fq -2 $out_dir/${infile}_R2.fq -X -o $raw_dir/human_removed/${infile}_de_human 
