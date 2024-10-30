from dash import html, callback, dcc
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc 
# from callback_functions.home_page_functions import create_filter_buttons_figures_and_tables_and_refresh_data
from callback_functions.side_filter_tab_function import *


layout = html.Div([
        html.Div([
            html.Div(id = "filters_rule_binding",className="side-filter-tab-contents"),
            html.Button("Clear", id = "clear_filter_button", className="btn-theme1"),
            # html.Button("Apply", id = "apply_filter_button", className="btn-theme1")
        ],className="filter-header",id = "filter_header"),
        
        # html.Hr(),
        # html.Div(id="trend_chart_options_container",
        #          children=[
        #              html.Span("Trend Chart Options",id='trend_label'),
        #              dbc.RadioItems(id="trend_chart_option",
        #                 options = [{"label":"1 month" ,"value" : "1"},
        #                             {"label":"3 months" ,"value" : "3"},
        #                             {"label":"6 months" ,"value" : "6"}],
        #                 inline = True,
        #                 value="6"),
        #          ])
        
], id="side-filter-tab-container",className="side-filter-tab-container")
