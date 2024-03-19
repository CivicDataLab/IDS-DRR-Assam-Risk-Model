# GCN250
GCN250 is the global gridded curve numbers data at a spatial resolution of 250m. Curve Numbers are fundamental in rainfall-runoff modelling. The potential application of this data includes hydrologic design, land management applications, flood risk assessment, and groundwater recharge modeling. 

Dataset is sourced from the [Google Earth Engine Community Catalogue](https://gee-community-catalog.org/projects/gcn250/)

You can also visualise this dataset using this [Google Earth Engine App](https://jaafarhadi.users.earthengine.app/view/hydrologic-curve-number) created by the authors of the dataset.


**Variables extracted from the source:** 

1. `mean_cn`: Mean curve numbers help in estimation of Surface runoff

![Alt text](<docs/IDS-DRR ETL GCN250.jpg>)

**Time Taken to run the script:** 
50 seconds

## Project Structure
- `scripts` : Contains the scripts used to obtain the data
    - `gcn250.py`: Calculates mean GCN250 values for each revenue circle in Assam
- `data`: Contains datasets generated using the scripts

