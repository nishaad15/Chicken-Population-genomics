import os

folder_path = os.path.dirname(os.path.abspath(__file__))

populations = ["JM", "JR", "RW", "ML"]

for pop in populations:
    input_file = os.path.join(folder_path, f"{pop}_merged_norm_output.txt")
    output_file = os.path.join(folder_path, f"{pop}_merged_norm_output_sorted_abs.txt")

    if not os.path.isfile(input_file):
        print(f"⚠️ File not found: {input_file}")
        continue

    merged_data = []

    with open(input_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            columns = line.strip().split('\t')
            if len(columns) >= 8:
                try:
                    columns[7] = str(abs(float(columns[7])))  
                    modified_line = '\t'.join(columns)
                    merged_data.append(modified_line + '\n')
                except ValueError:
                    print(f"⚠️ Could not convert to float: {columns[7]} in file {input_file}")

    sorted_data = sorted(merged_data, key=lambda x: int(x.split('\t')[0]))

    with open(output_file, "w") as out_file:
        out_file.writelines(sorted_data)

    print(f"✅ Processed and saved: {output_file}")

print("✅ All populations processed: sorted and absolute values updated.")
