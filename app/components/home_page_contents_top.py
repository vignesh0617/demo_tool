from dash import html,dcc 
import dash_bootstrap_components as dbc
from callback_functions.custom_helpers import *
from connections.MySQL import get_connection
from callback_functions.home_page_functions import * 
from callback_functions.rule_binding_functions import *

filters,table = load_filter_and_table_for_rule_binding_page()

layout = html.Div(id='hpct',
                  children = [
                      html.Div(id = 'hpct_filter_section',
                               children = [
                                    html.Div(id="filters_rules_repo",children=filters),
                                    dbc.Button("Clear All",id="clear_filter_button_rules_repo",className="btn-theme1"),
                                    #dbc.Button("Apply",id="apply_filter_button_rules_repo"),  
                               ]),
                      
                      html.Div(id = "rules_repo_table_container",children=table),
                  ])
