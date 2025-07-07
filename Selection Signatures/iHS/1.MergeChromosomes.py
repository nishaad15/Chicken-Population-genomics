import os

parent_folder = os.path.dirname(os.path.abspath(__file__))

populations = ["JM", "JR", "RW", "ML"]

for pop in populations:
    pop_folder = os.path.join(parent_folder, pop)
    if not os.path.isdir(pop_folder):
        print(f"Skipping missing folder: {pop_folder}")
        continue

    chromosome_data = {f"Chromosome {i}": [] for i in range(1, 30)}

    for file_name in os.listdir(pop_folder):
        if file_name.endswith(".norm"):
            try:
                chromosome_number = int(file_name.split('_chr')[1].split('_')[0])
            except (IndexError, ValueError):
                print(f"Skipping improperly named file: {file_name}")
                continue

            file_path = os.path.join(pop_folder, file_name)
            with open(file_path, "r") as file:
                lines = file.readlines()
                chromosome_data[f"Chromosome {chromosome_number}"].extend(lines)

    merged_file_name = f"{pop}_merged.norm"
    merged_file_path = os.path.join(parent_folder, merged_file_name)
    with open(merged_file_path, "w") as merged_file:
        for chrom, data_lines in chromosome_data.items():
            merged_file.writelines(data_lines)

    print(f"✅ Merged file created for {pop}: {merged_file_path}")
