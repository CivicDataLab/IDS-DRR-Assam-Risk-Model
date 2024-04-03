| Source  | Variables | Temporal Resolution |
| ------------- | -------------  | ------------- |
| ANTYODAYA  | `net-sown-area-in-hac`<br>`avg-electricity`<br>`avg-tele`<br>`rc-piped-hhds-pct`<br>`rc-nosanitation-hhds-pct` | One Time |
| BHARAT MAPS    | `Health Centres per RC` <br> `Road length per RC` <br> `Rail length per RC` | One Time |
| BHUVAN  | `Inundation percentage`<br>`Inundation intensity` | Monthly |
| Flood Forecast Stations (FFS)  | `riverlevel_mean`<br>`riverlevel_min`<br>`riverlevel_max`  | Monthly |
| FRIMS  | `All damages variables`  | Monthly |
| GCN250  | `Surface runoff`  | One Time |
| IMD   | `Rainfall`  | Monthly |
| NASADEM   | `Elevation` <br> `Slope`  | One Time |
| NERDRR  | `Proximity to embankment`  | One Time |
| SENTINEL  | `NDVI`<br>`NDBI`  | Monthly |
| TENDERS   | `All Tender related variables`  | Monthly |
| WRIS   | `Distance from rivers` <br>  `Drainage density` | One Time|

*Last updated: April 3, 2024*

A detailed description of each of these variables is available in the [data-dictionary](https://docs.google.com/spreadsheets/d/1z-aNMPA8YuCb6Q4w2nDGi4OhgK9W1jbboskRzYgLUbY/edit#gid=1901128506)


# Master variable preparation

Once each of these variables is created. The following scripts are to be ru to create a master variable CSV, which will be the input to the data model.

1. Run `master.py`  - This will create a timeseries sheet for each variable in the `Sources/master/` folder.
2. Run `master2.py` - This will create a master variables datasheet `MASTER_VARIABLES.csv` in the `RiskScoreModel/data` folder.