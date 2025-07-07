import os

parent_folder = os.path.dirname(os.path.abspath(__file__))

populations = ["JM", "JR", "RW", "ML"]

for pop in populations:
    pop_folder = os.path.join(parent_folder, pop)
    if not os.path.isdir(pop_folder):
        print(f"⚠️ Skipping missing folder: {pop_folder}")
        continue

    for file_name in os.listdir(pop_folder):
        if file_name.endswith(".norm"):
            try:
                chromosome_number = int(file_name.split('_chr')[1].split('_')[0])
            except (IndexError, ValueError):
                print(f"⚠️ Skipping malformed file name: {file_name}")
                continue

            file_path = os.path.join(pop_folder, file_name)

            with open(file_path, "r") as f:
                lines = f.readlines()

            modified_lines = [f"{chromosome_number}\t{line}" for line in lines]

            with open(file_path, "w") as f:
                f.writelines(modified_lines)

            print(f"✅ Processed: {file_name}")

print("✅ Chromosome column addition completed for all .norm files.")
