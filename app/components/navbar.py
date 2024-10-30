import dash_bootstrap_components as dbc
from callback_functions.custom_helpers import main_app
from dash import html,dcc,ctx,MATCH,ALL
from dash.dependencies import Output , Input, State
from callback_functions.custom_helpers import decode_token
import time



def get_navbar(active_link:str = '',type="logged_in"):

    logout_submenu = html.Ul([
                html.Li(   
                    children = [
                        dcc.Link(
                             id="login_logout",
                             href="#",
                             className="my_req_badge2",   
                        ),
                
                        html.Ul([
                            html.Li(
                                dcc.Link("Logout",
                                         id={"type" : "nav_link","index":8},
                                         href=main_app.environment_details['logout_page_link'],
                                         )
                            ),
                        ],className="submenu")
                    ] 
                ),

            ])
    
    navbar = html.Div([
        html.Nav([
            html.Ul([

                # main_app.environment_details['custom_user_defined_rules']),
                html.Li(
                    dcc.Link(children=[
                        html.Img(id="cognizant_logo",src=main_app.app.get_asset_url("cognizantlogo.svg"),),
                        "IDM"
                    ],id='logo',href=main_app.environment_details['home_page_link'])
                ),

                html.Li(
                    dcc.Link("Rule Binding",
                             id={"type" : "nav_link","index":0},
                             href=main_app.environment_details['home_page_link'],
                             className='active-link' if main_app.environment_details['home_page_link'] == active_link else '')
                ),

                html.Li(        
                    dcc.Link("Rule Execution",
                             id={"type" : "nav_link","index":1},
                             href=main_app.environment_details['rule_execution_link'],
                             className='active-link' if main_app.environment_details['rule_execution_link'] == active_link else '')
                ),
                    
                html.Li(    
                    dcc.Link("Dashboard",
                             id={"type" : "nav_link","index":2},
                             href=main_app.environment_details['score_card_link'],
                             className='active-link' if main_app.environment_details['score_card_link'] == active_link else '')
                ),
                    
                html.Li(   
                    children = [

                        dcc.Link("Custom Rules",
                             id={"type" : "nav_link","index":3},
                             href=main_app.environment_details['custom_rules_new'],
                             className='active-link' if main_app.environment_details['custom_rules_new'] == active_link or main_app.environment_details['custom_rules_my_req'] == active_link else ''
                        ),
                
                        html.Ul([
                            html.Li(
                                dcc.Link("Raise Request",
                                         id={"type" : "nav_link","index":4},
                                         href=main_app.environment_details['custom_rules_new'],
                                         )
                            ),

                            html.Li(
                                dcc.Link("My Requests",
                                         id={"type" : "nav_link","index":5},
                                         href=main_app.environment_details['custom_rules_my_req'],
                                         )
                            ),

                            # html.Li(
                            #     dcc.Link("Create New Rule",
                            #              id={"type" : "nav_link","index":6},
                            #              href=main_app.environment_details['custom_rules_new_rule'],
                            #              )
                            # ),
                        ],className="submenu")
                    ] 
                ),

            ]),
            # logout_submenu if type=="logged_in" else  html.Ul([
            #     html.Li(
            #         dcc.Link( "Login",
            #                  id='login_logout',
            #                  href=main_app.environment_details['login_page_link'])
            #     ),
            # ]),

            html.Ul([
                html.Li(
                    dcc.Link( "Logout" if type=="logged_in" else "Login",
                             id='login_logout',
                             href=main_app.environment_details['logout_page_link'] if type=="logged_in" else main_app.environment_details['login_page_link'] )
                ),
            ]),
        ],className="navbar")
    ],className="navbar-container")

    return navbar