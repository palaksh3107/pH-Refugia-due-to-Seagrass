import pandas as pd
import numpy as np
import PyCO2SYS as pyco2


# ============================================================
# INPUT FILE
# ============================================================

FILE = r"C:\Pyhton\PyCO2SYS_2019_20_8pair_results.csv"

df = pd.read_csv(FILE)

print("\nLoaded:")
print(FILE)

print("Total records:", len(df))


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required = [
    "Pair",
    "Month",

    "DIC_SG",
    "TA_SG",
    "SST_SG",
    "Salinity_SG",

    "DIC_OW",
    "TA_OW",
    "SST_OW",
    "Salinity_OW"
]

missing = [
    c for c in required
    if c not in df.columns
]

if missing:
    print("\nERROR: Missing columns:")
    print(missing)
    raise SystemExit


# ============================================================
# FUNCTION TO RUN PYCO2SYS
# ============================================================

def calculate_ph(DIC, TA, SST, Salinity):

    result = pyco2.sys(
        par1=DIC,
        par2=TA,
        par1_type=2,       # DIC
        par2_type=1,       # TA
        temperature=SST,
        salinity=Salinity
    )

    pH = float(
        np.asarray(
            result["pH_total"]
        ).squeeze()
    )

    omega = float(
        np.asarray(
            result["saturation_aragonite"]
        ).squeeze()
    )

    return pH, omega


# ============================================================
# CALCULATE pH FOR EVERY PIXEL
# ============================================================

all_results = []


for _, row in df.iterrows():

    # -----------------------------
    # Meadow
    # -----------------------------

    try:

        pH_SG, omega_SG = calculate_ph(
            row["DIC_SG"],
            row["TA_SG"],
            row["SST_SG"],
            row["Salinity_SG"]
        )

    except Exception:

        pH_SG = np.nan
        omega_SG = np.nan


    # -----------------------------
    # Open water
    # -----------------------------

    try:

        pH_OW, omega_OW = calculate_ph(
            row["DIC_OW"],
            row["TA_OW"],
            row["SST_OW"],
            row["Salinity_OW"]
        )

    except Exception:

        pH_OW = np.nan
        omega_OW = np.nan


    all_results.append({

        "Pair": row["Pair"],
        "Month": row["Month"],

        "DIC_SG": row["DIC_SG"],
        "TA_SG": row["TA_SG"],
        "SST_SG": row["SST_SG"],
        "Salinity_SG": row["Salinity_SG"],

        "DIC_OW": row["DIC_OW"],
        "TA_OW": row["TA_OW"],
        "SST_OW": row["SST_OW"],
        "Salinity_OW": row["Salinity_OW"],

        "pH_SG": pH_SG,
        "pH_OW": pH_OW,

        "Omega_SG": omega_SG,
        "Omega_OW": omega_OW,

        "Delta_pH": pH_SG - pH_OW,

        "Delta_DIC": row["DIC_SG"] - row["DIC_OW"],

        "Delta_TA": row["TA_SG"] - row["TA_OW"]
    })


calc = pd.DataFrame(all_results)


# ============================================================
# FIND BEST COMBINED CARBONATE CONDITIONS
# ============================================================

best_results = []


for month, group in calc.groupby("Month"):

    group = group.dropna(
        subset=["pH_SG", "pH_OW"]
    )

    if len(group) == 0:
        continue


    # --------------------------------------------------------
    # BEST MEADOW:
    # Highest actual pH
    #
    # This automatically incorporates:
    # DIC + TA + SST + Salinity
    # --------------------------------------------------------

    sg_best = group.loc[
        group["pH_SG"].idxmax()
    ]


    # --------------------------------------------------------
    # WORST OPEN WATER:
    # Lowest actual pH
    # --------------------------------------------------------

    ow_worst = group.loc[
        group["pH_OW"].idxmin()
    ]


    # --------------------------------------------------------
    # Combined maximum contrast
    # --------------------------------------------------------

    delta_pH = (
        sg_best["pH_SG"]
        -
        ow_worst["pH_OW"]
    )


    best_results.append({

        "Month": month,

        # Selected pixels
        "Best_Meadow_Pair": int(sg_best["Pair"]),
        "Worst_OpenWater_Pair": int(ow_worst["Pair"]),

        # Meadow
        "DIC_SG": sg_best["DIC_SG"],
        "TA_SG": sg_best["TA_SG"],
        "SST_SG": sg_best["SST_SG"],
        "Salinity_SG": sg_best["Salinity_SG"],
        "pH_SG": sg_best["pH_SG"],
        "Omega_SG": sg_best["Omega_SG"],

        # Open water
        "DIC_OW": ow_worst["DIC_OW"],
        "TA_OW": ow_worst["TA_OW"],
        "SST_OW": ow_worst["SST_OW"],
        "Salinity_OW": ow_worst["Salinity_OW"],
        "pH_OW": ow_worst["pH_OW"],
        "Omega_OW": ow_worst["Omega_OW"],

        # Differences
        "Delta_DIC": (
            sg_best["DIC_SG"]
            -
            ow_worst["DIC_OW"]
        ),

        "Delta_TA": (
            sg_best["TA_SG"]
            -
            ow_worst["TA_OW"]
        ),

        "Delta_pH": delta_pH,

        "Delta_Omega": (
            sg_best["Omega_SG"]
            -
            ow_worst["Omega_OW"]
        )
    })


best = pd.DataFrame(best_results)

best = best.sort_values("Month")


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n")
print("=" * 130)
print("BEST COMBINED DIC + TA CARBONATE CONTRAST")
print("=" * 130)

print(
    best[
        [
            "Month",

            "Best_Meadow_Pair",
            "Worst_OpenWater_Pair",

            "DIC_SG",
            "DIC_OW",
            "Delta_DIC",

            "TA_SG",
            "TA_OW",
            "Delta_TA",

            "pH_SG",
            "pH_OW",
            "Delta_pH",

            "Omega_SG",
            "Omega_OW",
            "Delta_Omega"
        ]
    ].to_string(index=False)
)


# ============================================================
# SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    f"Mean ΔDIC: "
    f"{best['Delta_DIC'].mean():.6f} µmol/kg"
)

print(
    f"Mean ΔTA: "
    f"{best['Delta_TA'].mean():.6f} µmol/kg"
)

print(
    f"Mean ΔpH: "
    f"{best['Delta_pH'].mean():.6f}"
)

print(
    f"Mean ΔΩarag: "
    f"{best['Delta_Omega'].mean():.6f}"
)

print(
    f"\nPositive ΔpH months: "
    f"{(best['Delta_pH'] > 0).sum()}"
)

print(
    f"Negative ΔpH months: "
    f"{(best['Delta_pH'] < 0).sum()}"
)


# ============================================================
# SAVE
# ============================================================

OUTPUT = (
    r"C:\Pyhton\BestCase_DIC_TA_PyCO2SYS_2019_20.csv"
)

best.to_csv(
    OUTPUT,
    index=False
)

print("\n")
print("=" * 70)
print("SAVED")
print("=" * 70)

print(OUTPUT)

print("\nDone.")