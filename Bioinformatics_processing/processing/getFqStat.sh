#!/bin/bash

# for X in *_1.fastq; do qsub -cwd -b y -l mem_free=4G -P jravel-lab -q threaded.q -pe thread 1 -N fqStat -V -o /local/scratch/bma/logs/ -e /local/scratch/bma/logs/ ./getFqStat.sh $X; done
# for X in *_1_tmp.fastq; do qsub -cwd -b y -l mem_free=4G -P jravel-lab -q threaded.q -pe thread 1 -N fqStat -V -o /local/scratch/bma/logs/ -e /local/scratch/bma/logs/ ./getFqStat.sh $X; done
# for X in *.se.fq; do qsub -cwd -b y -l mem_free=4G -P jravel-lab -q threaded.q -pe thread 1 -N fqStat -V -o /local/scratch/bma/logs/ -e /local/scratch/bma/logs/ ./getFqStat.sh $X; done
# for X in M?/*/*.gz; do qsub -cwd -b y -l mem_free=500M -P jravel-lab -q threaded.q -pe thread 1 -V -o /local/scratch/bma/logs/ -e /local/scratch/bma/logs/ ./getFqStat.sh $X; done

#echo -e "sample\ttotalBp\treadsInOne\treadsInPair\t"

## step 0: for delivered reads
#R1_basepairs R1_reads
#for x in *; do echo $x; done > lst
#for X in `cat lst2`; do cat $X/ILLUMINA_DATA/*_R1_stats.txt | awk -v name=$X '{base+=$2; reads+=$4}END{print name"\t"base"\t"reads}'; done > raw.stat

## step 1: for home-removed reads
# works on fastq.gz compressed file
## only check R1, because de human generated paired reads
input=$1
#for X in *_1.fastq; do qsub -cwd -b y -l mem_free=4G -P jravel-lab -q threaded.q -pe thread 1 -N fqStat -V -o /local/scratch/bma/logs/ -e /local/scratch/bma/logs/ ./getFqStat.sh $X; done
#file=`echo $X | cut -d'/' -f3 | sed 's/.fastq.gz//'`
file=`echo $input | cut -d'.' -f1`
cat $input | fastq-stats > $file.stat

#for X in *.stat; do name=`basename $X .stat`; cat $X | grep "^reads" | awk -F"\t" '{print $2}' | awk -v name=$name '{sum=+$1}END{print name"\t"sum}'; done > stat.txt
