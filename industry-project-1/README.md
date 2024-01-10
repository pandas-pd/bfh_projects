# Industry Project 1
See paper for further detail on the subject and goal

## Steps
0. Data Exploration
    1. Looking at the scada data
    2. Looking at the power curve
1. Join weather forecast data to scada data:
    1. Define an aggregation method (Weighted average)
    2. Define the relevant timeframe for forecasting
    3. Generate a new table according to the method
    4. Transform the wind speed prediction (10m) to match turbine height (100m?)
2. Calculate predicte power output and deviation:
    1. Join the scada data and transformed weather forecast data
    2. Apply the power curve table with the forecast data to get the predicted power output( = y_hat_fc)
    3. Calculate the theoretical output from scada wind speed and power curve (y_hat_th)
    4. Calculate the deviation and mean deviation from the scada data power output (y) from the pc predicted output
    5. Comparing the deviation of the raw vs interpolated values
3. Feature engineering / adding:
    1. Timestamps transformation with sin() and cos()
    2. Add positional data of turbines to scada data
    3. Seasons as categorical data
    4. (Add directional delta (noscol direction - wind direction))
4. Identify biases:
    1. Select a forecast time for identifying biases (=3)
    2. Identify possible reasons for devations / biases E.g. Season, Prediction Time, Park specifice, wind wake, etc.)
    3. Proof or disproof the biases
    4. Compare biases for all three time offsets with interpolated data
5. Correct Biases (normal model):
    1. Create the dataframes
    2. Define a ML model
    3. Train a ML model with [pc_data, aggregatet scada and forecast data, prediction and devition data]
    4. Hyper parameter tuning
6. Correct Biases (gnn model):
    1. Define node and node features (e.g. Turbines)
    2. Define edge and edge features (e.g. Positional relationship)
    3. Train model and optimes for the windpark
7. Compare ML models
    1. Create comparison for the offest
    2. calculate devtation
    3. Decide which performs better on what

Hints:
Calculate power output forecast with pc and weather forecast
- Umrechnung wendspeed (10m) with factor for (100m). See: https://www.energy.gov/eere/articles/wind-turbines-bigger-better
- Mean bias (deviation) -> Summe der Abweichung
- Biases:
- Chracterise (Jahreszeit, Tageszeit (Zielzeit), Anlage, Wake)
    - GNN for Bias correction:
    - Data: all tables can be used
