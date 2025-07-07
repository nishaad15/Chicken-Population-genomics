Generate feature annotations:

```bash
python annotateIHS.py --anno imput.txt --gff reference.gff --output result.tsv
```

Parameters:
- `--anno`: Input file with genomic regions
- `--gff`: GFF file from NCBI
- `--output`: Output TSV file name

### 2. Visualization

Create feature distribution plot:

```bash
python3 visualiseFeatures.py --input input.txt --gff reference.gff --output result --trait "trait name" --dpi 600
```

## Outputs

1. **Feature Annotations** (`result.tsv`)
   - Tab-separated file containing genomic features
   - Includes features like: exon, CDS, gene, lnc_RNA, mRNA, tRNA

2. **Feature Distribution** 
   - Bar plot and Pie chart plot visualization
   - Shows distribution of different feature types
  
   - 
#  Post-Annotation Gene Filtering

This step filters the annotation result file to retain only **unique gene entries** where the feature type is `"gene"` 
---



1. **Keep only the first occurrence of each gene ID** where the feature is `"gene"` (column 4).
2. **Output a filtered TSV** with non-redundant gene-level annotations.

---

```bash
awk -F'\t' 'BEGIN { OFS=FS } $4 == "gene" && !seen[$5]++' JM_result.tsv > JM_genes_filtered.tsv
