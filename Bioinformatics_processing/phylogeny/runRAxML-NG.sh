#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=64G -P jravel-lab -q threaded.q -pe thread 16 -N RAxML_MMOTH -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

export LD_LIBRARY_PATH=/usr/local/packages/gcc-9.3.0/lib64:$LD_LIBRARY_PATH

cd /local/scratch/mfrance/MMOTH/09_phylogeny

#/usr/local/packages/raxml-ng-1.0.1mpi/bin/raxml-ng-mpi --bootstrap --msa /local/scratch/mfrance/Gvaginalis_genomics/concat_speedier/nucl_concat.phy --msa-format PHYLIP --data-type DNA --prefix BS2 --seed 2 --model /local/scratch/mfrance/Gvaginalis_genomics/concat_speedier/raxml_partition_scheme.txt --threads 50 --workers 10 --bs-trees 200

#/usr/local/packages/raxml-ng-1.0.1mpi/bin/raxml-ng-mpi --bsconverge --bs-trees Gvag_nucl_concat.combined.bootstraps --prefix bs425 --seed 123456 --threads 8  --bs-cutoff 0.01

#/usr/local/packages/raxml-ng-1.0.1mpi/bin/raxml-ng-mpi --support --tree Gvag_nucl_concat.raxml.lastTree.TMP --bs-trees Gvag_nucl_concat.combined.bootstraps --prefix Gvag_nucl_concat --threads 8 --bs-metric fbp,tbe 

/usr/local/packages/raxml-ng-1.0.1mpi/bin/raxml-ng-mpi --all --msa /local/scratch/mfrance/MMOTH/09_phylogeny/MMOTH_all.phy -msa-format PHYLIP --data-type AA -prefix MMOTH_mags --seed 2 --model /local/scratch/mfrance/MMOTH/09_phylogeny/MMOTH_partition.txt --tree pars{10},rand{10} --thread 16 --workers 8 --bs-trees autoMRE
