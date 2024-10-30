from dash import html
from components.navbar import get_navbar
from callback_functions.main_app_class import main_app
import dash_bootstrap_components as dbc
from callback_functions.custom_rules_my_req_func import *

# ids = get_request_id_for_user()

layout = html.Div( children=[
    html.Div(className="app_bg"),
    html.Div(children=[
        get_navbar(active_link=main_app.environment_details["custom_rules_my_req"]),
    ],className='my_req_navbar'),
    

    html.Div(children=[

        html.Div(children=[
            dbc.Select(placeholder="Request ID",id="my_req_user_ids" ),

            dbc.Input(id="my_req_status" , placeholder="Status", disabled=True ),

            dbc.Input(id="my_req_requested_user" ,placeholder="Requested User", disabled=True),

            dbc.Textarea(id="my_req_description",placeholder="Business Desc/SQL",disabled=True ),

            dbc.Button("Close Request",id='my_req_close_button' , className='btn-theme1'),
        ],className="my_req_side_contents_1"),
        
        html.Div(children=[

            html.Div( id = "my_req_comments_area" , className='my_req_comments_area'),

            html.Div(children=[

                dbc.Textarea(id = "my_req_post_comments" ,className="my_req_post_comments"),
                dbc.Button("Submit",id="my_req_submit_comment" , className='btn-theme1'),

            ],className="my_req_submit_area")

        ],className="my_req_side_contents_2")

    ], className="my_req_body")
],className="my_req_main_container")
