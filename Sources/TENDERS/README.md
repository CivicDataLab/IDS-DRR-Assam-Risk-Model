# Tenders
Public procurement datasets are scraped from the [Assam Tenders](https://assamtenders.gov.in/nicgep/app) website. Flood tenders are identified and geotagged with revenue circles using the names of villages, revenue circles etc., present in tender work descriptions, IDs etc.

**Variables extracted from the source:** Count and Sum of Tenders, with various sub types.
1. `total-tender-awarded-value`: Total value of flood related tenders
2. `SOPD-tenders-awarded-value`: SOPD Scheme is the State Owned Priority Development Scheme. This variable gives information of total value of tenders that were granted under SOPD Scheme
3. `sdrf-tenders-awarded-value`: This variable gives information of total value of tenders that were granted under State Disaster Response Fund
4. `RIDF-tenders-awarded-value`: RIDF is the Rural Infrastructure Development Fund maintained by NABARD. This variable gives information of total value of tenders that were granted under RIDF.
5. `CIDF-tenders-awarded-value`: CIDF City Infra Development Fund is maintained by Assam Government for urban development. This variable gives information of total value of tenders that were granted under CIDF
6. `restoration-measures-tenders-awarded-value`: This variable gives sum of all tenders that are flagged as Restoration Measures
7. `immediate-measures-tenders-awarded-value`: This variable gives sum of all tenders that are flagged as Immediate Measures
8. `Others-tenders-awarded-value`: Every flood related tender is flagged as either "Preparedness", "Immediate Measure" or "Other" based on key words. This column gives sum of all tenders that are flagged as Other

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `scraper`: Contains codes for scraping tenders from assamtenders.in
        - `scraper_assam_recent_tenders_tender_status.py`: Scrapes tenders from [Assam Tenders](https://assamtenders.gov.in/nicgep/app). Takes year and month as system arguments. Eg: `python3 ~/scraper_assam_recent_tenders_tender_status.py 2023 6`
        - `concatinate_raw_tenders.py`: Creates one csv for each month in the `monthly_tenders` folder in `data`
    - `flood_tenders.py`: Identification of flood tenders
    - `geocode_district.py`: Geocode districts
    - `geocode_rc.py`: Geocode revenue circles
- `data`: Contains datasets generated using the scripts