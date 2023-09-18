# Tenders
Public procurement datasets are scraped from the [Assam Tenders](https://assamtenders.gov.in/nicgep/app) website.

**Variables extracted from the source:** Count and Sum of Tenders, with various sub types.

**Time Taken to run the script:** 

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `scraper`: Contains code for scraping tenders from assamtenders.in
    - `flood_tenders.py`: Identification of flood tenders
    - `geocode_district.py`: Geocode districts
    - `geocode_rc.py`: Geocode revenue circles
- `data`: Contains datasets generated using the scripts