# Scraping Waterlevel data from Flood forecast Stations (FFS)

The Central Water Commission (CWC) collects and maintains water level data from Flood forecast stations. This data is made available by the CWC here - [Link](https://ffs.india-water.gov.in/). 

There are three divisions in Assam. FFS stations are majorly distributed in these divisions
1. Upper Brahmaputra Division, Dibrugarh (UBDDIB)
2. Middle Brahmaputra Divison, Guwahati (MBDGHY)
3. Lower Brahmaputra Division, Jalpaiguri (LBDJPG)


## Project Directory:
1. `scripts`: Contains codes to scrape data from FFS.
    - `scraper.py`: To scrape data from CWC
    - `transformer.py`: To calculate variables
2. `data`: Contains all datasets used and produced for this source.