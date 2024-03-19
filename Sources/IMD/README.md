# IMD
Aggregate rainfall data from IMD (Indian Meteorological Department) for each revenue circle in Assam - on a monthly basis.

**Variables extracted from the source:** 
1. `max_rain`: Maximum rainfall value in the revenue circle
2. `mean_rain`: Mean rainfall value in the revenue circle
3. `sum_rain`: Sum rainfall value in the revenue circle

## Project Structure

-   `scripts` : Contains the scripts used to obtain the data
    -   `main.py`: Downloads the RAINFALL data for Assam.
-   `data`: Contains datasets generated using the scripts
