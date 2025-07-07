# SNP Extraction and ADMIXTURE Analysis Pipeline

This section covers SNP renaming by `chr:pos`, isolating 408 AIMs (Ancestry Informative Markers), extracting them using PLINK, and running ADMIXTURE analysis with PONG visualization.

---

## Steps

1. **Rename SNPs to `chr:pos` format** in `.bim` file  
2. **Prepare a list of SNP IDs (`chr:pos`)** to extract  
3. **Extract selected SNPs using PLINK**  
4. **Run ADMIXTURE across K = 1 to 23**  
5. **Ensure `.fam` population labels are fixed** in PLINK files  
6. **Run PONG** for ADMIXTURE visualization

---

```bash
awk '{$2 = $1 ":" $4; print}' OFS='\t' final_merged_noindels.bim > final_merged_noindels_chrpos.bim

awk '{print $1 ":" $2}' chrpos.txt > snp_ids_to_extract.txt

plink --bfile final_merged_noindels_chrpos \
      --extract snp_ids_to_extract.txt \
      --make-bed \
      --out extracted_snps \
      --chr-set 40

for K in {1..23}; do
    admixture --cv final_merged_noindels_chrpos.bed $K | tee log${K}.out
done

pong -m pong_filemap.txt -i ind2pop[1].txt -n pop_order_expandednames.txt
