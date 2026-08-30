import xarray as xr
import pandas as pd
import numpy as np

# ============================================================
# FILE
# ============================================================

FILE = r"C:\Pyhton\cmems_obs-mob_glo_bgc-car_my_irr-i_1788042515626.nc"


# ============================================================
# LOAD DATASET
# ============================================================

print("\nOpening Copernicus dataset...")

ds = xr.open_dataset(FILE)

print("Dataset opened successfully.\n")


# ============================================================
# BASIC INFORMATION
# ============================================================

print("=" * 70)
print("DATASET DIMENSIONS")
print("=" * 70)

print(ds.dims)


print("\n" + "=" * 70)
print("COORDINATES")
print("=" * 70)

for coord in ds.coords:
    values = ds[coord].values

    print(
        f"{coord}: "
        f"shape={values.shape}, "
        f"first={values.flat[0]}, "
        f"last={values.flat[-1]}"
    )


# ============================================================
# VARIABLES
# ============================================================

print("\n" + "=" * 70)
print("DATA VARIABLES")
print("=" * 70)

for var in ds.data_vars:

    da = ds[var]

    print(
        f"{var:<25} "
        f"dims={str(da.dims):<35} "
        f"units={da.attrs.get('units', 'N/A')}"
    )


# ============================================================
# TIME RANGE
# ============================================================

print("\n" + "=" * 70)
print("TIME COVERAGE")
print("=" * 70)

print("Start:", pd.Timestamp(ds.time.values[0]))
print("End  :", pd.Timestamp(ds.time.values[-1]))
print("Number of time steps:", len(ds.time))


# ============================================================
# 2019–2020 SUBSET
# ============================================================

ds_1920 = ds.sel(
    time=slice("2019-01-01", "2020-12-31")
)

print("\n" + "=" * 70)
print("2019–2020 DATASET")
print("=" * 70)

print("Time steps:", len(ds_1920.time))
print("Latitude cells:", len(ds_1920.latitude))
print("Longitude cells:", len(ds_1920.longitude))

print(
    "Total spatial cells:",
    len(ds_1920.latitude) * len(ds_1920.longitude)
)


# ============================================================
# IMPORTANT VARIABLES
# ============================================================

variables_to_check = [
    "tco2",
    "talk",
    "spco2",
    "ph",
    "omega_ar",
    "omega_ca",
    "fgco2"
]


# ============================================================
# MISSING DATA + RANGE
# ============================================================

print("\n" + "=" * 70)
print("VARIABLE QUALITY CHECK — 2019–2020")
print("=" * 70)

summary = []


for var in variables_to_check:

    if var not in ds_1920:

        print(f"\n{var}: NOT FOUND")
        continue

    data = ds_1920[var]

    values = data.values

    finite = np.isfinite(values)

    n_total = values.size
    n_valid = finite.sum()
    n_missing = n_total - n_valid

    if n_valid > 0:

        valid_values = values[finite]

        minimum = valid_values.min()
        maximum = valid_values.max()
        mean = valid_values.mean()

    else:

        minimum = np.nan
        maximum = np.nan
        mean = np.nan


    summary.append({

        "Variable": var,
        "Total_values": n_total,
        "Valid_values": n_valid,
        "Missing_values": n_missing,
        "Missing_percent": 100 * n_missing / n_total,
        "Minimum": minimum,
        "Maximum": maximum,
        "Mean": mean,
        "Units": data.attrs.get("units", "N/A")
    })


summary_df = pd.DataFrame(summary)

print(
    summary_df.to_string(index=False)
)


# ============================================================
# SPATIAL GRID
# ============================================================

print("\n" + "=" * 70)
print("SPATIAL GRID")
print("=" * 70)

lat = ds.latitude.values
lon = ds.longitude.values

print("Latitude range :", lat.min(), "to", lat.max())
print("Longitude range:", lon.min(), "to", lon.max())

if len(lat) > 1:
    print(
        "Latitude spacing:",
        abs(float(lat[1] - lat[0]))
    )

if len(lon) > 1:
    print(
        "Longitude spacing:",
        abs(float(lon[1] - lon[0]))
    )


# ============================================================
# CREATE ML-READY DATAFRAME
# ============================================================

print("\n" + "=" * 70)
print("CREATING ML-READY DATAFRAME")
print("=" * 70)

# Select variables that are useful initially
ml_variables = [
    "tco2",
    "talk",
    "spco2",
    "ph",
    "omega_ar",
    "omega_ca",
    "fgco2"
]

available = [
    v for v in ml_variables
    if v in ds_1920.data_vars
]

print("Variables included:")
print(available)


# Convert to dataframe
ml_df = (
    ds_1920[available]
    .to_dataframe()
    .reset_index()
)


# Add useful temporal variables
ml_df["year"] = ml_df["time"].dt.year
ml_df["month"] = ml_df["time"].dt.month

ml_df["month_sin"] = np.sin(
    2 * np.pi * ml_df["month"] / 12
)

ml_df["month_cos"] = np.cos(
    2 * np.pi * ml_df["month"] / 12
)


# ============================================================
# SAVE
# ============================================================

OUTPUT = r"C:\Pyhton\Copernicus_2019_20_ML_Data.csv"

ml_df.to_csv(
    OUTPUT,
    index=False
)

print("\nSaved ML-ready dataset:")
print(OUTPUT)

print("\nRows:", len(ml_df))
print("Columns:", len(ml_df.columns))


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(
    f"""
Period:
2019–2020

Spatial cells:
{len(lat)} × {len(lon)}
= {len(lat) * len(lon)} cells

Time steps:
{len(ds_1920.time)}

ML rows:
{len(ml_df)}

Variables:
{available}
"""
)

print("Data inspection complete.")