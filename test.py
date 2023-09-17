import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
import yfinance as yf


github_csv_url = 'https://github.com/gayatrisood2000/stock-ticker/blob/main/NASDAQcompanylist.csv'
nsdq = pd.read_csv(github_csv_url, encoding='utf-8')
nsdq.set_index('Symbol', inplace=True)

app = dash.Dash()
server = app.server

dropdown_options = []
for tic in nsdq.index:
    mydict = dict()
    mydict['label'] = nsdq.loc[tic]['Name'] + ' ' + tic
    mydict['value'] = tic
    dropdown_options.append(mydict)

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select stock symbol(s)', style=dict(paddingRight='30px'))
    ]),
    html.Div([
        dcc.Dropdown(
            id='ticker-symbols',
            options=dropdown_options,
            value=['TSLA'],
            multi=True
        )
    ], style=dict(display='inline-block', width='100%', verticalAlign='top')),
    html.Div([
        html.H3('Select a start and end date'),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=datetime(2013, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ]),
    html.P(),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit'
        )
    ]),
    html.Div([
        dcc.Graph(
            id='linechart',
            figure=dict(
                data=[go.Scatter(
                    x=[1, 2],
                    y=[3, 1],
                    mode='lines'
                )],
                layout=go.Layout(
                    title='Default Value'
                )
            )
        )
    ])
])


@app.callback(
    Output(component_id='linechart', component_property='figure'),
    Input(component_id='submit-button', component_property='n_clicks'),
    [State(component_id='ticker-symbols', component_property='value'),
     State(component_id='date-picker', component_property='start_date'),
     State(component_id='date-picker', component_property='end_date')]
)
def update_chart(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[0:10], '%Y-%m-%d')

    traces = []
    title = ', '.join(stock_ticker)
    for tic in stock_ticker:
        df = yf.download(tic, start, end)
        traces.append(go.Scatter(
            x=df.index, y=df['Adj Close'], mode='lines', name=tic
        ))
    figure = dict(
        data=traces,
        layout=go.Layout(
            title=title
        )
    )
    return figure


if __name__ == '__main__':
    app.run_server()
