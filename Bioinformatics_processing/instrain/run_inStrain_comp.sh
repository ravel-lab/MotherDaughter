#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=64G -P jravel-lab -q threaded.q -pe thread 8 -N inStrain_comp -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed

#setting the number of jobs to be executed
#$ -t 2-47

cd /local/scratch/mfrance/MMOTH/08_inStrain

infile=`sed -n -e "$SGE_TASK_ID p" MMOTH.lst`

source /usr/local/packages/usepackage/share/usepackage/use.bsh
use python-3.5

source /home/mfrance/software/inStrain/.venv/bin/activate
source /home/mfrance/.bashrc

cd $infile

map_dir=/local/scratch/mfrance/MMOTH/07_mapping

inStrain compare -i MG_* -p 8 -s $map_dir/magKeys/${infile}.txt --clusterAlg ward -o Compare_${infile}
