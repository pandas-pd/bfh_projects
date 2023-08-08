# Import required libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load your time series data into a pandas dataframe
df = pd.read_csv('your_data.csv', parse_dates=['date'], index_col='date')

# Define the number of days to forecast
n_days = 30

# Define the window size
window_size = 30

# Create the target variable for the forecast by shifting the data n_days forward
for i in range(1, n_days+1):
    df[f'target_{i}'] = df['your_variable'].shift(-i)

# Create the features by shifting the data within a window of size window_size
for i in range(1, window_size+1):
    df[f'feat_{i}'] = df['your_variable'].shift(i)

# Drop any rows with missing values (NaN)
df.dropna(inplace=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df.drop(df.columns[-n_days:], axis=1), df[df.columns[-n_days:]], test_size=0.2, random_state=42)

# Create the Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model on the training data
model.fit(X_train, y_train)

# Use the model to generate predictions for the test data
y_pred = model.predict(X_test)

# Calculate the Mean Squared Error (MSE) to evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)

print('MSE: ', mse)