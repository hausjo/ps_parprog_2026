import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

df = pd.read_csv("results.csv")

stats = (
    df.groupby(["Affinity", "Program"])["Time"]
    .agg(mean="mean", std="std")
    .reset_index()
)

programs = df["Program"].unique()
affinities = df["Affinity"].unique()

colors = plt.cm.tab10(np.linspace(0, 1, len(programs)))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("False Sharing Benchmark: same socket vs cross socket", fontsize=13, y=1.01)

affinity_labels = {
    "0-1-2-3-4-5": "Same socket\n(cores 0-5)",
    "0-1-2-6-7-8": "Cross socket\n(cores 0-2, 6-8)",
}

# — left: bar chart (mean + error bars per affinity)
ax = axes[0]
x = np.arange(len(affinities))
width = 0.8 / len(programs)
for i, (prog, color) in enumerate(zip(programs, colors)):
    sub = stats[stats["Program"] == prog]
    offset = (i - len(programs) / 2 + 0.5) * width
    ax.bar(x + offset, sub["mean"], width,
           yerr=sub["std"], label=prog, color=color,
           alpha=0.85, capsize=4)
ax.set_xlabel("Core Affinity")
ax.set_ylabel("Time (s)")
ax.set_title("Runtime vs core affinity")
ax.set_xticks(x)
ax.set_xticklabels([affinity_labels.get(a, a) for a in affinities])
ax.legend(fontsize=8)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(which="major", alpha=0.3); ax.grid(which="minor", alpha=0.1)

# — right: coefficient of variation
ax2 = axes[1]
stats["cv"] = stats["std"] / stats["mean"] * 100
pivot = stats.pivot_table(index="Affinity", columns="Program", values="cv", fill_value=0)
for i, (prog, color) in enumerate(zip(programs, colors)):
    offset = (i - len(programs) / 2 + 0.5) * width
    ax2.bar(x + offset, pivot[prog], width, label=prog, color=color, alpha=0.85)
ax2.set_xlabel("Core Affinity")
ax2.set_ylabel("Coefficient of variation (%)")
ax2.set_title("Measurement noise (CV = std/mean)")
ax2.set_xticks(x)
ax2.set_xticklabels([affinity_labels.get(a, a) for a in affinities])
ax2.axhline(5, color="red", linestyle="--", linewidth=1, label="5% threshold")
ax2.legend(fontsize=8)
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("benchmark_stability.png", dpi=150, bbox_inches="tight")
print("Saved: benchmark_stability.png")