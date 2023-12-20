import dash
import os
import io
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
	html.Div([
		html.Span("Select a CSV File: "),
		dcc.Dropdown(
			options = get_files(),
			id = "csv-select"
		)
	], id = "csv-select-grid"),

	html.Div([
		html.Div([
			html.Span("X Axis column: "),
			dcc.Dropdown(
				id = "csv-x-select"
			)
		], id = "x-grid"),
		html.Div([
			html.Span("Y Axis column: "),
			dcc.Dropdown(
				id = "csv-y-select"
			)
		], id = "y-grid")
	], id = "axis-select"),

	dcc.Graph(id = "csv-visual"),

	html.Div([
		html.Span("Column to Check: "),
		dcc.Dropdown(
			id = "cont-col-select"
		)
	], id = "pred-analyse"),

	dcc.Graph(id = "future-preds"),

	dcc.Store(id = "actual-file", data = {"file": {}})
], id = "main-body")


@app.callback(
	[
		Output("csv-x-select", "options"),
		Output("csv-y-select", "options"),
		Output("cont-col-select", "options"),
		Output("actual-file", "data")
	],
	Input("csv-select", "value"),
	State("actual-file", "data"),
	prevent_initial_call = True
)
def update_columns(filename, glob):
	if not filename:
		return [], [], [], {}
	data = pd.read_csv(data_dir + filename)

	cont_cols = []
	for col in data.columns:
		dtype = data[col].dtype
		if pd.api.types.is_numeric_dtype(dtype):
			cont_cols.append(col)

	return list(data.columns), list(data.columns), cont_cols, data.to_json()


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
	if not x_col or not y_col:
		return {}
	
	data = pd.read_json(io.StringIO(glob))
	if x_col == y_col:
		figure = px.histogram(
			data,
			x = x_col,
			nbins = 32,
			title = f"{x_col} Frequency Distribution"
		)

		figure.update_layout(
			title = f"{x_col} Frequency Distribution"
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
				"yaxis": {"title": y_col}
			}
		}

	return figure

app.run_server()