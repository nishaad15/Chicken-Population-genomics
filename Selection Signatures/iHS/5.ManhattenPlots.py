import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

input_folder = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(input_folder, "plots")
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
            raise ValueError(f"Expected 8 or 9 columns, found {num_cols}")

    except Exception as e:
        print(f"❌ Failed to load {input_file}: {e}")
        continue

    chromosome_positions = {chrom: idx for idx, chrom in enumerate(sorted(df["chromosome"].unique()))}
    df["chromosome_position"] = df["chromosome"].map(chromosome_positions)

    mean_ihs_abs = df["|IHS|"].mean()
    std_ihs_abs = df["|IHS|"].std()
    print(mean_ihs_abs)
    print(std_ihs_abs)
    color_palette = sns.color_palette("husl", n_colors=len(chromosome_positions))

    plt.figure(figsize=(14, 6))
    x_positions = np.linspace(0, len(chromosome_positions) - 1, len(chromosome_positions))

    for chrom, group in df.groupby("chromosome"):
        idx = chromosome_positions[chrom]
        jittered_x = x_positions[idx] + np.random.uniform(-0.2, 0.2, size=len(group))
        plt.scatter(jittered_x, group["|IHS|"], color=color_palette[idx], s=8, alpha=0.7)

    threshold_upper = mean_ihs_abs + 3 * std_ihs_abs
    plt.axhline(y=threshold_upper, color='red', linestyle='--', label='3 SD above mean')

    plt.xlabel("Chromosome")
    plt.ylabel("|iHS| Value")
    plt.title(f"Manhattan Plot of |iHS| for {pop}")
    plt.xticks(x_positions, list(chromosome_positions.keys()))
    plt.tick_params(axis='x', which='both', bottom=False, top=False)
    plt.ylim(bottom=0)
    plt.tight_layout()

    output_path = os.path.join(output_folder, f"{pop}_manhattan_plot_ihs_abs.png")
    plt.savefig(output_path, dpi=600)
    plt.close()

    print(f"✅ Saved Manhattan plot for {pop} at: {output_path}")

print("✅ All Manhattan plots generated.")
