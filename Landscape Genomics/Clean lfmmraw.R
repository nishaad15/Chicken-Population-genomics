geno <- read.table("geno_lfmm.raw", header = TRUE)
geno_matrix <- as.matrix(geno[, 7:ncol(geno)]) 
write.table(geno_matrix, "geno.lfmm", row.names = FALSE, col.names = FALSE)
