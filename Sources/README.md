
| Source  | Variables | Status | updateFreq |
| ------------- | ------------- | ------------- | ------------- |
| BHUVAN  | `Inundation percentage`<br>`Inundation intensity` | Scripts Reviewed | Monthly |
| SENTINEL  | `NDVI`<br>`NDBI`  | Scripts Reviewed | Monthly |
| TENDERS   | Count, Sum of Tenders  | Wrote Scripts | Quarterly |
| NASADEM   | `Elevation` <br> `Slope`  | Wrote Scripts | One-Time |
| IMD   | `Rainfall`  | Wrote Scripts | Monthly |
| GCN250  | `Surface runoff`  | Wrote Scripts | One-Time |
| BHARAT MAPS    | `Health Centres per RC` <br> `Road length per RC` <br> `Rail length per RC` | Wrote Scripts | One-Time |
| Mission Antyodaya 2020   | - | - | - |
| FRIMS  | `All damages variables` | - | - |
| NERDRR  | `Proximity to embankment`  | - | - |
| WRIS   | `Distance from rivers` <br>  `Drainage density` | - | - |


# Master variable preparation

1. Run `master.py`  - This will create a timeseries sheet for each variable in the `Sources/master/` folder.
2. Run `master2.py` - This will create a master variables datasheet `MASTER_VARIABLES.csv` in the `RiskScoreModel/data` folder.