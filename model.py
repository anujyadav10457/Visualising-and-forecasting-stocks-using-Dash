import yfinance as yf
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime as dt


def get_data(stock_code):
    # Fetch stock prices for the last 60 days
    df = yf.download(stock_code, period="60d")
    return df['Close'].values.reshape(-1, 1)

def train_model(data):
    X = np.arange(len(data)).reshape(-1, 1)
    y = data

    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Define parameter grid for GridSearchCV
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': [1, 0.1, 0.01, 0.001],
        'epsilon': [0.1, 0.01, 0.001, 0.0001]
    }

    # Instantiate SVR model with RBF kernel
    svr = SVR(kernel='rbf')

    # Perform GridSearchCV for hyperparameter tuning
    grid_search = GridSearchCV(svr, param_grid, cv=5, scoring='neg_mean_squared_error', verbose=2)
    grid_search.fit(X_train, y_train)

    # Train SVR model with the best parameters
    best_svr = grid_search.best_estimator_
    best_svr.fit(X_train, y_train)

    # Test model's performance
    y_pred = best_svr.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    return best_svr, mse, mae

if __name__ == "__main__":
    # Example usage
    stock_code = "AAPL"
    data = get_data(stock_code)
    model, mse, mae = train_model(data)
    print(f"Model trained with MSE: {mse}, MAE: {mae}")
