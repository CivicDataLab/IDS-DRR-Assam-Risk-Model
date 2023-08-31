# NASADEM
NASADEM provides global elevation data at 1 arc second spacing. NASADEM data products were derived from original telemetry data from the Shuttle Radar Topography Mission (SRTM). Check this [link](https://developers.google.com/earth-engine/datasets/catalog/NASA_NASADEM_HGT_001#description) for more details.

![Alt text](<docs/IDS-DRR ETL NASADEM.jpg>)

**Variables extracted from the source:** `Elevation` and `Slope`

**Time Taken to run the script:** ~3 hours at 30m scale.

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `nasadem.py`: Exports the DEM and Slope files for Assam into Google Drive
    - `gdrive.py`: Downloads the DEM and Slope files from Google Drive to server
    - `transformer.py`: Calculates the mean `elevation` and `slope` for each revenue circle in Assam. 
- `data`: Contains datasets generated using the scripts