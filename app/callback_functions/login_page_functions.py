from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from callback_functions.custom_helpers import *
from connections.MySQL import *
import time
from dash import no_update


#this function is used to show and hide password
@main_app.app.callback(
    Output("password","type"),
    Output("show_hide_password","className"),
    Input("show_hide_password","n_clicks"),
    prevent_initial_call =True
)
def show_hide_password(n_clicks):
    # if n_clicks  is None :
    #     raise PreventUpdate
    if n_clicks%2 == 1:
        return "text","bi bi-eye-slash"
    return "password","bi bi-eye"

#handles login requests
@main_app.app.callback(
    Output("token","data",allow_duplicate=True),
    Output("url1","pathname",allow_duplicate=True),
    Output("message","children",allow_duplicate=True),
    Output("message","className",allow_duplicate=True),
    Input("submit_button","n_clicks"), 
    State("username","value"), 
    State("password","value"),
    prevent_initial_call =True
    )
def login_handler(n_clicks,username, password):
    
    if username != "" and password != "" and username is not None and password is not None: 
        user_exisits , payload = get_payload(username=username,password=password)
        if user_exisits:
            token = create_token(payload= payload)
            return token , main_app.environment_details['home_page_link'], "Login Successfull","success"
        else :
            return "" , no_update ,"Wrong username or password","error"
    else : 
        raise PreventUpdate


#checks if username and password is not empty in the login page
@main_app.app.callback (
    Output("username","invalid"), 
    Output("password","invalid"),
    Input("username","value"),
    Input("password","value"),
    Input("submit_button","n_clicks"),
    )
def validate_form(username, password, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    username_invalid = (username =="" or username is None)
    password_invalid = (password =="" or password is None)
    return username_invalid,password_invalid


# function will return a flag that idicates wether the giver user exists in database or not
# if present, then return a payload along with it
def get_payload(username :str , password : str):
    users_table = main_app.environment_details['users_table']
    sql_query = f"select id,name, email_id,role from {users_table} where user_name = '{username}' and password='{password}'"

    res = get_data_as_tuple(sql_query=sql_query)

    if len(res) != 0:
        # print(res)
        user_id, name , email_id , role = res[0]
        payload = {
                    "user_id":user_id,
                    "user_name" : name,
                    "email_id" : email_id,
                    "role" : role,
                    "session_end_time" : int(time.time()) + int(main_app.environment_details["session_time_in_secs"])
                }
        return True,payload
    
    return False,None