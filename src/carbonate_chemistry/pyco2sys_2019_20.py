import pandas as pd
import numpy as np
import PyCO2SYS as pyco2

# ============================================================
# 1. FILES
# ============================================================

copernicus_file = r"C:\Pyhton\Copernicus_Seagrass_OpenWater_DIC_TA.csv"
socat_file = r"C:\Pyhton\SOCAT_Seagrass_OpenWater_monthly.csv"

cop = pd.read_csv(copernicus_file)
socat = pd.read_csv(socat_file)

cop["time"] = pd.to_datetime(cop["time"])
socat["DATE"] = pd.to_datetime(socat["DATE"])

cop["month"] = cop["time"].dt.to_period("M")
socat["month"] = socat["DATE"].dt.to_period("M")


# ============================================================
# 2. COMMON MONTHS
# ============================================================

sg_months = set(
    socat.loc[socat["Location"] == "Seagrass", "month"]
)

ow_months = set(
    socat.loc[socat["Location"] == "Open_Water", "month"]
)

common_months = sorted(sg_months.intersection(ow_months))

print("\nCommon months:")
for m in common_months:
    print(m)


# ============================================================
# 3. SOCAT DATA
# ============================================================

sg = socat[
    (socat["Location"] == "Seagrass") &
    (socat["month"].isin(common_months))
].copy()

ow = socat[
    (socat["Location"] == "Open_Water") &
    (socat["month"].isin(common_months))
].copy()

sg = sg.rename(columns={
    "COAST_FCO2_AVE_UNWTD": "fCO2_SG",
    "COAST_SST_AVE_UNWTD": "SST_SG",
    "COAST_SALINITY_AVE_UNWTD": "Salinity_SG"
})

ow = ow.rename(columns={
    "COAST_FCO2_AVE_UNWTD": "fCO2_OW",
    "COAST_SST_AVE_UNWTD": "SST_OW",
    "COAST_SALINITY_AVE_UNWTD": "Salinity_OW"
})

sg = sg[
    ["month", "fCO2_SG", "SST_SG", "Salinity_SG"]
]

ow = ow[
    ["month", "fCO2_OW", "SST_OW", "Salinity_OW"]
]

socat_pair = pd.merge(
    sg,
    ow,
    on="month",
    how="inner"
)


# ============================================================
# 4. COPERNICUS DIC + TA
# ============================================================

sg_cop = cop[
    cop["location"] == "Seagrass"
].copy()

ow_cop = cop[
    cop["location"] == "Open_Water"
].copy()

sg_cop = sg_cop.rename(columns={
    "DIC_tco2": "DIC_SG",
    "TA_talk": "TA_SG"
})

ow_cop = ow_cop.rename(columns={
    "DIC_tco2": "DIC_OW",
    "TA_talk": "TA_OW"
})

sg_cop = sg_cop[
    ["month", "DIC_SG", "TA_SG"]
]

ow_cop = ow_cop[
    ["month", "DIC_OW", "TA_OW"]
]

cop_pair = pd.merge(
    sg_cop,
    ow_cop,
    on="month",
    how="inner"
)


# ============================================================
# 5. COMBINE
# ============================================================

data = pd.merge(
    socat_pair,
    cop_pair,
    on="month",
    how="inner"
)

data = data.sort_values("month").reset_index(drop=True)

print("\n==============================================")
print("FINAL INPUT DATA")
print("==============================================")

print(data.to_string(index=False))


# ============================================================
# 6. CALCULATIONS
# ============================================================

results = []

for _, row in data.iterrows():

    # ========================================================
    # A. PRIMARY METHOD
    # DIC + TA + SST + Salinity
    # ========================================================

    sg_dic_result = pyco2.sys(
        par1=row["DIC_SG"],
        par2=row["TA_SG"],
        par1_type=2,
        par2_type=1,
        salinity=row["Salinity_SG"],
        temperature=row["SST_SG"],
        pressure=0
    )

    ow_dic_result = pyco2.sys(
        par1=row["DIC_OW"],
        par2=row["TA_OW"],
        par1_type=2,
        par2_type=1,
        salinity=row["Salinity_OW"],
        temperature=row["SST_OW"],
        pressure=0
    )

    pH_SG_DIC = float(sg_dic_result["pH_total"])
    pH_OW_DIC = float(ow_dic_result["pH_total"])

    omega_SG_DIC = float(
        sg_dic_result["saturation_aragonite"]
    )

    omega_OW_DIC = float(
        ow_dic_result["saturation_aragonite"]
    )


    # ========================================================
    # B. INDEPENDENT VALIDATION
    # fCO2 + TA + SST + Salinity
    # ========================================================

    sg_fco2_result = pyco2.sys(
        par1=row["fCO2_SG"],
        par2=row["TA_SG"],
        par1_type=5,
        par2_type=1,
        salinity=row["Salinity_SG"],
        temperature=row["SST_SG"],
        pressure=0
    )

    ow_fco2_result = pyco2.sys(
        par1=row["fCO2_OW"],
        par2=row["TA_OW"],
        par1_type=5,
        par2_type=1,
        salinity=row["Salinity_OW"],
        temperature=row["SST_OW"],
        pressure=0
    )

    pH_SG_FCO2 = float(sg_fco2_result["pH_total"])
    pH_OW_FCO2 = float(ow_fco2_result["pH_total"])

    DIC_SG_FCO2 = float(
        sg_fco2_result["dic"]
    )

    DIC_OW_FCO2 = float(
        ow_fco2_result["dic"]
    )

    omega_SG_FCO2 = float(
        sg_fco2_result["saturation_aragonite"]
    )

    omega_OW_FCO2 = float(
        ow_fco2_result["saturation_aragonite"]
    )


    # ========================================================
    # C. STORE RESULTS
    # ========================================================

    results.append({

        "month": str(row["month"]),

        # ---------------- Primary inputs ----------------

        "DIC_SG_Copernicus": row["DIC_SG"],
        "TA_SG_Copernicus": row["TA_SG"],
        "SST_SG_SOCAT": row["SST_SG"],
        "Salinity_SG_SOCAT": row["Salinity_SG"],

        "DIC_OW_Copernicus": row["DIC_OW"],
        "TA_OW_Copernicus": row["TA_OW"],
        "SST_OW_SOCAT": row["SST_OW"],
        "Salinity_OW_SOCAT": row["Salinity_OW"],

        # ---------------- Primary pH ----------------

        "pH_SG_DIC_TA": pH_SG_DIC,
        "pH_OW_DIC_TA": pH_OW_DIC,

        "Delta_pH_DIC_TA":
            pH_SG_DIC - pH_OW_DIC,

        # ---------------- Primary Omega ----------------

        "Omega_SG_DIC_TA": omega_SG_DIC,
        "Omega_OW_DIC_TA": omega_OW_DIC,

        "Delta_Omega_DIC_TA":
            omega_SG_DIC - omega_OW_DIC,

        # ---------------- fCO2 validation ----------------

        "fCO2_SG_SOCAT": row["fCO2_SG"],
        "fCO2_OW_SOCAT": row["fCO2_OW"],

        "pH_SG_fCO2_TA": pH_SG_FCO2,
        "pH_OW_fCO2_TA": pH_OW_FCO2,

        "Delta_pH_fCO2_TA":
            pH_SG_FCO2 - pH_OW_FCO2,

        # ---------------- DIC reconstructed from fCO2 ----------------

        "DIC_SG_from_fCO2": DIC_SG_FCO2,
        "DIC_OW_from_fCO2": DIC_OW_FCO2,

        # ---------------- Omega validation ----------------

        "Omega_SG_fCO2_TA": omega_SG_FCO2,
        "Omega_OW_fCO2_TA": omega_OW_FCO2,

        "Delta_Omega_fCO2_TA":
            omega_SG_FCO2 - omega_OW_FCO2
    })


# ============================================================
# 7. RESULTS
# ============================================================

results_df = pd.DataFrame(results)

print("\n==============================================")
print("PYCO2SYS VALIDATION RESULTS")
print("==============================================")

print(
    results_df[
        [
            "month",

            "pH_SG_DIC_TA",
            "pH_OW_DIC_TA",
            "Delta_pH_DIC_TA",

            "pH_SG_fCO2_TA",
            "pH_OW_fCO2_TA",
            "Delta_pH_fCO2_TA",

            "DIC_SG_from_fCO2",
            "DIC_SG_Copernicus",

            "DIC_OW_from_fCO2",
            "DIC_OW_Copernicus"
        ]
    ].to_string(index=False)
)


# ============================================================
# 8. SAVE
# ============================================================

output = r"C:\Pyhton\PyCO2SYS_Validation.csv"

results_df.to_csv(
    output,
    index=False
)

print("\n==============================================")
print("SAVED")
print("==============================================")

print(output)


# ============================================================
# 9. MEAN COMPARISON
# ============================================================

print("\n==============================================")
print("MEAN RESULTS")
print("==============================================")

print(
    "Mean ΔpH (DIC + TA):",
    results_df["Delta_pH_DIC_TA"].mean()
)

print(
    "Mean ΔpH (fCO2 + TA):",
    results_df["Delta_pH_fCO2_TA"].mean()
)

print(
    "Mean SG DIC difference:",
    (
        results_df["DIC_SG_from_fCO2"]
        - results_df["DIC_SG_Copernicus"]
    ).mean()
)

print(
    "Mean OW DIC difference:",
    (
        results_df["DIC_OW_from_fCO2"]
        - results_df["DIC_OW_Copernicus"]
    ).mean()
)