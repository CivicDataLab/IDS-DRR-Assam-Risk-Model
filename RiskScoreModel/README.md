# Risk Score Model

## Steps

After all the variables are prepared, you can calculate the factor scores and the risk score for each revenue circle.

## Calculation of Factor Scores

### Exposure

![alt text](docs/exposure.jpg)

1. `sum_population` and `total_hhd` variables are considered for the calculation. (add other variables as required)
2. Use min_max scaler to scale these variables for each month.
3. Sum the scaled variables of `sum_population` and `total_hhd`
4. Find mean and standard deviation of the sum calculated above.
5. Then find the `exposure` factor score using the following criteria:

    - If sum <= mean => very low(1) 
    - mean to mean+1std => low(2)
    - mean+1std to mean+2std => medium(3)
    - mean+2std to mean+3std => high(4)
    - sum > mean+3std => very high(5)

`exposure.py` is the code that runs above steps.

Input -- `MASTER_VARIABLES.csv`

Output -- `factor_scores_l1_exposure.csv`

### Flood Hazard
![alt text](docs/hazard.jpg)

1. `inundation_intensity_mean_nonzero` and `inundation_intensity_sum` variables are considered for the calculation. (add other variables as required)

2. Using the following table, calculate class for both these variables, for each revenue circle in each month.

- If sum <= mean => very low(1) 
- mean to mean+1std => low(2)
- mean+1std to mean+2std => medium(3)
- mean+2std to mean+3std => high(4)
- sum > mean+3std => very high(5)

3. Take average of both the classes thus calculated.
4. Then find the `exposure` factor score by rounding the average.

`hazard.py` is the code that runs above steps.

Input -- `MASTER_VARIABLES.csv`

Output -- `factor_scores_l1_hazard.csv`


### Vulnerability
...

### Government Response
...

Output -- `factor_scores.csv`

## Calculation of Risk-Score using TOPSIS

Once the factor scores are calculated for each revenue circle, we use these factor scores to calculate the comprehensive risk-score for each revenue circle. We use TOPSIS for this.

`topsis.py` is the Python module that implements TOPSIS.<br>
`topsis_riskscore.py` is the code that uses the above module to calculate risk score.

TOPSIS requires a weight to each factor. We've considered the following weights based on literature survey

| Factor   | Weight |
| -------- | ------- |
| Flood Hazard  | 4    |
| Vulnerability | 2     |
| Government Response    | 2    |
| Exposure    | 1   |

![alt text](docs/TOPSIS_RISK.jpg)

This is the inner mechanism of TOPSIS:
![alt text](docs/topsis.png)

## References
1. [What is TOPSIS? - By Robert Soczewica](https://robertsoczewica.medium.com/what-is-topsis-b05c50b3cd05)
2. [DEA Pythonic Implementation](https://github.com/wurmen/DEA/tree/master/Functions/basic_DEA_data%26code)