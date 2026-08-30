# Seagrass pH Refugia

## Assessing the Potential of Seagrass Meadows to Provide Localized pH Refugia from Ocean Acidification

This repository contains the data, Python scripts, analysis outputs, figures, GIS files, and final report for a research project investigating whether seagrass meadows can create localized carbonate-chemistry conditions that may provide temporary pH refugia from ocean acidification.

The study focuses on seagrass meadows in the Bahamas and compares carbonate-system conditions within or associated with seagrass meadows against nearby open-water conditions. The analysis uses observational and model-derived marine carbonate chemistry datasets and calculates carbonate-system parameters using PyCO2SYS.

---

## Research Objective

The primary objective is to investigate differences in marine carbonate chemistry between seagrass meadow and nearby open-water environments, with particular focus on:

* pH
* Dissolved Inorganic Carbon (DIC)
* Total Alkalinity (TA)
* Delta pH between seagrass and open-water conditions
* Temporal variability in carbonate chemistry
* The potential magnitude and consistency of seagrass-associated pH enhancement

The project also incorporates independent datasets for data validation and explores approaches for dealing with spatial and temporal data gaps.

---

## Study Area

The analysis is focused on seagrass meadows in the Bahamas.

Seagrass meadow locations and spatial boundaries are combined with oceanographic carbonate-chemistry datasets to identify suitable sampling locations and corresponding nearby open-water comparison regions.

---

## Methodology

The overall workflow consists of the following stages:

### 1. Seagrass Spatial Data

Seagrass meadow boundaries and spatial datasets are used to identify the study region and distinguish seagrass-associated locations from nearby open-water locations.

### 2. Spatial Sampling

Candidate locations are selected using the available spatial coverage of the carbonate-chemistry datasets. Seagrass and open-water locations are paired to enable a spatial comparison while maintaining comparable environmental conditions.

### 3. SOCAT Data

Surface-ocean CO2 observations from the Surface Ocean CO2 Atlas (SOCAT) are used to characterize surface carbonate-system variability and provide observational constraints.

### 4. Copernicus Marine Data

Copernicus Marine biogeochemical products are used to obtain gridded marine carbonate-system information and investigate spatial and temporal variability in the study region.

### 5. GLODAP Data

The Global Ocean Data Analysis Project (GLODAP) dataset is used as an independent source for carbonate-system observations and validation.

### 6. DIC and TA Estimation

Dissolved Inorganic Carbon and Total Alkalinity values are combined or estimated for selected locations and time periods where appropriate.

### 7. PyCO2SYS Calculations

The carbonate-system calculations are performed using PyCO2SYS to derive pH and related carbonate parameters from the available input variables.

### 8. Seagrass - Open Water Comparison

Calculated carbonate-system parameters are compared between seagrass-associated and open-water locations to estimate potential pH differences and assess whether the observed differences are consistent with a localized pH-refugia effect.

### 9. Validation and Uncertainty Analysis

Independent observations and alternative parameter scenarios are used to evaluate the reliability and sensitivity of the calculated results.

---

## Data Sources

The project uses data from several complementary sources:

| Dataset                   | Purpose                                                                   |
| ------------------------- | ------------------------------------------------------------------------- |
| SOCAT                     | Surface ocean CO2 observations and temporal/spatial carbonate variability |
| Copernicus Marine Service | Gridded marine biogeochemical data                                        |
| GLODAP                    | Independent carbonate-system observations and validation                  |
| Seagrass spatial datasets | Identification and delineation of seagrass meadows                        |
| PyCO2SYS                  | Carbonate-system calculations and pH estimation                           |

Large source datasets are separated from processed project outputs within the `data/` directory.

---

## Repository Structure

```text
pH-Refugia-due-to-Seagrass/
|
|-- README.md
|-- requirements.txt
|-- .gitignore
|
|-- data/
|   |-- raw/
|   |   |-- cmems/
|   |   |-- glodap/
|   |   |-- seagrass/
|   |   `-- socat/
|   |
|   `-- processed/
|       |-- copernicus/
|       |-- pyco2sys/
|       `-- misc/
|
|-- src/
|   |-- data_extraction/
|   |-- data_processing/
|   |-- carbonate_chemistry/
|   |-- validation/
|   `-- visualization/
|
|-- analysis/
|
|-- figures/
|   |-- final/
|   `-- workflow/
|
|-- gis/
|   `-- Gis.qgz
|
|-- report/
|   |-- final/
|   `-- supplementary/
|
`-- docs/
    |-- PROJECT_HISTORY.md
    `-- ORGANIZATION_SUMMARY.md
```

### Directory Descriptions

* `data/raw/` - Original or externally obtained datasets.
* `data/processed/` - Cleaned, filtered, transformed, or calculated datasets.
* `src/` - Python source code used for extraction, processing, carbonate chemistry, validation, and visualization.
* `analysis/` - Main analysis outputs and summarized results.
* `figures/final/` - Figures intended for presentation or the final report.
* `figures/workflow/` - Screenshots and visual documentation of the analysis workflow.
* `gis/` - QGIS project files and related GIS work.
* `report/final/` - Final research report.
* `docs/` - Project history and repository documentation.

---

## Key Analysis Outputs

The repository contains processed results including:

* Monthly Copernicus carbonate-chemistry results
* PyCO2SYS carbonate-system calculations
* Seagrass versus open-water comparisons
* DIC/TA sensitivity and minimum-maximum scenarios
* Validation results
* Sampling-pair coverage information

The corresponding CSV files can be found in `analysis/` and `data/processed/`.

---

## Final Report

The complete research report is available here:

**[Read the Final Report](report/final/Bahamas_pH_Refugia_Report_Palaksh.pdf)**

The report provides the complete methodology, analysis, results, discussion, limitations, and conclusions of the study.

---

## Reproducibility

The Python environment required for the analysis is specified in:

```text
requirements.txt
```

The main analysis workflow is implemented through the scripts in:

```text
src/
```

Raw datasets that are too large for practical version control are excluded through `.gitignore`. The repository therefore separates source data, processed data, analysis outputs, and code to make the workflow easier to understand and reproduce.

---

## Current Project Status

The main data-processing and carbonate-chemistry workflows have been developed, and the principal analysis and validation steps have been completed.

The repository is currently being organized and documented to provide a clear, reproducible record of the research workflow.

---

## Author

**Palaksh Shah**

Undergraduate Student, Civil Engineering
Indian Institute of Technology Gandhinagar

---

## Acknowledgements

This project makes use of publicly available oceanographic and carbonate-chemistry datasets and open-source scientific software. Individual data sources and software packages are documented within the project materials and final report.
