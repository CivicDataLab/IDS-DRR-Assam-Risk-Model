# NASADEM
NASADEM provides global elevation data at 1 arc second spacing. NASADEM data products were derived from original telemetry data from the Shuttle Radar Topography Mission (SRTM). Check this [link](https://developers.google.com/earth-engine/datasets/catalog/NASA_NASADEM_HGT_001#description) for more details.

![Alt text](<docs/IDS-DRR ETL SENTINEL.jpg>)

**Variables extracted from the source:** DEM and Slope

**Time Taken to run the script:** 

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `nasadem.py`: Downloads the DEM file for Assam.
- `data`: Contains datasets generated using the scripts