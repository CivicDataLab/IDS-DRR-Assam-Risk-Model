# FRIMS Daily Reports Scraper

The Assam Disaster Management Authority (ASDMA) instituted a robust data collection system called Flood Reporting and Information Management System [(FRIMS)](http://www.asdma.gov.in/reports.html), which updates data of flood damages and relief efforts of the government on a daily basis.

This data is made available in the form of PDFs by the ASDMA making them not machine-readable. The following web scraper codes thus help to organise the FRIMS data in CSVs, so that the data can be used for further analysis.

## Directory Tree:
1. [FRIMS_Reports](): All downloaded FRIMS PDFs are stored here.
2. [Data](): The scraped and cleaned data are stored here.

## Notebooks:
1. [FRIMS_DailyReports_2022](): This notebook scrapes all PDFs published by FRIMS in 2022 and produces clean CSVs of damages and relief efforts data. It is a semi-automatic scraper: few PDFs that could not be scraped have to be manually scraped.
2. [FRIMS_InformationExtraction_2022](): This notebook works on the CSVs scraped by the the above notebook and calculates the number of damages and relief efforts in each revenue circle. 
3. [FRIMS_Cumulative_Reports](): This notebook scrapes the cumulative data shared by the ASDMA and calculates number of damages and relief efforts in each revenue circle, per year.

## Scraped and cleaned data:
1. FRIMS 2022: [IDEA-FRM past_damages](https://github.com/CivicDataLab/IDEA-FRM/tree/main/past_damages)

If you want to contribute to the data sources or have any doubts with the data, please contact us at info@civicdatalab.in