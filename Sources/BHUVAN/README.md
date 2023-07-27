# BHUVAN Disaster Services
BHUVAN Disaster Services provides inundation maps of various flood events in India. Check this [link](https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php?id=flood) for more details.

**Variables extracted from the source:** `inundation`

**Time Taken to run the scripts:**

All tiles downloaded - Time Taken: 345.03382126099996 seconds
Vertical Images created - Time Taken: 36.502292907000026 seconds
Horizontal stitch - Time Taken: 25.73003852100004 seconds
PNG save - Time Taken: 6.136171567000019 seconds
NC save - Time Taken: 6.4725895149999815 seconds
Tiff save - Time Taken: 9.237463594000019 seconds

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `get_dates.py`: Scrapes the BHUVAN portal to get all the dates on which the flood inundation maps are available for Assam
    - `scrapebhuvan.py`: Scrapes all 13680 tiles from BHUVAN and creates a flood inundation raster by georeferencing them. This [blog](https://medium.com/civicdatalab/tailoring-flood-images-baa169cc53d2) further explains this script.
    - `stitch.py`:
    - `upload_to_s3.py`:

- `data`: Contains datasets generated using the scripts.
    - `PNGs`: Contains flood inundation maps of a given day before geo-referencing.
    - `tiffs`: Contains flood inundation maps of a given day after geo-referencing.


