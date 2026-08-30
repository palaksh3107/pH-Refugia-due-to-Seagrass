import pandas as pd
import xarray as xr
import PyCO2SYS as pyco2

# ============================================================
# FILES
# ============================================================

copernicus_csv = r"C:\Pyhton\Copernicus_Seagrass_OpenWater_DIC_TA.csv"
socat_csv = r"C:\Pyhton\SOCAT_Seagrass_OpenWater_monthly.csv"
netcdf_file = r"C:\Pyhton\cmems_obs-mob_glo_bgc-car_my_irr-i_1788027948077.nc"


# ============================================================
# READ FILES
# ============================================================

cop = pd.read_csv(copernicus_csv)
socat = pd.read_csv(socat_csv)

cop["time"] = pd.to_datetime(cop["time"])
socat["DATE"] = pd.to_datetime(socat["DATE"])

cop["month"] = cop["time"].dt.to_period("M")
socat["month"] = socat["DATE"].dt.to_period("M")

print("Files loaded successfully")


# ============================================================
# OPEN NETCDF
# ============================================================

ds = xr.open_dataset(netcdf_file)

print("NetCDF loaded successfully")


# ============================================================
# MONTHS
# ============================================================

common_months = [
    "2019-03",
    "2019-04",
    "2019-06",
    "2019-07"
]

print("\nMonths being validated:")
print(common_months)


# ============================================================
# LOOP THROUGH LOCATIONS AND MONTHS
# ============================================================

results = []

for location in ["Seagrass", "Open_Water"]:

    print("\nProcessing:", location)

    for month_string in common_months:

        month = pd.Period(month_string, freq="M")

        # ----------------------------------------------------
        # SOCAT
        # ----------------------------------------------------

        s = socat[
            (socat["Location"] == location) &
            (socat["month"] == month)
        ]

        if len(s) == 0:
            print("  No SOCAT data:", month_string)
            continue

        s = s.iloc[0]

        # ----------------------------------------------------
        # Copernicus CSV
        # ----------------------------------------------------

        c = cop[
            (cop["location"] == location) &
            (cop["month"] == month)
        ]

        if len(c) == 0:
            print("  No Copernicus data:", month_string)
            continue

        c = c.iloc[0]

        # ----------------------------------------------------
        # Values
        # ----------------------------------------------------

        dic = float(c["DIC_tco2"])
        ta = float(c["TA_talk"])

        temperature = float(
            s["COAST_SST_AVE_UNWTD"]
        )

        salinity = float(
            s["COAST_SALINITY_AVE_UNWTD"]
        )

        # ----------------------------------------------------
        # PyCO2SYS
        # ----------------------------------------------------

        result = pyco2.sys(
            par1=dic,
            par2=ta,
            par1_type=2,
            par2_type=1,
            temperature=temperature,
            salinity=salinity,
            pressure=0
        )

        pyco2_ph = float(
            result["pH_total"]
        )

        # ----------------------------------------------------
        # ORIGINAL COPERNICUS pH
        # ----------------------------------------------------

        original = ds.sel(
            latitude=float(c["grid_lat"]),
            longitude=float(c["grid_lon"]),
            time=c["time"],
            method="nearest"
        )

        copernicus_ph = float(
            original["ph"].values
        )

        difference = pyco2_ph - copernicus_ph

        print(
            f"  {month_string}: "
            f"PyCO2SYS={pyco2_ph:.6f}, "
            f"Copernicus={copernicus_ph:.6f}, "
            f"Difference={difference:.6f}"
        )

        results.append({
            "Location": location,
            "Month": month_string,
            "Latitude": c["grid_lat"],
            "Longitude": c["grid_lon"],
            "DIC": dic,
            "TA": ta,
            "SST": temperature,
            "Salinity": salinity,
            "PyCO2SYS_pH": pyco2_ph,
            "Copernicus_pH": copernicus_ph,
            "Difference": difference,
            "Absolute_Difference": abs(difference)
        })


# ============================================================
# RESULTS
# ============================================================

results_df = pd.DataFrame(results)

print("\n==============================================")
print("PH VALIDATION RESULTS")
print("==============================================")

print(results_df.to_string(index=False))


# ============================================================
# STATISTICS
# ============================================================

print("\n==============================================")
print("VALIDATION STATISTICS")
print("==============================================")

print(
    "Mean absolute difference:",
    results_df["Absolute_Difference"].mean()
)

print(
    "Maximum absolute difference:",
    results_df["Absolute_Difference"].max()
)


# ============================================================
# SAVE
# ============================================================

output = r"C:\Pyhton\Copernicus_pH_validation.csv"

results_df.to_csv(
    output,
    index=False
)

print("\nSaved:")
print(output)