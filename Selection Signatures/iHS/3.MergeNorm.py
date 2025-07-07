import os

parent_folder = os.path.dirname(os.path.abspath(__file__))

populations = ["JM", "JR", "RW", "ML"]

for pop in populations:
    pop_folder = os.path.join(parent_folder, pop)
    if not os.path.isdir(pop_folder):
        print(f"⚠️ Skipping missing folder: {pop_folder}")
        continue

    merged_data = []

    for file_name in os.listdir(pop_folder):
        if file_name.endswith(".norm"):
            file_path = os.path.join(pop_folder, file_name)
            with open(file_path, "r") as file:
                lines = file.readlines()
                merged_data.extend(lines)

    merged_output_file = os.path.join(parent_folder, f"{pop}_merged_norm_output.txt")
    with open(merged_output_file, "w") as merged_file:
        merged_file.writelines(merged_data)

    print(f"✅ Merged .norm files for {pop}: {merged_output_file}")
