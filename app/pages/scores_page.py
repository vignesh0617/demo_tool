from components.navbar import get_navbar
from dash import dcc, html
from callback_functions.main_app_class import main_app
from components.score_card import layout as score_card



layout = html.Div(children=[
    html.Div(className="app_bg"),
    get_navbar(main_app.environment_details['score_card_link']),
    score_card,
    dcc.Download("data_to_download")
],className="main-container flex-container")