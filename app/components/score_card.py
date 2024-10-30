from dash import html,dcc
from callback_functions.score_card_functions import *
import dash_bootstrap_components as dbc

layout = html.Div([
    
    html.Div([
            html.Div(id = "filters_rule_binding",className="side-filter-tab-contents"),
            html.Button("Clear", id = "clear_filter_button", className="btn-theme1 btn btn-primary"),
            # html.Button("Apply", id = "apply_filter_button", className="btn-theme1")
        ],className="filter-header",id = "filter_header"),


    html.Div([

            dcc.Loading([
                dcc.Graph(id="pie_chart1"),
                ]),

            dcc.Loading([
                dcc.Graph(id="pie_chart2"),
                ]),

                html.Div(id="score_card_rules_table",className="top-table")
        
    ],id="score_card_contents_top",className="score-card-page-contents-top"),
    

    
    dcc.Loading([
    html.Div([
        html.Div([
            dbc.Tabs(
            [
                dbc.Tab(label="1 Month",children=[dcc.Graph(id="trend_chart_1_month")]),
                dbc.Tab(label="3 Months",children=[dcc.Graph(id="trend_chart_3_month")]),
                dbc.Tab(label="6 Months",children=[dcc.Graph(id="trend_chart_6_month")]),
            ]
        )
        ],id="score_card_trend_charts_tabs"),
        
    
        html.Div(id="score_card_binded_rules_container",children = [
            html.Div(id="download_container",children = [
                html.Button("Download",id="download_failed_data",className = "btn-theme1 btn-primary")
            ]),

            html.Div(id="score_card_binded_rules",className="bottom-table")
        ],className = "bottom-table-container"),

        dcc.Download(id="failed_dataset"),
        
    ],id="score_card_contents_bottom",className="score-card-page-contents-bottom"),
    ]),
                
        

    html.Span(id="refresh_button_score_card_page", className="bi bi-arrow-clockwise refresh_button_position btn-white circle btn-animated"),
    
],id = "score_card_failed_records_container")
