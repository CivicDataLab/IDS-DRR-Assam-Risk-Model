# Tenders
Public procurement datasets are scraped from the [Assam Tenders](https://assamtenders.gov.in/nicgep/app) website.

**Variables extracted from the source:** Count and Sum of Tenders, with various sub types.

**Time Taken to run the script:** 

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `scraper`: Contains codes for scraping tenders from assamtenders.in
        - `scraper_assam_recent_tenders_tender_status.py`: Scrapes tenders from [Assam Tenders](https://assamtenders.gov.in/nicgep/app). Takes year and month as system arguments. Eg: `python3 ~/scraper_assam_recent_tenders_tender_status.py 2023 6`
        - `concatinate_raw_tenders.py`: Creates one csv for each month in the `monthly_tenders` folder in `data`
    - `flood_tenders.py`: Identification of flood tenders
    - `geocode_district.py`: Geocode districts
    - `geocode_rc.py`: Geocode revenue circles
- `data`: Contains datasets generated using the scripts