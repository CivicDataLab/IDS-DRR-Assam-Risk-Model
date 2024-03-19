# Mission Antyodaya 2020
Under Mission Antyodaya, data is collected for every village in India for various socio economic indicators.
We took [Mission Antyodaya 2020 data](https://docs.google.com/spreadsheets/d/1jVhsf9N410T2LwIN9-GJ0wNI1r_SEbKp/edit?usp=sharing&ouid=109659935473365455052&rtpof=true&sd=true) to collect a few variables that explain vulnerability and exposure.

**Variables extracted from the source that are used in the risk score calculation:**

Original Mission Antyodaya data does not have revenue circle information. We tagged villages to a Revenue Circle based on lat-lon information, LGD Codes etc., and then processed to calculate variables. Methodology of processing can be found here: [Link](https://docs.google.com/document/d/1_wt-wO18sa5iQBy3b-WpSHDjCqRl3MeN67N1v3dTZtQ/edit#heading=h.9ja8pjh1oic)

1. `total_hhd`: Total number of households
2. `net-sown-area-in-hac`: Net sown area in the Revenue Circle.
3.  `avg-electricity`: Average availablity of domestic electricity
4. `avg-tele`: Average availablity of telecom services
5. `rc-piped-hhds-pct`: Percentage of households with piped water connection
6. `rc-nosanitation-hhds-pct`: Percentage of households without sanitation facilities

# Project structure
- `data`: Contains all datasets created.
- `scripts`: Contains codes to transform the raw data.
    - `Transformer.ipynb`: Original Mission Antyodaya data does not have revenue circle information. We tagged villages to a Revenue Circle based on lat-lon information, LGD Codes etc., and then processed to calculate variables. Methodology of processing can be found here: [Link](https://docs.google.com/document/d/1_wt-wO18sa5iQBy3b-WpSHDjCqRl3MeN67N1v3dTZtQ/edit#heading=h.9ja8pjh1oic)
