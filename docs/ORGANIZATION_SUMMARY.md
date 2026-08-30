# Repository Organization Summary

## Overview

The repository has been organized to separate source code, raw and processed data, analysis outputs, figures, GIS files, the final research report, and project documentation.

The structure is designed to make the project easier to navigate, maintain, and reproduce.

---

## Repository Structure

### Root Directory

* `README.md` - Main project overview, methodology, data sources, repository structure, and report link.
* `requirements.txt` - Python dependencies required for the analysis.
* `.gitignore` - Files and datasets excluded from version control.

### `data/`

Contains the datasets used throughout the project.

#### `data/raw/`

Contains original or externally obtained datasets.

* `cmems/` - CMEMS NetCDF marine biogeochemical datasets.
* `glodap/` - GLODAP datasets and Bahamas subsets.
* `seagrass/` - Seagrass meadow boundaries and spatial datasets.
* `socat/` - SOCAT datasets and derived spatial selections.

#### `data/processed/`

Contains datasets generated or transformed during the analysis.

* `copernicus/` - Processed Copernicus outputs and selected cells.
* `pyco2sys/` - PyCO2SYS calculation results and parameter summaries.
* `misc/` - Additional processed analysis information.

### `src/`

Contains the Python source code used in the project.

#### `src/data_extraction/`

Scripts for obtaining and extracting data from the different source datasets.

#### `src/data_processing/`

Scripts for filtering, inspecting, preparing, and processing datasets.

#### `src/carbonate_chemistry/`

Scripts for carbonate-system calculations using PyCO2SYS and related DIC/TA analyses.

#### `src/validation/`

Scripts used for validation of calculated pH and related results.

#### `src/visualization/`

Scripts used to generate project figures and visualizations.

### `analysis/`

Contains the main analysis outputs and summarized results, including Copernicus and PyCO2SYS results.

### `figures/`

Contains project visualizations.

* `final/` - Figures intended for the final analysis and report.
* `workflow/` - Screenshots and images documenting the research workflow.

### `gis/`

Contains the QGIS project used for spatial analysis and visualization.

* `Gis.qgz` - Main QGIS project.

### `report/`

Contains the research report.

* `final/` - Final version of the research report.
* `supplementary/` - Supplementary report material.

### `docs/`

Contains project documentation.

* `PROJECT_HISTORY.md` - Development and analysis timeline.
* `ORGANIZATION_SUMMARY.md` - Description of the repository organization.

---

## Data Management

Large raw datasets are kept separate from processed analysis outputs.

Datasets that are too large for practical version control are excluded using `.gitignore`. Smaller derived datasets required to understand the analysis are retained where appropriate.

The repository does not modify the original raw datasets as part of the organization process; instead, files are separated into `raw` and `processed` locations according to their role in the workflow.

---

## Code Organization

The source code is grouped according to its role in the research workflow:

```text
Data Sources
     |
     v
data_extraction/
     |
     v
data_processing/
     |
     +------------------+
     |                  |
     v                  v
carbonate_chemistry/   validation/
     |
     v
analysis/
     |
     v
visualization/
```

This organization reflects the general progression from data acquisition and processing to carbonate-system calculations, validation, analysis, and visualization.

---

## Final Report

The final research report is located at:

```text
report/final/Bahamas_pH_Refugia_Report_Palaksh.pdf
```

The report is also linked directly from the main `README.md`.

---

## Current Status

The principal data-processing, carbonate-chemistry, analysis, and validation workflows have been developed.

The repository has been reorganized to provide a clearer and more reproducible representation of the research workflow.

---

## Notes

The repository structure may evolve as additional analyses, figures, documentation, or supplementary materials are added.

When adding new files, maintain the separation between:

* Raw data
* Processed data
* Source code
* Analysis outputs
* Final figures
* Documentation
* Report materials
