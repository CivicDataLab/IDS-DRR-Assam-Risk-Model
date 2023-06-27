# FRIMS Daily Reports Scraper
The Assam Disaster Management Authority (ASDMA) instituted a robust data collection system called Flood Reporting and Information Management System [(FRIMS)](http://www.asdma.gov.in/reports.html), which updates data of flood damages and relief efforts of the government on a daily basis.

This data is made available in the form of PDFs by the ASDMA making them not machine-readable. The following web scraper codes thus help to organise the FRIMS data in CSVs, so that the data can be used for further analysis.

## Directory Tree:
1. [FRIMS_Reports](https://github.com/CivicDataLab/IDEA-FRM_Codes/tree/main/Scrapers/FRIMS_Daily_Reports_Scraper/FRIMS_Reports): All downloaded FRIMS PDFs are stored here.
2. [Data](https://github.com/CivicDataLab/IDEA-FRM_Codes/tree/main/Scrapers/FRIMS_Daily_Reports_Scraper/Data): The scraped and cleaned data are stored here.

## Notebooks:
1. [FRIMS_DailyReports_2022](https://github.com/CivicDataLab/IDEA-FRM_Codes/blob/main/Scrapers/FRIMS_Daily_Reports_Scraper/FRIMS_DailyReports_2022.ipynb): This notebook scrapes all PDFs published by FRIMS in 2022 and produces clean CSVs of damages and relief efforts data. It is a semi-automatic scraper: few PDFs that could not be scraped have to be manually scraped.
2. [FRIMS_InformationExtraction_2022](https://github.com/CivicDataLab/IDEA-FRM_Codes/blob/main/Scrapers/FRIMS_Daily_Reports_Scraper/FRIMS_InformationExtraction_2022.ipynb): This notebook works on the CSVs scraped by the the above notebook and calculates the number of damages and relief efforts in each revenue circle. 
3. [FRIMS_Cumulative_Reports](https://github.com/CivicDataLab/IDEA-FRM_Codes/blob/main/Scrapers/FRIMS_Daily_Reports_Scraper/FRIMS_Cumulative_Reports.ipynb): This notebook scrapes the cumulative data shared by the ASDMA and calculates number of damages and relief efforts in each revenue circle, per year.

## Scraped and cleaned data:
1. FRIMS 2022: [IDEA-FRM past_damages](https://github.com/CivicDataLab/IDEA-FRM/tree/main/past_damages)

## 2023
Scraped till 25.06.2023
Few issues with the scraped data - Infra damages
1. South Salmara revenue circle is present in Dhubri district 25th June's FRIMS report. This is not as per maps.
2. Minor discrepancies between overall number of damages reported in a district and number of individual damages reported in `Details` section. Check road damages in `Bongaigaon` on 25th June; `Cachar` on 23rd June for examples.
3. `Dangtol` RC is present in `Bongaigaon` [20th June]. This is not as per maps. Renamed it to `Bongaigaon` RC.
4. At times, RC level split is not available on FRIMS. Check `Kokrajhar` embankments affected on 23rd June for example. 

If you want to contribute to the data sources or have any doubts with the data, please contact us at info@civicdatalab.in
