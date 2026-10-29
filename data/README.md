# Data

This folder holds the datasets used in the project. `raw/` is never modified; every notebook writes its output to `processed/`.

## Provenance

Measurements were taken on 24 individual plants of *Nephrolepis* sp. at the Jardín Botánico de Medellín (Medellín, Antioquia, Colombia). Each individual is identified as `H01`–`H24`. Length and width were measured directly on the frond. Leaf area was extracted from standardized photographs with ImageJ (scale calibration, color thresholding, automated boundary extraction). Sori were counted row by row along the fertile zone, on one side of each pinna pair, and doubled to represent the full pair (bilateral symmetry assumed).

## Raw data (`raw/`)

### `fronds.csv`
One row per individual (24 rows).

| Column | Description | Unit |
|---|---|---|
| `individual_id` | Individual identifier (`H01`–`H24`) | - |
| `frond_length_cm` | Frond length | cm |
| `frond_width_cm` | Frond width | cm |
| `leaf_area_cm2` | Frond area, measured with ImageJ | cm² |
| `n_sori_total` | Total sori count for the frond | count |

### `sori.csv`
One row per pinna-pair position along a frond (1,921 rows).

| Column | Description | Unit |
|---|---|---|
| `individual_id` | Individual identifier, matches `fronds.csv` | - |
| `row_id` | Position of the pinna pair along the frond | - |
| `n_sori_per_row` | Sori counted at that position | count |

### Known issues in the raw data
- **H15** has no row-level records and no `n_sori_total`. Both are imputed in notebooks 02 and 03.
- **H19** had a mismatch between `n_sori_total` and the sum of its row-level counts, caused by a data-entry error. It was corrected against the original field records in notebook 01.

## Processed data (`processed/`)

| File | Created by | Content |
|---|---|---|
| `fronds_clean.csv` | `01_data_cleaning` | Raw fronds table with standardized names/types and the H19 correction |
| `sori_clean.csv` | `01_data_cleaning` | Raw sori table with standardized names/types |
| `fronds_imputed.csv` | `02_total_sori_imputation` | Fronds table with H15's total sori count imputed (Theil-Sen) |
| `sori_imputed.csv` | `03_spatial_distribution_imputation` | Sori table with H15's row-level distribution imputed (weighted KNN-donor) |
| `fronds_density.csv` | `04_sori_density_engineering` | Fronds table with sori density features added |
| `sori_estimation_validation.csv` | `06_sori_estimation_reduced_sampling` | Real vs. estimated total sori counts for the reduced-sampling methods |

Imputed values are flagged with an `is_imputed` column so they can be included or excluded explicitly in any downstream analysis.