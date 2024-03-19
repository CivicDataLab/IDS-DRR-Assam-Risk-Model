# WORLDPOP

Population, and housing census are important baseline denominator information for planning. However, these census data aggregated at administrative units are challenging to integrate with other datasets. WorldPop(Lloyd et al., 2019) utilises machine learning to get the correlations between population densities and a range of geographic covariate layers to disaggregate current census-based population counts into 1 km x 1 km and 100x100m grid cells using Random Forest-based asymmetric redistribution.

IDS-DRR uses the [Unconstrained individual countries 2000-2020 UN adjusted (100 m resolution)](https://hub.worldpop.org/geodata/listing?id=29) population counts data estimates for 2017 to 2020 from the WorldPop. The top-down, unconstrained estimation method assumes that no settlement dataset is accurate enough to identify all global residential settlements. Therefore, by disaggregating census databases, the method predicts population numbers for all 100x100 grid cells globally for each year from 2000-2020, leading to a non-zero allocation to all land grid cells. The estimates are adjusted to match the United Nation’s national population estimates. We download the maps from the website, and for the remaining years, we use the annual growth rate calculated from the population estimates of 2015 and 2020 to project the population for 2021, 2022 and 2023 using [linear regression extrapolation](https://www.measureevaluation.org/resources/training/online-courses-and-resources/non-certificate-courses-and-mini-tutorials/population-analysis-for-planners/lesson-6.html#:~:text=The%20linear%20model%20assumes%20that,similar%20to%20a%20straight%20line).

These rasters are cropped to Assam State extent before processing.

**Variables extracted from the source:**

The rasters are processed to calculate the following variables for each revenue circle in the state of Assam.

1. `sexratio`: Total number of females per 1000 male population
2. `sum-population`: Net sown area in the Revenue Circle.
3.  `sum-aged-population`: Average availablity of domestic electricity
4. `sum-young-population`: Average availablity of telecom services


## Project Structure
- `scripts` : Contains the scripts used to process the data
    - `zonalstats.py`: Calculates `sum_population`, `sexratio`, `sum_aged_population` and `sum_young_population` for each revenue circle in Assam for each population raster. Takes `year` as the system argument. Eg: `python3 ~/zonalstats.py 2016`
    - `projections.py`: Projects the variables for years 2021-2023 through linear regressions extrapolation. Takes the variable name as teh system argument. Eg: `python3 ~/projections.py sum_aged_population`
    - `transformer.py`: Creates variable datasets for model input.

- `data`: Contains datasets generated using the scripts
