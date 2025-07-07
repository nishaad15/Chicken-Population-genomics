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
