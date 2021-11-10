#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=2G -P jravel-lab -q threaded.q -pe thread 1 -N binV -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-47

source /usr/local/packages/usepackage/share/usepackage/use.bsh

cd /local/groupshare/ravel/mfrance/MMOTH/05_binning/binV

use python-3.5

contig_dir=/local/groupshare/ravel/mfrance/MMOTH/04_assembly/metaspades/assembled_contigs

seq_dir=/local/groupshare/ravel/mfrance/MMOTH/02_preprocess/2_fastq_se/

ref_db=/local/projects-t2/M8910/VOG_demo/0_db

ref=$ref_db/VIRGO


infile=`sed -n -e "$SGE_TASK_ID p" MD_barcodes_all.txt`

bowtie-build $contig_dir/${infile}.contigs.fasta ${infile}

bowtie -p 4 -l 25 --fullref --chunkmbs 512 --best --strata -m 20 --mm $infile --suppress 2,4,5,6,7,8,9,10,11,12 $seq_dir/${infile}.se.fq.gz $infile.reads2contigs
bowtie -p 4 -l 25 --fullref --chunkmbs 512 --best --strata -m 20 --mm $ref --suppress 2,4,5,6,7,8,9,10,11,12 $seq_dir/${infile}.se.fq.gz $infile.reads2ref

python /home/mfrance/software/binV/binV.py ${infile} $contig_dir/${infile}/${infile}.contigs.fasta
python /home/mfrance/software/binV/binV_plot.py ${infile}_contig_info.txt ${infile}
