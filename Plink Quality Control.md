# PLINK Processing Pipeline

This section includes conversion of VCFs to PLINK format, filtering SNPs and individuals, LD pruning, and removal of indels. All commands are grouped into one code block for easy copy-paste execution.

---

## Steps

1. **Convert VCF to PLINK binary format**  
2. **Apply filtering: MAF ≥ 0.05, mind ≤ 0.1**  
3. **Perform LD pruning (r² threshold = 0.2)**  
4. **Remove indels and retain only A/C/G/T SNPs**
5. **Rename the .fam file for standardizing the population names and Individual IDs**
---

```bash
plink --vcf Merged_SNPs.geno05.vcf.gz --make-bed --double-id --allow-extra-chr --chr-set 95 --out Merged_SNPs.geno05

plink --bfile Merged_SNPs.geno05 --maf 0.05 --mind 0.1 --make-bed --double-id --allow-extra-chr --chr-set 95 --out filtered_snps

plink --bfile filtered_snps --indep-pairwise 50 5 0.2 --chr-set 35 --out filtered_snps.pruned

plink --bfile final_merged --snps-only just-acgt --make-bed --out final_merged_noindels --chr-set 40
