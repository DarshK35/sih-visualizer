import dash
import os

from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

data_dir = "Data/"

def get_files():
	ret = {}
	return ret

app = dash.Dash("Visualisation")
app.title = "CSV Visualisation"
app.layout = html.Div([
	dcc.Dropdown(
		options = get_files()
	)
])