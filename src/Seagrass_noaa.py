import pandas as pd
import numpy as np

# Read SOCAT file
df = pd.read_csv(
    "SOCATv2023_qrtrdeg_gridded_coast_monthly.csv",
    skiprows=253
)

# Remove unwanted spaces from column names
df.columns = df.columns.str.strip()

print("Columns:")
print(df.columns.tolist())


# --------------------------------------------------
# 1. Convert DATE to datetime
# --------------------------------------------------

df["DATE"] = pd.to_datetime(df["DATE"])


# --------------------------------------------------
# 2. Keep only 2019 and 2020
# --------------------------------------------------

df = df[df["DATE"].dt.year.isin([2019, 2020])].copy()

print("\n2019–2020 records:", len(df))


# --------------------------------------------------
# 3. Keep cells with fCO2 observations
# --------------------------------------------------

df = df[df["COAST_FCO2_COUNT_NOBS"] > 0].copy()

print("With fCO2 observations:", len(df))


# --------------------------------------------------
# 4. Also require SST and salinity observations
# --------------------------------------------------

df = df[
    (df["COAST_SST_COUNT_NOBS"] > 0) &
    (df["COAST_SALINITY_COUNT_NOBS"] > 0)
].copy()

print("With fCO2 + SST + salinity:", len(df))


# --------------------------------------------------
# 5. Save filtered data
# --------------------------------------------------

df.to_csv(
    "SOCAT_2019_2020_filtered.csv",
    index=False
)

print("\nSaved: SOCAT_2019_2020_filtered.csv")

# --------------------------------------------------
# 6. Summarize data by 0.25° grid cell
# --------------------------------------------------

summary = (
    df.groupby(["LAT", "LON"])
      .agg(
          total_fCO2_obs=("COAST_FCO2_COUNT_NOBS", "sum"),
          total_SST_obs=("COAST_SST_COUNT_NOBS", "sum"),
          total_salinity_obs=("COAST_SALINITY_COUNT_NOBS", "sum"),
          months_with_data=("DATE", "nunique"),
          total_cruises=("COAST_COUNT_NCRUISE", "sum")
      )
      .reset_index()
)

# --------------------------------------------------
# 7. Sort by amount of fCO2 data
# --------------------------------------------------

summary = summary.sort_values(
    by="total_fCO2_obs",
    ascending=False
)

# --------------------------------------------------
# 8. Print the 50 best-supported cells
# --------------------------------------------------

print("\nTop 50 cells:")
print(summary.head(50).to_string(index=False))

# --------------------------------------------------
# 9. Save summary for QGIS
# --------------------------------------------------

summary.to_csv(
    "SOCAT_2019_2020_cell_summary.csv",
    index=False
)

print("\nSaved:")
print("SOCAT_2019_2020_cell_summary.csv")

# --------------------------------------------------
# 10. Create a QGIS-ready cell summary
# --------------------------------------------------

# Keep cells with at least 1 observation
qgis_cells = summary[
    summary["total_fCO2_obs"] > 0
].copy()

# Save
qgis_cells.to_csv(
    "SOCAT_2019_2020_QGIS_cells.csv",
    index=False
)

print("\nQGIS cells saved:")
print("SOCAT_2019_2020_QGIS_cells.csv")

# ============================================================
# 11. Extract our two study cells
# ============================================================

study_points = {
    "Seagrass": (23.125, -78.375),
    "Open_Water": (23.125, -78.875)
}

study_data = []

for location, (lat, lon) in study_points.items():

    point = df[
        (df["LAT"] == lat) &
        (df["LON"] == lon)
    ].copy()

    point["Location"] = location

    study_data.append(point)

study = pd.concat(study_data, ignore_index=True)


# ============================================================
# 12. Select variables needed for PyCO2SYS
# ============================================================

study = study[
    [
        "Location",
        "DATE",
        "LAT",
        "LON",
        "COAST_FCO2_COUNT_NOBS",
        "COAST_FCO2_AVE_UNWTD",
        "COAST_FCO2_AVE_WEIGHTED",
        "COAST_SST_COUNT_NOBS",
        "COAST_SST_AVE_UNWTD",
        "COAST_SST_AVE_WEIGHTED",
        "COAST_SALINITY_COUNT_NOBS",
        "COAST_SALINITY_AVE_UNWTD",
        "COAST_SALINITY_AVE_WEIGHTED"
    ]
].copy()


# ============================================================
# 13. Print the actual monthly observations
# ============================================================

print("\n==============================================")
print("SELECTED SOCAT STUDY CELLS")
print("==============================================")

print(study.to_string(index=False))


# ============================================================
# 14. Save
# ============================================================

study.to_csv(
    "SOCAT_Seagrass_OpenWater_monthly.csv",
    index=False
)

print("\nSaved:")
print("SOCAT_Seagrass_OpenWater_monthly.csv")