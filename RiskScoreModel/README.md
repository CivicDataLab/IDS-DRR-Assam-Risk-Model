# Risk Score Model

## Steps

After all the variables are prepared, you can calculate the factor scores and the risk score for each revenue circle.

### Calculation of Factor Scores

#### Flood Hazard
...


#### Vulnerability
...

#### Exposure
...

#### Government Response
...


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