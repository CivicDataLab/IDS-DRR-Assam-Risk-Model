# WORLDPOP

Population, and housing census are important baseline denominator information for planning. However, these census data aggregated at administrative units are challenging to integrate with other datasets. WorldPop(Lloyd et al., 2019) utilises machine learning to get the correlations between population densities and a range of geographic covariate layers to disaggregate current census-based population counts into 1 km x 1 km and 100x100m grid cells using Random Forest-based dasymetric redistribution.

IDS-DRR uses the [Unconstrained individual countries 2000-2020 UN adjusted (100 m resolution)](https://hub.worldpop.org/geodata/listing?id=29) population counts data estimates for 2017 to 2020 from the WorldPop. The top-down, unconstrained estimation method assumes that no settlement dataset is accurate enough to identify all global residential settlements. Therefore, by disaggregating census databases, the method predicts population numbers for all 100x100 grid cells globally for each year from 2000-2020, leading to a non-zero allocation to all land grid cells. The estimates are adjusted to match the United Nation’s national population estimates. We download the maps from the website, and for the remaining years, we use the annual growth rate calculated from the population estimates of 2015 and 2020 to project the population for 2021, 2022 and 2023.

These rasters are cropped to Assam State extent before processing.

## Project Structure
- `scripts` : Contains the scripts used to process the data
    - `transformer.py`: Calculates sum population for each revenue circle in Assam for each population raster.
- `data`: Contains datasets generated using the scripts
