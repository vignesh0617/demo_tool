from dash import html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from callback_functions.load_function import *
from callback_functions.custom_helpers import *
from pages.home_page import layout as home_page
from callback_functions.routing import *
from components.loading_screen import layout as loading_screen
# import plotly.express as px


main_app.app.layout = html.Div(children = [
    dcc.Location(id="url1",refresh=False),
    dcc.Location(id="url2",refresh=False),
    #the token is stored in local web browser for authenticating the user
    dcc.Store(id="token", storage_type = "session", data="") , 
    html.Div(id="app_output",children=home_page),
    loading_screen,
    dbc.Toast(
        children = [],
        id="info_toast",
        is_open=False,
        dismissable=True,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    ),  
    ])

if(__name__ == "__main__"):
    main_app.app.run_server(port = 8056 , debug = False, dev_tools_hot_reload = True)