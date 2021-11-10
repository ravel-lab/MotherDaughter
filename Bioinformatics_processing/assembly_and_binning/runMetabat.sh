#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=8G -P jravel-lab -q threaded.q -pe 8 -N MD_bat -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-47

infile=`sed -n -e "$SGE_TASK_ID p" MD_barcodes_all.txt`

cd /local/scratch/mfrance/MMOTH/mapping
seq_dir=/local/groupshare/ravel/mfrance/MMOTH/02_preprocess/1_fastq_pe
output_dir=/loca/scratch/mfrance/MMOTH/mapping
contig_dir=/local/groupshare/ravel/mfrance/MMOTH/04_assembly/metaspades/assembled_contigs

source /usr/local/packages/usepackage/share/usepackage/use.bsh

bowtie2-build $contig_dir/${infile}.contigs.fasta $output_dir/${infile}
bowtie2 -x $output_dir/${infile} -1 $seq_dir/${infile}.R1.fq -2 $seq_dir/${infile}.R2.fq -U $seq_dir/${infile}.unpaired.fq -S $output_dir/${infile}.sam

samtools faidx $ouput_dir/${infile}.sam
samtools view -bt $output_dir/${infile}.fai $output_dir/${infile}.sam > $output_dir/${infile}.bam
samtools sort -o $output_dir/${infile}_s.bam -T $output_dir/${infile}-TEMP $output_dir/${infile}.bam 
samtools index $output_dir/${infile}_s.bam

rm $output_dir/${infile}.sam

java -jar /usr/local/packages/picard-2.18.7/picard.jar MarkDuplicates \
I=$output_dir/${infile}_s.bam \
O=$output_dir/${infile}_smd.bam \
VALIDATION_STRINGENCY=LENIENT \
METRICS_FILE=$output_dir/${infile}.md.metrics.txt \
REMOVE_DUPLICATES=TRUE

samtools sort -o $output_dir/${infile}_smds.bam -T $output_dir/${infile}_md-TEMP $output_dir/${infile}_smd.bam
samtools index $output_dir${infile}_smds.bam

/local/projects/M8910/software/metabat-2.10.2/runMetaBat.sh -o ${infile} $contig_dir/${infile}.contigs.fasta $output_dir/${infile}_smds.bam
