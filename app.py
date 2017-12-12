import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('dataeurostat.csv')

available_na_item = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()
df1 = df[df['UNIT'] == 'Current prices, million euro']

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.Div([
		html.Div([
            dcc.Dropdown( 
            	id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_na_item],
                value='Imports of goods and services'
            ),
            dcc.RadioItems(
                id='xaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], 
        style={'width': '30%', 'display': 'inline-block'}),
    
    	html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_na_item],
                value='Exports of goods and services'
            ),
            dcc.RadioItems(
                id='yaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='Eurostat-graph1'),

    html.Div(dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(TIME): str(TIME) for TIME in df['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),

    html.Hr(),

# Second graph

    html.Div([
        html.Div([
        dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_na_item],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Germany'
            
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='Eurostat-graph2'),


])

@app.callback(
    dash.dependencies.Output('Eurostat-graph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):

    dff = df[df['TIME'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    
@app.callback(
    dash.dependencies.Output('Eurostat-graph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name):

    dff = df1[df1['GEO'] == yaxis_column_name]
    return {
        'data': [go.Scatter(
            x=dff['TIME'].unique(),
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()