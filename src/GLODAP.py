import pandas as pd
import numpy as np

# ============================================================
# GLODAPv2.2023 — Bahamas shallow carbonate data
# ============================================================


# --------------------------------------------------
# 1. Read GLODAP Atlantic CSV
# --------------------------------------------------

file = "GLODAPv2.2023_Atlantic_Ocean.csv"

df = pd.read_csv(
    file,
    low_memory=False
)

print("Original shape:", df.shape)


# --------------------------------------------------
# 2. Clean column names
# --------------------------------------------------

df.columns = df.columns.str.strip()

print("\nColumns:")
print(df.columns.tolist())


# --------------------------------------------------
# 3. Filter to Bahamas / nearby region
# --------------------------------------------------

df = df[
    (df["G2latitude"] >= 18) &
    (df["G2latitude"] <= 27) &
    (df["G2longitude"] >= -82) &
    (df["G2longitude"] <= -70)
].copy()

print("\nBahamas region:", df.shape)


# --------------------------------------------------
# 4. Keep shallow observations <= 10 m
# --------------------------------------------------

df = df[
    (df["G2depth"] >= 0) &
    (df["G2depth"] <= 10)
].copy()

print("Upper 10 m:", df.shape)


# --------------------------------------------------
# 5. Keep records containing all required variables
# --------------------------------------------------

required = [
    "G2tco2",
    "G2talk",
    "G2temperature",
    "G2salinity",
    "G2phtsinsitutp"
]

df = df.dropna(
    subset=required
).copy()

print(
    "With DIC + TA + T + S + pH:",
    df.shape
)


# --------------------------------------------------
# 6. Keep only reasonable values
# --------------------------------------------------

df = df[
    (df["G2tco2"] > 0) &
    (df["G2talk"] > 0) &
    (df["G2temperature"] > -5) &
    (df["G2salinity"] > 0) &
    (df["G2phtsinsitutp"] > 0)
].copy()

print(
    "After basic value filter:",
    df.shape
)


# --------------------------------------------------
# 7. Select useful columns
# --------------------------------------------------

columns_to_keep = [
    # Station information
    "G2expocode",
    "G2cruise",
    "G2station",

    # Date
    "G2year",
    "G2month",
    "G2day",

    # Location
    "G2latitude",
    "G2longitude",

    # Depth
    "G2depth",

    # Carbonate chemistry
    "G2tco2",
    "G2talk",

    # Physical parameters
    "G2temperature",
    "G2salinity",

    # Observed pH
    "G2phtsinsitutp",

    # Quality control
    "G2tco2qc",
    "G2talkqc",
    "G2phtsqc"
]

# Keep only columns that actually exist
columns_to_keep = [
    col for col in columns_to_keep
    if col in df.columns
]

df_final = df[columns_to_keep].copy()


# --------------------------------------------------
# 8. Sort by location and depth
# --------------------------------------------------

df_final = df_final.sort_values(
    by=[
        "G2latitude",
        "G2longitude",
        "G2depth"
    ]
)


# --------------------------------------------------
# 9. Save filtered analysis file
# --------------------------------------------------

df_final.to_csv(
    "GLODAP_Bahamas_shallow_carbonate.csv",
    index=False
)

print("\nSaved:")
print("GLODAP_Bahamas_shallow_carbonate.csv")


# --------------------------------------------------
# 10. Save QGIS-ready file
# --------------------------------------------------

df_final.to_csv(
    "GLODAP_Bahamas_QGIS.csv",
    index=False
)

print("\nQGIS file saved:")
print("GLODAP_Bahamas_QGIS.csv")


# --------------------------------------------------
# 11. Summary
# --------------------------------------------------

print("\n========================================")
print("FINAL DATASET SUMMARY")
print("========================================")

print(
    "Number of observations:",
    len(df_final)
)

print(
    "Depth range:",
    df_final["G2depth"].min(),
    "to",
    df_final["G2depth"].max(),
    "m"
)

print(
    "Latitude range:",
    df_final["G2latitude"].min(),
    "to",
    df_final["G2latitude"].max()
)

print(
    "Longitude range:",
    df_final["G2longitude"].min(),
    "to",
    df_final["G2longitude"].max()
)


# --------------------------------------------------
# 12. Display first 10 records
# --------------------------------------------------

print("\nFirst 10 records:")

print(
    df_final.head(10).to_string(
        index=False
    )
)