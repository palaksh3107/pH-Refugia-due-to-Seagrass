import pandas as pd
import numpy as np
import xarray as xr


# ============================================================
# FILES
# ============================================================

SOCAT_FILE = r"C:\Pyhton\SOCATv2023_qrtrdeg_gridded_coast_monthly.csv"

COPERNICUS_FILE = r"C:\Pyhton\cmems_obs-mob_glo_bgc-car_my_irr-i_1788027948077.nc"


# ============================================================
# SIX SEAGRASS / OPEN-WATER PAIRS
# ============================================================

pairs = [
    (1, 24.875, -77.375, 24.875, -77.625),
    (2, 24.625, -76.875, 24.625, -76.625),
    (3, 23.125, -78.375, 23.125, -78.875),
    (4, 22.875, -78.375, 22.875, -78.625),
    (5, 22.875, -78.125, 22.625, -78.125),
    (6, 22.375, -77.375, 22.125, -77.125),
]


# ============================================================
# LOAD SOCAT
# ============================================================

print("Loading SOCAT...")

socat = pd.read_csv(
    SOCAT_FILE,
    skiprows=253
)

socat.columns = socat.columns.str.strip()

socat["DATE"] = pd.to_datetime(socat["DATE"])

socat["month"] = socat["DATE"].dt.to_period("M")

print("SOCAT loaded.")
print("Columns found:")
print(socat.columns.tolist())


# ============================================================
# LOAD COPERNICUS
# ============================================================

print("\nLoading Copernicus...")

ds = xr.open_dataset(COPERNICUS_FILE)

print("Copernicus loaded.")

print(
    "\nCopernicus time range:",
    str(ds.time.values[0]),
    "to",
    str(ds.time.values[-1])
)


# ============================================================
# FUNCTION: CHECK SOCAT POINT
# ============================================================

def check_socat(lat, lon):

    # Find nearest SOCAT grid cell
    point = socat[
        (np.isclose(socat["LAT"], lat)) &
        (np.isclose(socat["LON"], lon))
    ].copy()

    available = []

    for month, group in point.groupby("month"):

        if len(group) == 0:
            continue

        row = group.iloc[0]

        fco2 = row["COAST_FCO2_COUNT_NOBS"]
        sst = row["COAST_SST_COUNT_NOBS"]
        sal = row["COAST_SALINITY_COUNT_NOBS"]

        if (
            pd.notna(fco2) and fco2 > 0 and
            pd.notna(sst) and sst > 0 and
            pd.notna(sal) and sal > 0
        ):
            available.append(str(month))

    return available


# ============================================================
# FUNCTION: CHECK COPERNICUS POINT
# ============================================================

def check_copernicus(lat, lon):

    point = ds.sel(
        latitude=lat,
        longitude=lon,
        method="nearest"
    )

    valid = []

    for i in range(len(ds.time)):

        time = ds.time.values[i]

        dic = point["tco2"].isel(time=i).values
        ta = point["talk"].isel(time=i).values
        ph = point["ph"].isel(time=i).values

        if (
            np.isfinite(dic) and
            np.isfinite(ta) and
            np.isfinite(ph)
        ):

            month = pd.Timestamp(time).strftime("%Y-%m")

            valid.append(month)

    return valid


# ============================================================
# CHECK ALL PAIRS
# ============================================================

all_results = []

for pair_no, sg_lat, sg_lon, ow_lat, ow_lon in pairs:

    print("\n")
    print("=" * 70)
    print("PAIR", pair_no)
    print("=" * 70)

    print(
        f"Seagrass:  {sg_lat}, {sg_lon}"
    )

    print(
        f"Open water: {ow_lat}, {ow_lon}"
    )

    # --------------------------------------------------------
    # SOCAT
    # --------------------------------------------------------

    sg_socat = check_socat(
        sg_lat,
        sg_lon
    )

    ow_socat = check_socat(
        ow_lat,
        ow_lon
    )

    common_socat = sorted(
        set(sg_socat) & set(ow_socat)
    )

    print("\nSOCAT")

    print(
        "Seagrass months:",
        len(sg_socat)
    )

    print(
        sg_socat
    )

    print(
        "Open-water months:",
        len(ow_socat)
    )

    print(
        ow_socat
    )

    print(
        "COMMON months:",
        len(common_socat)
    )

    print(
        common_socat
    )


    # --------------------------------------------------------
    # COPERNICUS
    # --------------------------------------------------------

    sg_cop = check_copernicus(
        sg_lat,
        sg_lon
    )

    ow_cop = check_copernicus(
        ow_lat,
        ow_lon
    )

    common_cop = sorted(
        set(sg_cop) & set(ow_cop)
    )

    print("\nCOPERNICUS")

    print(
        "Seagrass months:",
        len(sg_cop)
    )

    print(
        sg_cop
    )

    print(
        "Open-water months:",
        len(ow_cop)
    )

    print(
        ow_cop
    )

    print(
        "COMMON months:",
        len(common_cop)
    )

    print(
        common_cop
    )


    # --------------------------------------------------------
    # FULL COMMON MONTHS
    # --------------------------------------------------------

    full_common = sorted(
        set(common_socat) &
        set(common_cop)
    )

    print("\nFULL PIPELINE COMMON MONTHS")

    print(
        "Months available in BOTH SOCAT and Copernicus:",
        len(full_common)
    )

    print(
        full_common
    )


    all_results.append({

        "pair": pair_no,

        "SOCAT_common_months":
            len(common_socat),

        "Copernicus_common_months":
            len(common_cop),

        "Full_pipeline_months":
            len(full_common),

        "Full_pipeline_month_list":
            ", ".join(full_common)
    })


# ============================================================
# SUMMARY
# ============================================================

summary = pd.DataFrame(all_results)

print("\n")
print("=" * 70)
print("FINAL PAIR COVERAGE SUMMARY")
print("=" * 70)

print(
    summary.to_string(index=False)
)


# ============================================================
# SAVE
# ============================================================

output = r"C:\Pyhton\Six_pair_coverage.csv"

summary.to_csv(
    output,
    index=False
)

print("\nSaved:")
print(output)