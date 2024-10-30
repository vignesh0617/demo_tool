from datetime import datetime
import plotly.express as px
from plotly.express import pie
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import decode_token
from dash import no_update
from dash.dependencies import Output, Input, State
from pages.home_page import layout as home_page
from pages.login_page import layout as login_page
from pages.page_not_found import layout as page_not_found
from pages.rule_binding_page import layout as rule_binding_page
from pages.scores_page import layout as scores_page
from pages.custom_rules_raise_req import layout as custom_rules
from pages.custom_rules_my_req import layout as my_request
import time

# app = main_app.app

c = 0

# This function updates the following
# 1 -> url2 component's pathname
# 2 -> app_output component's children
# 3 -> token component's clear_data
# It takes 2 inpiuts (1 input and 1 state)
# Input -> url1 components pathname
# State -> token components data
@main_app.app.callback(
    Output("url2","pathname"),
    Output("app_output","children"),
    Output("token","clear_data"),
    Input("url1","pathname"),
    State("token","data"),
    )
def validate_token_and_update_screen(pathname,token):

    if pathname is None:
        print('Request received')
        return 'Loading'
    global c
    c+=1
    print(f'''----------------------
            Loop number = {c}
            pathname =========== {pathname}
            ---------------------------''')
    try:
        payload = decode_token(token)
        session_not_over = payload['session_end_time'] > int(time.time())
        if session_not_over:
            main_app.current_url = pathname
            if(pathname == main_app.environment_details['home_page_link'] or pathname == main_app.environment_details['login_page_link']):
                print("1.1--------------------")
                print(f"=========> {main_app.current_url}")
                return main_app.environment_details['home_page_link'],home_page,False
            elif(pathname == main_app.environment_details['rule_execution_link'] or pathname == main_app.environment_details['login_page_link'] ):
                print("1.2--------------------")
                print(f"=========> {main_app.current_url}")
                main_app.binding_id_list=[]
                return main_app.environment_details['rule_execution_link'],rule_binding_page,False
            elif(pathname == main_app.environment_details['score_card_link'] or pathname == main_app.environment_details['login_page_link'] ):
                print("1.2--------------------")
                print(f"=========> {main_app.current_url}")
                return main_app.environment_details['score_card_link'],scores_page,False
            elif(pathname == main_app.environment_details['custom_rules_new'] or pathname == main_app.environment_details['login_page_link'] ):
                print("1.2--------------------")
                print(f"=========> {main_app.current_url}")
                return main_app.environment_details['custom_rules_new'],custom_rules,False
            elif(pathname == main_app.environment_details['custom_rules_my_req'] or pathname == main_app.environment_details['login_page_link'] ):
                print("1.2--------------------")
                print(f"=========> {main_app.current_url}")
                return main_app.environment_details['custom_rules_my_req'],my_request,False
            elif(pathname == main_app.environment_details['logout_page_link']):
                print("1.4--------------------")
                main_app.connector = ""
                return main_app.environment_details['logout_page_link'],login_page,True
            else:
                print("1.5--------------------")
                return pathname,page_not_found,False
        else:
            print("2-------------------- Session over login again")
            return main_app.environment_details['login_page_link'],login_page,False
    except Exception as e:
        print("3 ---------------------Not a valid Token")
        # return login_page, False
        return main_app.environment_details['login_page_link'],login_page, False
