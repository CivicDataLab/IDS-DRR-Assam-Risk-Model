# Sentinel-2
Sentinel-2 is a wide-swath, high-resolution, multi-spectral imaging mission supporting Copernicus Land Monitoring studies, including the monitoring of vegetation, soil and water cover, as well as observation of inland waterways and coastal areas. Check this [link](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED#description) for more details.

![Alt text](<docs/IDS-DRR ETL SENTINEL.jpg>)

**Variables extracted from the source:** NDVI and NDBI

**Time Taken to run the script:** 
307 seconds with `scale=1000m`

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `sentinel.py`: Calculates mean NDVI and NDBI indices for each revenue circle in Assam for a given time range
- `data`: Contains datasets generated using the scripts

