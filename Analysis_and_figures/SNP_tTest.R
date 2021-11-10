setwd("~/Dropbox (IGS)/ravel_lab/mother_daughter/data_scripts/")

SNP_data <- read.csv("MMOTH_recentTrans_SNPs.csv",sep=",")

t.test(SNP_data$SNPs_per_Mb[SNP_data$Same_family=="Match"], SNP_data$SNPs_per_Mb[SNP_data$Same_family=="NoMatch"])

pairs_data <- read.csv("mdpairs_data.csv",sep=",")
daughter_data <- pairs_data[pairs_data$moda_id=="D",]
mother_data <- pairs_data[pairs_data$moda_id=="M",]
t.test(mother_data$age[mother_data$Shared==1], mother_data$age[mother_data$Shared==0])
