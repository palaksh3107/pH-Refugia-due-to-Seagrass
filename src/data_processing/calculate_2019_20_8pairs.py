import pandas as pd
import numpy as np
import xarray as xr
import PyCO2SYS as pyco2

# ============================================================
# FILE PATHS
# ============================================================

COPERNICUS_FILE = r"C:\Pyhton\cmems_obs-mob_glo_bgc-car_my_irr-i_1788042515626.nc"

SOCAT_FILE = r"C:\Pyhton\SOCATv2023_qrtrdeg_gridded_coast_monthly.csv"


# ============================================================
# 8 SEAGRASS / OPEN-WATER PAIRS
# ============================================================

pairs = [
    (1, 24.875, -77.375, 24.875, -77.625),
    (2, 24.625, -76.875, 24.625, -76.625),
    (3, 23.125, -78.375, 23.125, -78.875),
    (4, 22.875, -78.375, 22.875, -78.625),
    (5, 22.875, -78.125, 22.625, -78.125),
    (6, 22.375, -77.375, 22.125, -77.125),
    (7, 22.875, -77.875, 22.625, -78.125),
    (8, 22.375, -77.375, 22.125, -77.375),
]


# ============================================================
# 1. LOAD SOCAT
# ============================================================

print("\nLoading SOCAT...")

socat = pd.read_csv(
    SOCAT_FILE,
    skiprows=253
)

socat.columns = socat.columns.str.strip()

socat["DATE"] = pd.to_datetime(socat["DATE"])

# Keep only 2019–2020
socat = socat[
    socat["DATE"].dt.year.isin([2019, 2020])
].copy()

socat["month"] = socat["DATE"].dt.to_period("M").astype(str)

print("SOCAT loaded.")
print("2019–2020 records:", len(socat))


# ============================================================
# 2. LOAD COPERNICUS
# ============================================================

print("\nLoading Copernicus...")

ds = xr.open_dataset(COPERNICUS_FILE)

print("Copernicus loaded.")

print(
    "Copernicus period:",
    str(ds.time.values[0]),
    "to",
    str(ds.time.values[-1])
)


# ============================================================
# 3. FUNCTION TO EXTRACT COPERNICUS
# ============================================================

def get_copernicus(lat, lon):

    point = ds.sel(
        latitude=lat,
        longitude=lon,
        method="nearest"
    )

    rows = []

    for i in range(len(ds.time)):

        date = pd.Timestamp(ds.time.values[i])

        # Only 2019–2020
        if date.year not in [2019, 2020]:
            continue

        dic = point["tco2"].isel(time=i).values
        ta = point["talk"].isel(time=i).values
        cop_ph = point["ph"].isel(time=i).values
        omega = point["omega_ar"].isel(time=i).values

        if (
            np.isfinite(dic) and
            np.isfinite(ta)
        ):

            rows.append({
                "month": date.strftime("%Y-%m"),
                "grid_lat": float(point.latitude.values),
                "grid_lon": float(point.longitude.values),
                "DIC": float(dic),
                "TA": float(ta),
                "Copernicus_pH": float(cop_ph)
                    if np.isfinite(cop_ph)
                    else np.nan,
                "Copernicus_Omega_ar": float(omega)
                    if np.isfinite(omega)
                    else np.nan
            })

    return pd.DataFrame(rows)


# ============================================================
# 4. FUNCTION TO EXTRACT SOCAT
# ============================================================

def get_socat(lat, lon):

    point = socat[
        (np.isclose(socat["LAT"], lat)) &
        (np.isclose(socat["LON"], lon))
    ].copy()

    rows = []

    for month, group in point.groupby("month"):

        row = group.iloc[0]

        sst_count = row["COAST_SST_COUNT_NOBS"]
        sal_count = row["COAST_SALINITY_COUNT_NOBS"]

        # Require both SST and salinity
        if (
            pd.notna(sst_count) and
            sst_count > 0 and
            pd.notna(sal_count) and
            sal_count > 0
        ):

            rows.append({
                "month": month,

                "SST": row["COAST_SST_AVE_UNWTD"],

                "Salinity": row["COAST_SALINITY_AVE_UNWTD"],

                "SST_nobs": sst_count,

                "Salinity_nobs": sal_count
            })

    return pd.DataFrame(rows)


# ============================================================
# 5. PROCESS ALL 8 PAIRS
# ============================================================

all_results = []


for pair_no, sg_lat, sg_lon, ow_lat, ow_lon in pairs:

    print("\n")
    print("=" * 70)
    print(f"PROCESSING PAIR {pair_no}")
    print("=" * 70)

    print(
        f"Seagrass   : {sg_lat}, {sg_lon}"
    )

    print(
        f"Open water : {ow_lat}, {ow_lon}"
    )


    # --------------------------------------------------------
    # COPERNICUS
    # --------------------------------------------------------

    sg_cop = get_copernicus(
        sg_lat,
        sg_lon
    )

    ow_cop = get_copernicus(
        ow_lat,
        ow_lon
    )


    # --------------------------------------------------------
    # SOCAT
    # --------------------------------------------------------

    sg_soc = get_socat(
        sg_lat,
        sg_lon
    )

    ow_soc = get_socat(
        ow_lat,
        ow_lon
    )


    # --------------------------------------------------------
    # MERGE SEAGRASS
    # --------------------------------------------------------

    sg = pd.merge(
        sg_cop,
        sg_soc,
        on="month",
        how="inner"
    )


    # --------------------------------------------------------
    # MERGE OPEN WATER
    # --------------------------------------------------------

    ow = pd.merge(
        ow_cop,
        ow_soc,
        on="month",
        how="inner"
    )


    # --------------------------------------------------------
    # RENAME
    # --------------------------------------------------------

    sg = sg.rename(columns={
        "DIC": "DIC_SG",
        "TA": "TA_SG",
        "SST": "SST_SG",
        "Salinity": "Salinity_SG",
        "Copernicus_pH": "Copernicus_pH_SG",
        "Copernicus_Omega_ar": "Copernicus_Omega_ar_SG"
    })

    ow = ow.rename(columns={
        "DIC": "DIC_OW",
        "TA": "TA_OW",
        "SST": "SST_OW",
        "Salinity": "Salinity_OW",
        "Copernicus_pH": "Copernicus_pH_OW",
        "Copernicus_Omega_ar": "Copernicus_Omega_ar_OW"
    })


    # --------------------------------------------------------
    # MATCH SG + OW MONTHS
    # --------------------------------------------------------

    merged = pd.merge(
        sg,
        ow,
        on="month",
        how="inner",
        suffixes=("_SG", "_OW")
    )


    print(
        f"Common valid months: {len(merged)}"
    )


    # ========================================================
    # PYCO2SYS CALCULATION
    # ========================================================

    for _, row in merged.iterrows():

        try:

            # ------------------------------------------------
            # SEAGRASS
            # ------------------------------------------------

            sg_result = pyco2.sys(
                par1=row["DIC_SG"],
                par2=row["TA_SG"],
                par1_type=2,       # DIC
                par2_type=1,       # TA
                temperature=row["SST_SG"],
                salinity=row["Salinity_SG"]
            )


            # ------------------------------------------------
            # OPEN WATER
            # ------------------------------------------------

            ow_result = pyco2.sys(
                par1=row["DIC_OW"],
                par2=row["TA_OW"],
                par1_type=2,
                par2_type=1,
                temperature=row["SST_OW"],
                salinity=row["Salinity_OW"]
            )


            pH_sg = float(
                np.asarray(sg_result["pH_total"]).squeeze()
            )

            pH_ow = float(
                np.asarray(ow_result["pH_total"]).squeeze()
            )


            omega_sg = float(
                np.asarray(
                    sg_result["saturation_aragonite"]
                ).squeeze()
            )

            omega_ow = float(
                np.asarray(
                    ow_result["saturation_aragonite"]
                ).squeeze()
            )


            # ------------------------------------------------
            # DIFFERENCES
            # ------------------------------------------------

            delta_ph = pH_sg - pH_ow

            delta_omega = omega_sg - omega_ow


            # ------------------------------------------------
            # SAVE
            # ------------------------------------------------

            all_results.append({

                "Pair": pair_no,

                "Month": row["month"],

                "SG_Lat": sg_lat,
                "SG_Lon": sg_lon,

                "OW_Lat": ow_lat,
                "OW_Lon": ow_lon,

                "DIC_SG": row["DIC_SG"],
                "TA_SG": row["TA_SG"],
                "SST_SG": row["SST_SG"],
                "Salinity_SG": row["Salinity_SG"],

                "DIC_OW": row["DIC_OW"],
                "TA_OW": row["TA_OW"],
                "SST_OW": row["SST_OW"],
                "Salinity_OW": row["Salinity_OW"],

                "pH_SG": pH_sg,
                "pH_OW": pH_ow,

                "Delta_pH": delta_ph,

                "Omega_ar_SG": omega_sg,
                "Omega_ar_OW": omega_ow,

                "Delta_Omega_ar": delta_omega,

                "Copernicus_pH_SG":
                    row["Copernicus_pH_SG"],

                "Copernicus_pH_OW":
                    row["Copernicus_pH_OW"],

                "pH_validation_SG":
                    pH_sg - row["Copernicus_pH_SG"],

                "pH_validation_OW":
                    pH_ow - row["Copernicus_pH_OW"],

                "SOCAT_SST_nobs_SG":
                    row["SST_nobs_SG"],

                "SOCAT_Salinity_nobs_SG":
                    row["Salinity_nobs_SG"],

                "SOCAT_SST_nobs_OW":
                    row["SST_nobs_OW"],

                "SOCAT_Salinity_nobs_OW":
                    row["Salinity_nobs_OW"]
            })


        except Exception as e:

            print(
                f"ERROR Pair {pair_no}, "
                f"{row['month']}: {e}"
            )


# ============================================================
# CONVERT TO DATAFRAME
# ============================================================

results = pd.DataFrame(all_results)


# ============================================================
# SAVE PAIRWISE RESULTS
# ============================================================

pair_output = (
    r"C:\Pyhton\PyCO2SYS_2019_20_8pair_results.csv"
)

results.to_csv(
    pair_output,
    index=False
)


# ============================================================
# MONTHLY REGIONAL SUMMARY
# ============================================================

monthly = (
    results
    .groupby("Month")
    .agg(
        n_pairs=("Delta_pH", "count"),

        Mean_Delta_pH=("Delta_pH", "mean"),

        SD_Delta_pH=("Delta_pH", "std"),

        Mean_Delta_Omega_ar=("Delta_Omega_ar", "mean"),

        SD_Delta_Omega_ar=("Delta_Omega_ar", "std"),

        Mean_pH_SG=("pH_SG", "mean"),

        Mean_pH_OW=("pH_OW", "mean"),

        Mean_DIC_SG=("DIC_SG", "mean"),

        Mean_DIC_OW=("DIC_OW", "mean"),

        Mean_TA_SG=("TA_SG", "mean"),

        Mean_TA_OW=("TA_OW", "mean")
    )
    .reset_index()
)


# Standard error

monthly["SE_Delta_pH"] = (
    monthly["SD_Delta_pH"] /
    np.sqrt(monthly["n_pairs"])
)

monthly["SE_Delta_Omega_ar"] = (
    monthly["SD_Delta_Omega_ar"] /
    np.sqrt(monthly["n_pairs"])
)


# ============================================================
# SAVE MONTHLY SUMMARY
# ============================================================

monthly_output = (
    r"C:\Pyhton\PyCO2SYS_2019_20_monthly_summary.csv"
)

monthly.to_csv(
    monthly_output,
    index=False
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("2019–2020 MONTHLY REGIONAL RESULTS")
print("=" * 70)

if len(monthly) > 0:

    print(
        monthly.to_string(index=False)
    )

else:

    print("NO VALID RESULTS FOUND.")


# ============================================================
# VALIDATION SUMMARY
# ============================================================

if len(results) > 0:

    print("\n")
    print("=" * 70)
    print("PYCO2SYS vs COPERNICUS pH VALIDATION")
    print("=" * 70)

    print(
        "Mean absolute SG difference:",
        results["pH_validation_SG"]
        .abs()
        .mean()
    )

    print(
        "Mean absolute OW difference:",
        results["pH_validation_OW"]
        .abs()
        .mean()
    )

    print(
        "Overall mean absolute difference:",
        pd.concat([
            results["pH_validation_SG"].abs(),
            results["pH_validation_OW"].abs()
        ]).mean()
    )


print("\n")
print("=" * 70)
print("SAVED")
print("=" * 70)

print(pair_output)
print(monthly_output)

print("\nDone.")