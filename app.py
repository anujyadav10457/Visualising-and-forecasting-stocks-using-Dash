import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# User defined function to calculate Exponential Moving Average (EMA)
def get_ema(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.line(df, x=df.index, y='EWA_20', title="Exponential Moving Average vs Date")
    return fig

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.Div([
        html.P("Welcome to the Stock Forecast by Anuj!", className="start"),
        html.P([
            html.Label('Input stock code:')
        ]),
        dcc.Input(id='stock-code', type='text', placeholder='stock code'),
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.Div([
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date=dt.today().replace(day=1),
                end_date=dt.today(),
                display_format='YYYY-MM-DD'
            )
        ]),
        html.Div([
            html.Button('Fetch Stock Price', id='fetch-stock-price', n_clicks=0),
            html.Button('Indicators', id='indicator', n_clicks=0),
            dcc.Input(id='days-forecast', type='text', placeholder='No. of days to forecast'),
            html.Button('Forecast', id='forecast-button', n_clicks=0)
        ])
    ], className='nav'),
    html.Div([
        html.Div(id="header"),  # Logo & Company Name
        html.Div(id="description", className="description_ticker"),  # Description
        html.Div(id="graphs-content"),  # Stock price plot
        html.Div(id="indicator-graph"),  # Indicator plot
        html.Div(id="forecast-content")  # Forecast plot
    ], className="content"),
    html.Div(id='output-div')  # Added this line for the callback output
], className='container')

@app.callback(
    Output('output-div', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-code', 'value')]
)
def update_output(n_clicks, stock_code):
    if n_clicks > 0 and stock_code:
        ticker = yf.Ticker(stock_code)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf, orient="index").T
        business_summary = df['longBusinessSummary'][0]
        logo_url = df['logo_url'][0]
        short_name = df['shortName'][0]
        
        return [
            html.H3(short_name),
            html.P(business_summary),
            html.Img(src=logo_url, style={'width': '100px', 'height': '100px'})
        ]
    else:
        return "Please enter a valid stock code and click submit"
    
    
@app.callback(
    Output("graphs-content", "children"),
    [Input('fetch-stock-price', 'n_clicks')],
    [State('stock-code', 'value'),
    State('date-range-picker', 'start_date'),
    State('date-range-picker', 'end_date')]
)
def update_stock_graph(n_clicks, stock_code, start_date, end_date):
    if n_clicks > 0:
        try:
            df = yf.download(stock_code, start=start_date, end=end_date)
            fig = px.line(df, x=df.index, y='Close', title=f'Stock Price History for {stock_code}')
            stock_graph = dcc.Graph(figure=fig)
            return stock_graph
        except Exception as e:
            return html.P(f"Error fetching stock price data: {str(e)}")
    return None

@app.callback(
    Output("indicator-graph", "children"),
    [Input('indicator', 'n_clicks')],
    [State('stock-code', 'value'),
    State('date-range-picker', 'start_date'),
    State('date-range-picker', 'end_date')]
)
def update_indicator_graph(n_clicks, stock_code, start_date, end_date):
    if n_clicks > 0:
        try:
            df = yf.download(stock_code, start=start_date, end=end_date)
            fig = get_ema(df)
            indicator_graph = dcc.Graph(figure=fig)
            return indicator_graph
        except Exception as e:
            return html.P(f"Error calculating indicators: {str(e)}")
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
