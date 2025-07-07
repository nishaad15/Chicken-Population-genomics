import os

# Input and output directories
input_dir = os.getcwd()
output_dir = os.path.join(input_dir, "bed_input_regions")
os.makedirs(output_dir, exist_ok=True)

# Populations
populations = ["JM", "JR", "RW", "ML"]

window = 25000

for pop in populations:
    input_file = os.path.join(input_dir, f"{pop}_ihs_above_threshold.txt")
    output_file = os.path.join(output_dir, f"{pop}_ihs_regions.txt")

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()[1:]  # Skip first (header) line
        outfile.write("CHR\tSTART\tEND\n")

        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                try:
                    chrom = parts[0]
                    pos = int(float(parts[2]))  # third column is position

                    start = max(0, pos - window)
                    end = pos + window

                    outfile.write(f"{chrom}\t{start}\t{end}\n")
                except ValueError:
                    continue  # skip lines with bad data

    print(f"✅ Created: {output_file}")

print("✅ All BED-style region files created.")


