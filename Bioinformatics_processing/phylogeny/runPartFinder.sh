#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=32G -P jravel-lab -q threaded.q -pe thread 16 -N PartFinder -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

source /home/mfrance/software/PartitionFinder/venv/bin/activate

cd /local/scratch/mfrance/MMOTH/09_phylogeny

python /home/mfrance/software/PartitionFinder/partitionfinder-2.1.1/PartitionFinderProtein.py /local/scratch/mfrance/MMOTH/09_phylogeny/ --raxml --rcluster-max 1000 -p 16 -q
