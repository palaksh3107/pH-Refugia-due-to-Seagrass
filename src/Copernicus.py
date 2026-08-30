import xarray as xr

# --------------------------------------------------
# 1. Open Copernicus file
# --------------------------------------------------

file = "cmems_obs-mob_glo_bgc-car_my_irr-i_1788027948077.nc"

ds = xr.open_dataset(file)

# --------------------------------------------------
# 2. ACTUAL STUDY AREA LOCATION
# --------------------------------------------------

lat = 23.1257
lon = -78.6395

# --------------------------------------------------
# 3. Find nearest Copernicus grid cell
# --------------------------------------------------

point = ds.sel(
    latitude=lat,
    longitude=lon,
    method="nearest"
)

print("\n========================================")
print("NEAREST COPERNICUS GRID CELL")
print("========================================")

print("Study latitude :", lat)
print("Study longitude:", lon)

print(
    "Grid latitude  :",
    float(point.latitude.values)
)

print(
    "Grid longitude :",
    float(point.longitude.values)
)


# --------------------------------------------------
# 4. Extract required variables
# --------------------------------------------------

result = point[
    [
        "ph",
        "tco2",
        "talk",
        "spco2",
        "omega_ar",
        "omega_ca"
    ]
]


# --------------------------------------------------
# 5. Convert to dataframe
# --------------------------------------------------

df = result.to_dataframe().reset_index()


# --------------------------------------------------
# 6. Print result
# --------------------------------------------------

print("\n========================================")
print("CARBONATE DATA")
print("========================================")

print(
    df.to_string(index=False)
)


# --------------------------------------------------
# 7. Save
# --------------------------------------------------

df.to_csv(
    "Copernicus_study_area_cell.csv",
    index=False
)

print("\nSaved:")
print("Copernicus_study_area_cell.csv")