#  Population-wise Phasing via Beagle and Selscan Pipeline

This section includes isolating individual populations from extracted SNPs, converting to VCF, phasing using Beagle, splitting by chromosome, and running iHS-based selection scans using selscan.

---

## Steps

1. **Isolate individual populations from `.fam` file**  
```bash
awk '$1 == "JM" {print $1, $2}' extracted_snps.fam > keep_JM.txt

for pop in JM JR RW ML; do
    plink --bfile extracted_snps \
          --keep keep_${pop}.txt \
          --make-bed \
          --out extracted_snps_${pop} \
          --chr-set 40
done
```
2. **Convert PLINK files to VCF for each population**
```bash
for pop in JM JR RW ML
do
    plink --bfile extracted_snps_"$pop" --recode vcf --chr-set 40 --out extracted_snps_"$pop"
done
```
3. **Phase each population’s VCF using Beagle**  
```bash
for pop in JM JR RW ML
do
    java -jar beagle.jar gt=extracted_snps_"$pop".vcf out=extracted_snps_"$pop"_phased nthreads=4
done
```
4. **Index the phased VCFs using Tabix**  
```bash
for pop in JM JR RW ML
do
    tabix -p vcf extracted_snps_"$pop"_phased.vcf.gz
done
```
5. **Split phased VCFs into chromosome-wise files**  
```bash
for pop in JM JR RW ML
do
    for chr in {1..39} 40
    do
        bcftools view -r $chr extracted_snps_${pop}_phased.vcf.gz -Oz -o ${pop}_chr${chr}.vcf.gz
        tabix -p vcf ${pop}_chr${chr}.vcf.gz
    done
done
```
6. **Run selscan (iHS) per chromosome**  
```bash
pops=("JM" "JR" "RW" "ML")

for pop in "${pops[@]}"
do
    for chr in {1..40}
    do
        vcf_file="${pop}_chr${chr}.vcf.gz"
        out_file="${pop}_chr${chr}_ihs"

        selscan --ihs --vcf "$vcf_file" --pmap --out "$out_file"
    done
done
```
7. **Normalize iHS scores using `norm`**
```bash
for pop in "${pops[@]}"
do
    for chr in {1..40}
    do
        ihs_file="${pop}_chr${chr}_ihs.ihs.out"

        if [[ -f "$ihs_file" ]]; then
            ./norm --ihs --files "$ihs_file"
        else
            echo "⚠️  File not found: $ihs_file"
        fi
    done
done
