# Chicken SNP VCF Normalization and Filtering Pipeline

This pipeline processes VCF files by normalizing, renaming chromosomes, merging datasets, and filtering SNPs based on genotype completeness using `bcftools`.

---

## Assuming you have
vcf files(with snps only) to merge have chromosome no. as integers-1 2 3... and.fa reference does not have chr no. as integer

---


**1)Rename chromosomes in the FASTA file** using a mapping file (`rename_fasta_headers.txt`) to remove `chr` prefixes or convert to integers for compatibility.


```bash
awk 'BEGIN {
  while ((getline < "rename_fasta_headers.txt") > 0) {
    map[$1] = $2
  }
}
{
  if ($0 ~ /^>/) {
    gsub(/^>/, "", $0)
    if ($0 in map) {
      print ">" map[$0]
    } else {
      print ">" $0
    }
  } else {
    print $0
  }
}' galGal4.fa > galGal4_renamed.fa
```
---
**2)Normalize the VCF again**, now using the renamed FASTA. If the reference mismatches cause errors, allow mismatches using `--check-ref x`.

```bash
nohup bcftools norm -f galGal4_renamed.fa -O z -o Global_chicken_snps_only.norm.vcf.gz Global_chicken_snps_only.vcf.gz > norm_global.log 2>&1 &
nohup bcftools norm -f galGal4_renamed.fa --check-ref x -O z -o Global_chicken_snps_only.norm.vcf.gz Global_chicken_snps_only.vcf.gz > norm_global.log 2>&1 &
```
---
**3)Merge the global and local VCFs** into a single file for joint analysis.


```bash
nohup bcftools merge -m all -O z -o Merged_SNPs.vcf.gz Global_chicken_snps_only.norm.vcf.gz local.norm.vcf.gz > merge_bcftools.log 2>&1 &
```

---
**4)Fill in the missingness statistics (F_MISSING)** and apply a filter to retain SNPs with <5% missing data.
---
```bash
nohup bcftools +fill-tags Merged_SNPs.vcf.gz -Oz -o merged.filled.vcf.gz -- -t F_MISSING > fill_tags.log 2>&1 &
nohup bcftools view -i 'INFO/F_MISSING<0.05' merged.filled.vcf.gz -O z -o Merged_SNPs.geno05.vcf.gz > filter_geno.log 2>&1 &
```
---
**5)Count the number of SNPs** that remain after filtering.

```bash
bcftools view -H Merged_SNPs.geno05.vcf.gz | wc -l
```
---
