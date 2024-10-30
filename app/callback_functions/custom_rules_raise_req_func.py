from dash import Input,Output,State,ctx,no_update
from dash.exceptions import PreventUpdate
from callback_functions.main_app_class import main_app
from connections.MySQL import get_data_as_data_frame,get_data_as_tuple
from callback_functions.custom_helpers import decode_token

# def load_user_email_options():
#     df_name_and_email = get_data_as_data_frame(sql_query="select name , email_id from users")
#     name = df_name_and_email['name'].tolist()
#     email = df_name_and_email['email_id'].tolist()
#     options = {}
#     for i in range(len(name)):
#         options[email[i]] = name[i]
#     return options




@main_app.app.callback(
    Output("requesting_user","value"),
    Output("user_email","value"),
    Input("url1","pathname"),
    State('token','data')
)
def get_username_email_from_token(url,token):
    if url == main_app.environment_details["custom_rules_new"]:
        tok = decode_token(token=token)
        return tok['user_name'],tok['email_id']
    raise PreventUpdate


# @main_app.app.callback(
#         Output('user_email','value'),
#         Input('requesting_user','value')
# )
# def update_email_id(requesting_user_name):
#     return requesting_user_name




def validate_custom_rules_form(requesting_user,user_email,request_type,business_desc_sql):#,status):

    user_flag = requesting_user is not None and len(requesting_user.strip()) >5 
    email_flag = user_email is not None and len(user_email.strip()) != 0 and user_email.find("@") != -1 and user_email.find(".com") != -1 and (user_email.find(".com") - user_email.find("@") != 1)
    type_flag = request_type is not None and len(request_type.strip()) != 0 
    sql_flag = business_desc_sql is not None and len(business_desc_sql.strip()) != 0 
    # status_flag  = status is not None and len(status.strip()) != 0 

    individual_flags = dict(user_flag = user_flag,email_flag=email_flag,type_flag=type_flag,sql_flag=sql_flag)#,status_flag=status_flag)
    final_flag = user_flag and email_flag and type_flag and business_desc_sql #and status_flag

    return individual_flags,final_flag

@main_app.app.callback(
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Output("status","value",allow_duplicate=True),
    Output("request_id","value",allow_duplicate=True),

    # Output("requesting_user","valid",allow_duplicate=True),
    # Output("requesting_user","invalid",allow_duplicate=True),
    # Output("user_email","valid",allow_duplicate=True),
    # Output("user_email","invalid",allow_duplicate=True),
    # Output("request_type","valid",allow_duplicate=True),
    # Output("request_type","invalid",allow_duplicate=True),
    # Output("business_desc_sql","valid",allow_duplicate=True),
    # Output("business_desc_sql","invalid",allow_duplicate=True),
    

    # Output("status","valid",allow_duplicate=True),
    # Output("status","invalid",allow_duplicate=True),
    Input("cudf_submit_btn","n_clicks"),
    State("requesting_user","value"),
    State("user_email","value"),
    State("request_type","value"),
    State("business_desc_sql","value"),
    State("status","value"),
    prevent_initial_call = True
)
def open_close_modal(n_clicks,requesting_user,user_email,request_type,business_desc_sql,status):
    if ctx.triggered_id is None or n_clicks is None:
        raise PreventUpdate
    
    print('Entered into func')
    individual_flags,all_fields_validated = validate_custom_rules_form(requesting_user,user_email,request_type,business_desc_sql)#,status)

    if all_fields_validated:
        
        # sql_query = f'insert into custom_rules_request (`REQUESTING_USER`,`USER_EMAIL`,`REQUEST_TYPE`,`DESCRIPTION/SQL`,`STATUS`) values ("{requesting_user.strip()}","{user_email.strip()}","{request_type.strip()}","{business_desc_sql.strip()}","Submitted")' #"{status.strip()}")'
        user_id = get_data_as_data_frame(sql_query=f'select id from users where email_id = "{user_email}"').iloc[0][0]
        sql_query = f'insert into custom_rules_request (`USER_ID`,`REQUEST_TYPE`,`DESCRIPTION/SQL`,`STATUS`) values ({user_id},"{request_type}","{business_desc_sql.strip()}","Submitted")' #"{status.strip()}")'
        # main_app.cursor.execute(sql_query)
        res = get_data_as_tuple(sql_query=sql_query)

        if res!='Error':
            request_id = get_data_as_data_frame(sql_query=f'select max(request_id) from custom_rules_request').iloc[0][0]
            print('Inserted successfully')
            return "Request Submitted","Success","success",5000,True,"Submitted",request_id   #,individual_flags["user_flag"],not(individual_flags["user_flag"]),individual_flags["email_flag"],not(individual_flags["email_flag"]),individual_flags["type_flag"],not(individual_flags["type_flag"]),individual_flags["sql_flag"],not(individual_flags["sql_flag"]),'Submitted' #individual_flags["status_flag"],not(individual_flags["status_flag"])
        else:
            # print('---------------------------\n',str(e).split(":")[1],str(e).split(":")[0] == '1062 (23000)')
            msg = 'This request is already submitted by another user' #if str(e).split(":")[0] == '1062 (23000)' else str(e)
            return msg,"Warning","warning",5000,True,no_update,no_update    #,individual_flags["user_flag"],not(individual_flags["user_flag"]),individual_flags["email_flag"],not(individual_flags["email_flag"]),individual_flags["type_flag"],not(individual_flags["type_flag"]),individual_flags["sql_flag"],not(individual_flags["sql_flag"]),no_update #individual_flags["status_flag"],not(individual_flags["status_flag"])
    

    return "Fill all details","Warning","warning",5000,True,no_update,no_update    #,individual_flags["user_flag"],not(individual_flags["user_flag"]),individual_flags["email_flag"],not(individual_flags["email_flag"]),individual_flags["type_flag"],not(individual_flags["type_flag"]),individual_flags["sql_flag"],not(individual_flags["sql_flag"]),no_update #individual_flags["status_flag"],not(individual_flags["status_flag"])



