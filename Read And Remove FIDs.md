# PLINK: Remove Individuals by FAM ID





Ensure you have the following PLINK binary files:
- `pop.fam`
- `pop.bim`
- `pop.bed`

---

## 1. Count the number of individuals per FAM ID in a `.fam` file.

Use this Python snippet to count how many individuals belong to each FAM ID:

```python
from collections import Counter

def count_fam_ids(fam_file):
    with open(fam_file, 'r') as f:
        lines = f.readlines()

    fam_ids = [line.strip().split()[0] for line in lines]  # FID = column 1
    fam_counts = Counter(fam_ids)

    for fid, count in fam_counts.items():
        print(f"FAM ID: {fid}, Count: {count}")

# Example
count_fam_ids("pop.fam")
```
## 2. Create a removal list of individuals with specific FAM IDs.
```python
def write_multiple_fid_removals(fam_file, fid_list, output_file):
    """Writes FID IID pairs to output_file for PLINK --remove"""
    with open(fam_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as out:
        for line in lines:
            parts = line.strip().split()
            fid, iid = parts[0], parts[1]
            if fid in fid_list:
                out.write(f"{fid} {iid}\n")

# Example usage
fids_to_remove = ["FAM123", "FAM456", "FAM789"]
write_multiple_fid_removals("pop.fam", fids_to_remove, "remove_list.txt")
```
## 3. Use PLINK to generate a new binary dataset excluding those individuals.
```bash
plink --bfile pop --remove remove_list.txt --make-bed --out pop_filtered --chr-set 40
