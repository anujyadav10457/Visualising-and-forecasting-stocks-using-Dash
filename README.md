# Visualising and forecasting stocks
## Project Overview  
The Stock Dash App is a single-page web application developed using Dash (a Python framework) and machine learning models. This app allows users to input a stock code and view relevant company information, stock price plots, and predicted stock prices for specific dates. This project leverages the yfinance library to fetch financial data and employs a Support Vector Regression (SVR) model to predict stock prices.

## Features
Company Information: Displays the company logo, registered name, and description based on the provided stock code.  
Stock Price Visualization: Generates dynamic plots of stock prices using historical data.  
Stock Price Prediction: Utilizes a machine learning model to predict future stock prices based on user input.  
## Files and Directories
app.py: This is the main file that sets up the Dash web application, defines the layout, and handles user inputs and outputs via callback functions.  
model.py: This file contains the implementation of the SVR machine learning model for predicting stock prices.  
assets/style.css: Contains CSS styles for enhancing the appearance of the web application.  
requirements.txt: Lists all the Python libraries required to run the application.  
Procfile: Necessary for deploying the app on Heroku.  
