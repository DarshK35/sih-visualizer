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
	html.Label("Select a CSV File: "),
	dcc.Dropdown(
		options = get_files(),
		id = "csv-select"
	),
	html.Br(),

	html.Label("Select X Axis column: "),
	dcc.Dropdown(
		id = "csv-x-select"
	),
	html.Br(),
	html.Label("Select Y Axis column: "),
	dcc.Dropdown(
		id = "csv-y-select"
	),

	dcc.Graph(id = "csv-visual"),

	dcc.Store(id = "actual-file", data = {"file": {}})
])


@app.callback(
	[
		Output("csv-x-select", "options"),
		Output("csv-y-select", "options"),
		Output("actual-file", "data")
	],
	Input("csv-select", "value"),
	State("actual-file", "data"),
	prevent_initial_call = True
)
def update_columns(filename, glob):
	if not filename:
		return [], [], {}
	data = pd.read_csv(data_dir + filename)
	print(glob["file"])
	return list(data.columns), list(data.columns), data.to_json()


@app.callback(
	Output("csv-visual", "figure"),
	[
		Input("csv-x-select", "value"),
		Input("csv-y-select", "value")
	],
	State("actual-file", "data"),
	prevent_initial_call = True
)
def auto_graph(x_col, y_col, glob):
	print(glob)
	print(x_col)
	print(y_col)
	if not x_col or not y_col:
		return {}
	
	data = pd.read_json(glob)
	if x_col == y_col:
		figure = px.histogram(
			data,
			x = x_col,
			nbins = 32,
			title = f"{x_col} Frequency Distribution"
		)

		figure.update_layout(
			title = f"{x_col} Frequency Distribution",
			height = 600,
			width = 960
		)
	else:
		figure = {
			"data": [{
				"x": data[x_col],
				"y": data[y_col],
				"mode": "markers",
				"marker": {
					"size": 8
				}
			}],
			"layout": {
				"title": f"{x_col} vs {y_col}",
				"xaxis": {"title": x_col},
				"yaxis": {"title": y_col},
				"height": 600,
				"width": 960
			}
		}

	return figure

app.run_server(debug = True)