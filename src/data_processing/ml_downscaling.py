import pandas as pd
import numpy as np

# ============================================================
# LOAD PAIRWISE PYCO2SYS RESULTS
# ============================================================

file = r"C:\Pyhton\PyCO2SYS_2019_20_8pair_results.csv"

df = pd.read_csv(file)

print("\nLoaded results:")
print(len(df), "pair-month observations")


# ============================================================
# CALCULATE PARAMETER DIFFERENCES
# ============================================================

df["Delta_DIC"] = (
    df["DIC_SG"] - df["DIC_OW"]
)

df["Delta_TA"] = (
    df["TA_SG"] - df["TA_OW"]
)

df["Delta_SST"] = (
    df["SST_SG"] - df["SST_OW"]
)

df["Delta_Salinity"] = (
    df["Salinity_SG"] - df["Salinity_OW"]
)


# ============================================================
# SELECT IMPORTANT COLUMNS
# ============================================================

cols = [
    "Pair",
    "Month",

    "SG_Lat",
    "SG_Lon",
    "OW_Lat",
    "OW_Lon",

    "DIC_SG",
    "DIC_OW",
    "Delta_DIC",

    "TA_SG",
    "TA_OW",
    "Delta_TA",

    "SST_SG",
    "SST_OW",
    "Delta_SST",

    "Salinity_SG",
    "Salinity_OW",
    "Delta_Salinity",

    "pH_SG",
    "pH_OW",
    "Delta_pH",

    "Omega_ar_SG",
    "Omega_ar_OW",
    "Delta_Omega_ar"
]

analysis = df[cols].copy()


# ============================================================
# PRINT PAIRWISE RESULTS
# ============================================================

print("\n")
print("=" * 100)
print("PAIRWISE CARBONATE-SYSTEM DIFFERENCES")
print("=" * 100)

print(
    analysis.to_string(index=False)
)


# ============================================================
# MONTHLY SUMMARY
# ============================================================

monthly = (
    analysis
    .groupby("Month")
    .agg(

        n_pairs=("Pair", "count"),

        Mean_Delta_DIC=("Delta_DIC", "mean"),
        SD_Delta_DIC=("Delta_DIC", "std"),

        Mean_Delta_TA=("Delta_TA", "mean"),
        SD_Delta_TA=("Delta_TA", "std"),

        Mean_Delta_SST=("Delta_SST", "mean"),
        SD_Delta_SST=("Delta_SST", "std"),

        Mean_Delta_Salinity=("Delta_Salinity", "mean"),
        SD_Delta_Salinity=("Delta_Salinity", "std"),

        Mean_Delta_pH=("Delta_pH", "mean"),
        SD_Delta_pH=("Delta_pH", "std"),

        Mean_Delta_Omega_ar=("Delta_Omega_ar", "mean"),
        SD_Delta_Omega_ar=("Delta_Omega_ar", "std")
    )
    .reset_index()
)


# ============================================================
# STANDARD ERRORS
# ============================================================

for parameter in [
    "DIC",
    "TA",
    "SST",
    "Salinity",
    "pH",
    "Omega_ar"
]:

    monthly[f"SE_Delta_{parameter}"] = (
        monthly[f"SD_Delta_{parameter}"]
        /
        np.sqrt(monthly["n_pairs"])
    )


# ============================================================
# PRINT MONTHLY SUMMARY
# ============================================================

print("\n")
print("=" * 100)
print("MONTHLY MEAN DIFFERENCES")
print("=" * 100)

print(
    monthly.to_string(index=False)
)


# ============================================================
# SAVE
# ============================================================

output1 = (
    r"C:\Pyhton\PyCO2SYS_2019_20_Parameter_Differences.csv"
)

output2 = (
    r"C:\Pyhton\PyCO2SYS_2019_20_Monthly_Parameter_Summary.csv"
)

analysis.to_csv(
    output1,
    index=False
)

monthly.to_csv(
    output2,
    index=False
)


print("\n")
print("=" * 100)
print("SAVED")
print("=" * 100)

print(output1)
print(output2)