import xarray as xr
import pandas as pd
import numpy as np

# ============================================================
# 1. COPERNICUS FILE
# ============================================================

file = r"C:\Pyhton\cmems_obs-mob_glo_bgc-car_my_irr-i_1788027948077.nc"

ds = xr.open_dataset(file)

print("Dataset opened successfully")
print(ds)


# ============================================================
# 2. OUR TWO LOCATIONS
# ============================================================

locations = {
    "Seagrass": {
        "lat": 23.125,
        "lon": -78.375
    },

    "Open_Water": {
        "lat": 23.125,
        "lon": -78.875
    }
}


# ============================================================
# 3. EXTRACT NEAREST COPERNICUS GRID CELL
# ============================================================

results = []

for name, coords in locations.items():

    lat = coords["lat"]
    lon = coords["lon"]

    # Find nearest Copernicus grid cell
    point = ds.sel(
        latitude=lat,
        longitude=lon,
        method="nearest"
    )

    # Actual Copernicus grid coordinates
    grid_lat = float(point.latitude.values)
    grid_lon = float(point.longitude.values)

    print("\n========================================")
    print(name)
    print("========================================")
    print("Requested location:")
    print("Latitude :", lat)
    print("Longitude:", lon)

    print("\nNearest Copernicus grid cell:")
    print("Latitude :", grid_lat)
    print("Longitude:", grid_lon)

    # --------------------------------------------------------
    # Extract variables
    # --------------------------------------------------------

    tco2 = point["tco2"].values
    talk = point["talk"].values

    # Store every available time step
    for i, time in enumerate(point.time.values):

        results.append({
            "location": name,
            "requested_lat": lat,
            "requested_lon": lon,
            "grid_lat": grid_lat,
            "grid_lon": grid_lon,
            "time": pd.Timestamp(time),
            "DIC_tco2": float(tco2[i]),
            "TA_talk": float(talk[i])
        })


# ============================================================
# 4. CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(results)

# Remove invalid values
df = df.replace([-999, -9999, -1e34], np.nan)

# Remove rows where DIC or TA is missing
df = df.dropna(subset=["DIC_tco2", "TA_talk"])


# ============================================================
# 5. PRINT RESULTS
# ============================================================

print("\n\n================================================")
print("COPERNICUS DIC + TA RESULTS")
print("================================================")

print(
    df.to_string(index=False)
)


# ============================================================
# 6. SAVE CSV
# ============================================================

output = r"C:\Pyhton\Copernicus_Seagrass_OpenWater_DIC_TA.csv"

df.to_csv(output, index=False)

print("\n\nSaved:")
print(output)


# ============================================================
# 7. SUMMARY
# ============================================================

print("\n================================================")
print("SUMMARY")
print("================================================")

for location in ["Seagrass", "Open_Water"]:

    subset = df[df["location"] == location]

    print(f"\n{location}")

    print(
        "DIC range:",
        subset["DIC_tco2"].min(),
        "to",
        subset["DIC_tco2"].max(),
        "µmol/kg"
    )

    print(
        "TA range:",
        subset["TA_talk"].min(),
        "to",
        subset["TA_talk"].max(),
        "µmol/kg"
    )