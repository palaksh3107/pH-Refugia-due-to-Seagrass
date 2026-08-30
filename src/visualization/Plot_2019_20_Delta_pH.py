import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Load monthly results
# --------------------------------------------------

file = r"C:\Pyhton\PyCO2SYS_2019_20_monthly_summary.csv"

df = pd.read_csv(file)

df["Month"] = pd.to_datetime(df["Month"])


# --------------------------------------------------
# Plot Mean Delta pH
# --------------------------------------------------

plt.figure(figsize=(9, 5))

plt.errorbar(
    df["Month"],
    df["Mean_Delta_pH"],
    yerr=df["SE_Delta_pH"],
    marker="o",
    capsize=4
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel("Month")
plt.ylabel("Mean ΔpH (Seagrass − Open Water)")
plt.title("Seagrass–Open Water ΔpH: 2019–20")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    r"C:\Pyhton\Delta_pH_2019_20.png",
    dpi=300
)

plt.show()