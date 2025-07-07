import pandas as pd
import os

input_folder = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(input_folder, "significant_hits")
os.makedirs(output_folder, exist_ok=True)

populations = ["JM", "JR", "RW", "ML"]

for pop in populations:
    input_file = os.path.join(input_folder, f"{pop}_merged_norm_output_sorted_abs.txt")
    if not os.path.isfile(input_file):
        print(f"⚠️ Missing input file: {input_file}")
        continue

    try:

        df = pd.read_csv(input_file, sep='\t', header=None)
        num_cols = df.shape[1]

        if num_cols == 8:
            df.columns = ["chromosome", "snp_id", "unknown1", "position", "freq1", "freq2", "ihs_raw", "|IHS|"]
        elif num_cols == 9:
            df.columns = ["chromosome", "snp_id", "unknown1", "position", "freq1", "freq2", "ihs_raw", "|IHS|", "extra"]
        else:
            raise ValueError(f"{pop}: Unexpected number of columns ({num_cols})")

        mean_ihs = df["|IHS|"].mean()
        std_ihs = df["|IHS|"].std()
        threshold = mean_ihs + 3 * std_ihs

        significant_hits = df[df["|IHS|"] > threshold]

        output_file = os.path.join(output_folder, f"{pop}_ihs_above_threshold.txt")
        significant_hits.to_csv(output_file, sep='\t', index=False)

        print(f"✅ Saved significant iHS hits for {pop} to {output_file}")

    except Exception as e:
        print(f"❌ Error processing {pop}: {e}")

print("✅ Done filtering all populations.")
