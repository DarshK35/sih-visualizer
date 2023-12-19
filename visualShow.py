import dash
import os
import numpy as np
import pandas as pd

from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from plotly import express as px
from plotly import subplots as sp
from plotly import graph_objects as go

data_dir = "Data/"

def get_files():
	ret = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
	return ret

app = dash.Dash("Visualisation")
app.title = "CSV Visualisation"
app.layout = html.Div([
	dcc.Dropdown(
		options = get_files(),
		id = "csv-select"
	),

	dcc.Graph(id = "csv-visual")
])

# Using a pair plot to show the correlations
@app.callback(
	Output("csv-visual", "figure"),
	Input("csv-select", "value")
)
def auto_graph(filename):
	data = pd.read_csv(data_dir + filename)
	columns = data.columns

	figure = sp.make_subplots(
		rows = len(columns),
		cols = len(columns),
		shared_xaxes = False,
		shared_yaxes = False
	)

	for i, col1 in enumerate(columns):
		for j, col2 in enumerate(columns):
			if col1 == col2:
				trace = go.Histogram(
					x = data[col1],
					name = col1,
					showlegend = False,
				)
			else:
				trace = go.Scatter(
					x=data[col1],
					y=data[col2],
					mode='markers',
					name = col1.split('_')[0] + ' vs ' + col2.split('_')[0],
					marker = {"size": 4}
				)
			figure.add_trace(trace, row=i + 1, col=j + 1)

	for i, col in enumerate(columns):
		figure.update_xaxes(title_text=col, row=len(columns), col=i + 1)
		figure.update_yaxes(title_text=col, row=i + 1, col=1)
	
	figure.update_layout(
		showlegend = False,
		height = 1000,
		width = 1600
	)

	return figure

app.run_server(debug = True)