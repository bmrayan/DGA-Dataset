

# ──────────────────────────── IMPORTS ────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# ──────────────────────────── PATHS ──────────────────────────────
data_path  = r"C:\Users\bmray\OneDrive - Texas A&M University at Qatar\Desktop\DGA WEBPAGE\DGA_Dataset_ Repo\FinalDataSet_DGA.xlsx"
output_dir = r"C:\Users\bmray\OneDrive - Texas A&M University at Qatar\Desktop\DGA WEBPAGE\DGA_Dataset_ Repo\FinalFigures1"
os.makedirs(output_dir, exist_ok=True)
summary_file = os.path.join(output_dir, "raw_data_analysis_summary.txt")

# ──────────────────────────── CONSTANTS ──────────────────────────
gas_cols  = ["Hydrogen (H2)", "Methane (CH4)", "Ethylene (C2H4)",
             "Ethane (C2H6)", "Acetylene (C2H2)"]
gas_names = ["H2", "CH4", "C2H4", "C2H6", "C2H2"]

# ──────────────────────────── STYLE ──────────────────────────────
plt.style.use("default")
sns.set_palette("husl")
plt.rcParams["figure.dpi"]  = 100
plt.rcParams["savefig.dpi"] = 300
# Font settings for bold and readable text
plt.rcParams["font.size"] = 14
plt.rcParams["axes.labelsize"] = 16
plt.rcParams["axes.titlesize"] = 18
plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14
plt.rcParams["legend.fontsize"] = 14
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# ──────────────────────────── HELPERS ────────────────────────────
def add_subplot_labels(axes, labels=None, loc="upper left",
                       offset=(-0.08, 0.05), **kwargs):
    """Add (a), (b)… labels to subplots."""
    if not isinstance(axes, (list, tuple, np.ndarray)):
        axes = [axes]
    if labels is None:
        labels = [f"({chr(97+i)})" for i in range(len(axes))]

    default_kw = dict(fontsize=14, fontweight="bold",
                      ha="center", va="center",
                      bbox=dict(boxstyle="round,pad=0.3",
                                facecolor="white", alpha=0.8,
                                edgecolor="black"),
                      zorder=1000)
    default_kw.update(kwargs)

    for ax, lab in zip(axes, labels):
        x_off, y_off = offset
        if   loc == "upper left":  (x, y) = (x_off, 1+y_off)
        elif loc == "upper right": (x, y) = (1+x_off, 1+y_off)
        elif loc == "lower left":  (x, y) = (x_off, y_off)
        elif loc == "lower right": (x, y) = (1+x_off, y_off)
        else:                      (x, y) = (x_off, 1+y_off)
        ax.text(x, y, lab, transform=ax.transAxes, **default_kw)

# ──────────────────────────── 1. LOAD DATA ───────────────────────
print("Loading raw dataset (absolutely no filtering)...")
df = pd.read_excel(data_path)

# Convert specified gases to numeric; keep NaN values
for col in gas_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

n_total = len(df)
print(f"Transformers in file: {n_total}")

# ──────────────────────────── 2. VISUALS ─────────────────────────

# 2a. Hydrogen scatter (linear + log)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
idx = df.index

# Linear
ax1.scatter(idx, df["Hydrogen (H2)"], s=40, alpha=0.6,
            color="lightcoral", edgecolor="k", linewidth=0.5)
ax1.set(title="Hydrogen Concentration – Linear Scale",
        xlabel="Transformer Index", ylabel="H₂ (ppm)")
ax1.grid(alpha=0.3)

# Log
ax2.scatter(idx, df["Hydrogen (H2)"].where(df["Hydrogen (H2)"] > 0)+1,
            s=40, alpha=0.6, color="lightgreen",
            edgecolor="k", linewidth=0.5)
ax2.set(title="Hydrogen Concentration – Log Scale",
        xlabel="Transformer Index", ylabel="H₂ (ppm)")
ax2.set_yscale("log")
ax2.grid(alpha=0.3)

add_subplot_labels([ax1, ax2])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "01_hydrogen_distribution.png"),
            bbox_inches="tight")
plt.close()

# 2a2. Hydrogen scatter (log only)
fig, ax = plt.subplots(figsize=(12, 7))
idx = df.index

ax.scatter(idx, df["Hydrogen (H2)"].where(df["Hydrogen (H2)"] > 0)+1,
           s=40, alpha=0.6, color="lightgreen",
           edgecolor="k", linewidth=0.5)
ax.set(title="Hydrogen Concentration – Log Scale",
       xlabel="Transformer Index", ylabel="H₂ (ppm)")
ax.set_yscale("log")
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "01c_hydrogen_distribution_log_only.png"),
            bbox_inches="tight")
plt.close()

# 2a3. Individual gas scatter plots (log only, including zeros)
colors = ["lightcoral", "lightblue", "lightgreen", "lightyellow", "lightpink"]

for i, (col, short, color) in enumerate(zip(gas_cols, gas_names, colors)):
    # Create individual figure for each gas
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Get all data including zeros
    gas_data = df[col]
    # Add 1 to all values to handle zeros in log scale
    gas_data_shifted = gas_data + 1
    
    # Plot all data points
    ax.scatter(df.index, gas_data_shifted,
               s=40, alpha=0.6, color=color,
               edgecolor="k", linewidth=0.5)
    
    ax.set(title=f"{short} Concentration – Log Scale",
           xlabel="Transformer Index", ylabel=f"{short} (ppm)")
    ax.set_yscale("log")
    ax.grid(alpha=0.3)
    # Ensure consistent x-axis limits
    ax.set_xlim(df.index.min(), df.index.max())
    
    # Add count statistics
    n_total = gas_data.notna().sum()
    n_zeros = (gas_data == 0).sum()
    n_positive = (gas_data > 0).sum()
    
    ax.text(0.02, 0.98, f"Total: {n_total}\nZeros: {n_zeros}\nPositive: {n_positive}", 
            transform=ax.transAxes, 
            fontsize=12, verticalalignment='top', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    # Save each gas separately
    plt.savefig(os.path.join(output_dir, f"01c2_{short}_distribution_log_only.png"),
                bbox_inches="tight")
    plt.close()

# 2b. Correlation heat-map (pairwise complete obs)
fig, ax = plt.subplots(figsize=(8, 8))
corr = df[gas_cols].corr()           # NaNs automatically handled
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".3f",
            square=True, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title("Gas Correlation Matrix")
ax.set_xticklabels(gas_names, rotation=45)
ax.set_yticklabels(gas_names, rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "02_correlation_analysis.png"))
plt.close()

# 2c. Box-plots (raw & log)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
melt = df[gas_cols].melt(var_name="Gas", value_name="ppm")
melt["Gas"] = melt["Gas"].map(dict(zip(gas_cols, gas_names)))

# Raw
sns.boxplot(data=melt, x="Gas", y="ppm", ax=ax1, palette="Set2")
ax1.set(title="Gas Concentration Distributions (Raw)",
        ylabel="Concentration (ppm)")
ax1.grid(alpha=0.3, axis="y")

# Log
melt["log10(ppm+1)"] = np.log10(melt["ppm"] + 1)
sns.boxplot(data=melt, x="Gas", y="log10(ppm+1)", ax=ax2, palette="Set2")
ax2.set(title="Gas Concentrations (Log)",
        ylabel="log₁₀(ppm + 1)")
ax2.grid(alpha=0.3, axis="y")

add_subplot_labels([ax1, ax2])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "03_distribution_analysis.png"))
plt.close()

# 2c2. Box-plots (log only, without +1 notation)
fig, ax = plt.subplots(figsize=(14, 7))
melt_log = df[gas_cols].melt(var_name="Gas", value_name="ppm")
melt_log["Gas"] = melt_log["Gas"].map(dict(zip(gas_cols, gas_names)))
melt_log["log10_ppm"] = np.log10(melt_log["ppm"] + 1)

sns.boxplot(data=melt_log, x="Gas", y="log10_ppm", ax=ax, palette="Set2")
ax.set(title="Gas Concentrations (Log Scale)",
       ylabel="log₁₀(ppm)")
ax.grid(alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "03c_distribution_analysis_log_only.png"))
plt.close()

# 2d. Histograms (log scale y-axis)
fig, axes = plt.subplots(2, 5, figsize=(22, 10))
for i, (col, short) in enumerate(zip(gas_cols, gas_names)):
    # Top row - with log y-scale
    data_top = df[col].dropna()
    axes[0, i].hist(data_top, bins=30,
                    color="skyblue", edgecolor="k", alpha=0.7)
    axes[0, i].set_yscale('log')
    axes[0, i].set(title=f"{short} – Log Y-Scale")
    axes[0, i].set_xlabel("Concentration (ppm)")
    axes[0, i].set_ylabel("Frequency (log)")
    axes[0, i].grid(alpha=0.3, axis='y')
    
    # Bottom row - with log y-scale (different binning)
    axes[1, i].hist(data_top, bins=50,
                    color="lightgreen", edgecolor="k", alpha=0.7)
    axes[1, i].set_yscale('log')
    axes[1, i].set(title=f"{short} – Log Y-Scale (50 bins)")
    axes[1, i].set_xlabel("Concentration (ppm)")
    axes[1, i].set_ylabel("Frequency (log)")
    axes[1, i].grid(alpha=0.3, axis='y')
    
add_subplot_labels(axes.flatten(),
                   labels=[f"({chr(97+i)})" for i in range(10)])
plt.suptitle("Gas Histograms with Logarithmic Frequency Scale", y=0.98, fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "04_histogram_analysis.png"))
plt.close()

# 2d2. Individual histograms (log scale y-axis only, normal x-axis)
colors_hist = ["skyblue", "lightcoral", "lightgreen", "lightyellow", "lightpink"]

for i, (col, short, color) in enumerate(zip(gas_cols, gas_names, colors_hist)):
    # Create individual figure for each gas
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Get the data
    data = df[col].dropna()
    
    # Create histogram with log scale on y-axis
    counts, bins, patches = ax.hist(data, bins=50,
                                   color=color, edgecolor="k", 
                                   alpha=0.7, linewidth=1.2)
    
    ax.set_yscale('log')
    ax.set_title(f"{short} Concentration Distribution", fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel("Concentration (ppm)", fontsize=16, fontweight='bold')
    ax.set_ylabel("Frequency (log scale)", fontsize=16, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    # Add statistics box
    mean_val = data.mean()
    median_val = data.median()
    std_val = data.std()
    
    stats_text = f"Mean: {mean_val:.1f} ppm\nMedian: {median_val:.1f} ppm\nStd: {std_val:.1f} ppm"
    ax.text(0.98, 0.98, stats_text, 
            transform=ax.transAxes, 
            fontsize=12, verticalalignment='top', horizontalalignment='right',
            fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    # Save each gas separately
    plt.savefig(os.path.join(output_dir, f"04c_{short}_histogram_log_y_axis.png"), 
                bbox_inches='tight')
    plt.close()

# 2e. Distribution analysis - Normal distribution on actual ppm values
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.flatten()

for i, (col, short) in enumerate(zip(gas_cols, gas_names)):
    if i < 5:  # We have 5 gases
        # Get all data values
        data = df[col].dropna()
        
        if len(data) > 0:
            ax = axes[i]
            
            # Fit normal distribution to actual ppm data
            mu, sigma = data.mean(), data.std()
            
            # Create smooth curve for normal distribution
            x = np.linspace(data.min(), data.max(), 1000)
            y_norm = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu)/sigma)**2)
            
            # Plot normal distribution
            ax.plot(x, y_norm, 'r-', linewidth=3, label=f'Normal fit: μ={mu:.1f}, σ={sigma:.1f}')
            
            # Set reasonable y-axis limits
            ax.set_ylim(0, y_norm.max() * 1.2)
            
            # Styling
            ax.set_title(f'{short} Distribution', fontsize=16, fontweight='bold')
            ax.set_xlabel('Concentration (ppm)', fontsize=14, fontweight='bold')
            ax.set_ylabel('Density', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, which='both')
            ax.legend(fontsize=11, loc='upper left')
            
            # Stack all info boxes in top right corner
            y_pos = 0.98
            
            # Distribution statistics box
            textstr = f'n={len(data)}\nSkewness={data.skew():.2f}\nKurtosis={data.kurtosis():.2f}'
            ax.text(0.98, y_pos, textstr, transform=ax.transAxes, 
                   fontsize=10, verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            y_pos -= 0.18  # Move down for next box
            
            # Normal fit parameters box
            normal_text = f'Normal fit:\nμ={mu:.1f}\nσ={sigma:.1f}'
            ax.text(0.98, y_pos, normal_text, transform=ax.transAxes, 
                   fontsize=10, verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            y_pos -= 0.15  # Move down for next box
            

# Remove empty subplot
if len(gas_cols) < 6:
    fig.delaxes(axes[5])

add_subplot_labels(axes[:5])
plt.suptitle('Distribution Analysis: Gas Concentration Distributions with Normal Fit', 
             fontsize=20, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "04_5_distribution_analysis_lognormal.png"),
            bbox_inches="tight")
plt.close()

# 2e2. Normal distribution curves only (without histogram)
from scipy import stats
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.flatten()

for i, (col, short) in enumerate(zip(gas_cols, gas_names)):
    if i < 5:  # We have 5 gases
        # Get all data values
        data = df[col].dropna()
        
        if len(data) > 0:
            ax = axes[i]
            
            # Fit normal distribution to actual ppm data
            mu, sigma = data.mean(), data.std()
            
            # Create smooth curve for normal distribution
            x = np.linspace(data.min() - 3*sigma, data.max() + 3*sigma, 1000)
            y_norm = stats.norm.pdf(x, mu, sigma)
            
            # Plot normal distribution
            ax.plot(x, y_norm, 'b-', linewidth=3, label=f'Normal: μ={mu:.1f}, σ={sigma:.1f}')
            
            # Add vertical lines for mean and std deviations
            ax.axvline(mu, color='r', linestyle='--', linewidth=2, label=f'Mean = {mu:.1f}')
            ax.axvline(mu - sigma, color='g', linestyle=':', linewidth=1.5, alpha=0.7)
            ax.axvline(mu + sigma, color='g', linestyle=':', linewidth=1.5, alpha=0.7, label='±1σ')
            ax.axvline(mu - 2*sigma, color='orange', linestyle=':', linewidth=1.5, alpha=0.5)
            ax.axvline(mu + 2*sigma, color='orange', linestyle=':', linewidth=1.5, alpha=0.5, label='±2σ')
            
            # Fill areas under curve
            x_fill = x[(x >= mu - sigma) & (x <= mu + sigma)]
            y_fill = stats.norm.pdf(x_fill, mu, sigma)
            ax.fill_between(x_fill, y_fill, alpha=0.3, color='green', label='68.3% of data')
            
            # Styling
            ax.set_title(f'{short} Normal Distribution', fontsize=16, fontweight='bold')
            ax.set_xlabel('Concentration (ppm)', fontsize=14, fontweight='bold')
            ax.set_ylabel('Probability Density', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10, loc='upper right')
            
            # Add statistics box
            stats_text = f'n={len(data)}\nSkewness={data.skew():.2f}\nKurtosis={data.kurtosis():.2f}\nMin={data.min():.1f}\nMax={data.max():.1f}'
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
                   fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Remove empty subplot
if len(gas_cols) < 6:
    fig.delaxes(axes[5])

add_subplot_labels(axes[:5])
plt.suptitle('Normal Distribution Analysis (Without Histograms)', 
             fontsize=20, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "04_5_normal_distribution_only.png"),
            bbox_inches="tight")
plt.close()

# 2f. Fault analysis if labels exist
if "Fault" in df.columns and df["Fault"].notna().any():
    df_fault = df[df["Fault"].astype(str).str.strip() != ""]
    if not df_fault.empty:
        fault_counts = df_fault["Fault"].value_counts()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

        # Pie chart
        wedges, _ = ax1.pie(fault_counts.values, startangle=90,
                            colors=plt.cm.Set3(np.linspace(0, 1, len(fault_counts))),
                            labels=None, labeldistance=None)
        ax1.set_title("Fault Type Distribution")
        labels = [f"{f}\n{c} ({c/len(df_fault)*100:.1f}%)"
                  for f, c in fault_counts.items()]
        ax1.legend(wedges, labels, title="Fault", bbox_to_anchor=(1, 0.5))

        # Mean by fault (log scale)
        means = np.log10(df_fault.groupby("Fault")[gas_cols].mean() + 1)
        means.columns = gas_names
        means.plot.bar(stacked=True, ax=ax2, colormap="viridis",
                       width=0.8, alpha=0.8)
        ax2.set(title="Mean Gas per Fault – Log",
                ylabel="log₁₀(ppm + 1)", xlabel="Fault")
        ax2.legend(bbox_to_anchor=(1.05, 1))
        ax2.grid(alpha=0.3, axis="y")

        add_subplot_labels([ax1, ax2])
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "05_fault_analysis.png"))
        plt.close()


# ──────────────────────────── 3. SUMMARY TXT ─────────────────────
desc = df[gas_cols].describe().T
desc["skewness"] = df[gas_cols].skew()
desc["kurtosis"] = df[gas_cols].kurtosis()

with open(summary_file, "w") as f:
    f.write("=== RAW DGA DATA ANALYSIS SUMMARY ===\n")
    f.write(f"Transformers in file: {n_total}\n\n")
    f.write("=== DESCRIPTIVE STATISTICS (ALL DATA) ===\n")
    f.write(desc.to_string())
    f.write("\n\n=== CORRELATION MATRIX ===\n")
    f.write(corr.to_string())
    if "Fault" in df.columns and not df_fault.empty:
        f.write("\n\n=== FAULT DISTRIBUTION ===\n")
        f.write(fault_counts.to_string())
        f.write("\n")

print("Analysis complete - figures & summary saved to:")
print(output_dir)

# ──────────────────────────── 4. CREATE WEB DATA ───────────────────
print("\nCreating web interface data...")

# Convert DataFrame to JSON for web interface
web_data = []
for index, row in df.iterrows():
    transformer_record = {
        "ID": int(index + 1),
        "Hydrogen": float(row["Hydrogen (H2)"]) if pd.notna(row["Hydrogen (H2)"]) else 0,
        "Methane": float(row["Methane (CH4)"]) if pd.notna(row["Methane (CH4)"]) else 0,
        "Ethylene": float(row["Ethylene (C2H4)"]) if pd.notna(row["Ethylene (C2H4)"]) else 0,
        "Ethane": float(row["Ethane (C2H6)"]) if pd.notna(row["Ethane (C2H6)"]) else 0,
        "Acetylene": float(row["Acetylene (C2H2)"]) if pd.notna(row["Acetylene (C2H2)"]) else 0,
        "Fault": str(row["Fault"]) if pd.notna(row["Fault"]) and str(row["Fault"]).strip() != "" else "No Fault"
    }
    web_data.append(transformer_record)

# Save JSON data for web interface
import json
with open(os.path.join(output_dir, "..", "web_data.json"), "w") as f:
    json.dump(web_data, f, indent=2)

print(f"Web data created: {len(web_data)} transformer records")
print("Web interface data ready for deployment")
