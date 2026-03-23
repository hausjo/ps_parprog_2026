import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

df = pd.read_csv("results.csv")

stats = (
    df.groupby(["Threads", "Program"])["Time"]
    .agg(mean="mean", std="std")
    .reset_index()
)

programs = df["Program"].unique()
threads  = sorted(df["Threads"].unique())

colors = plt.cm.tab10(np.linspace(0, 1, len(programs)))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Benchmark stability: mean ± 1 std dev", fontsize=13, y=1.01)

# — left: line chart (mean + error bars per thread count)
ax = axes[0]
for prog, color in zip(programs, colors):
    sub = stats[stats["Program"] == prog].sort_values("Threads")
    ax.errorbar(
        sub["Threads"], sub["mean"], yerr=sub["std"],
        label=prog, color=color,
        marker="o", linewidth=1.8, capsize=4, capthick=1.5,
    )
ax.set_xlabel("Threads")
ax.set_ylabel("Time (s)")
ax.set_title("Runtime vs thread count")
ax.set_xticks(threads)
ax.legend(fontsize=8, ncol=2)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(which="major", alpha=0.3); ax.grid(which="minor", alpha=0.1)

# — right: bar chart of coefficient of variation (stddev / mean), all configs
ax2 = axes[1]
stats["cv"] = stats["std"] / stats["mean"] * 100
pivot = stats.pivot_table(index="Threads", columns="Program", values="cv", fill_value=0)
x = np.arange(len(threads))
width = 0.8 / len(programs)
for i, (prog, color) in enumerate(zip(programs, colors)):
    offset = (i - len(programs) / 2 + 0.5) * width
    ax2.bar(x + offset, pivot[prog], width, label=prog, color=color, alpha=0.85)
ax2.set_xlabel("Threads")
ax2.set_ylabel("Coefficient of variation (%)")
ax2.set_title("Measurement noise (CV = std/mean)")
ax2.set_xticks(x); ax2.set_xticklabels(threads)
ax2.axhline(5, color="red", linestyle="--", linewidth=1, label="5% threshold")
ax2.legend(fontsize=8, ncol=2)
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("benchmark_stability.png", dpi=150, bbox_inches="tight")
print("Saved: benchmark_stability.png")