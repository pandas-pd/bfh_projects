import pandas as pd
from pandas.api.types import is_object_dtype, is_numeric_dtype

def dtype_as_category(df):

    for column in df.keys():
        if is_object_dtype(df[column]):
            df[column] = df[column].astype('category')

    return df

def fill_numeric_na(df, method : str = "mean"):
    """method: mean or median"""

    for column in df.keys():

        if is_numeric_dtype(df[column]):

            if method == "mean":
                df[column].fillna(df[column].mean(), inplace = True)
            elif method == "median":
                df[column].fillna(df[column].median(), inplace = True)

    return df

def rmse(y, yhat):
    """A utility function to calculate the Root Mean Square Error (RMSE).
    
    Args:
        y (array): Actual values for target.
        yhat (array): Predicted values for target.
        
    Returns:
        rmse (double): The RMSE.
    """
    return np.sqrt(mean_squared_error(y, yhat))