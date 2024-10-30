from dash import Input,Output,State,no_update
from dash.exceptions import PreventUpdate
from connections.MySQL import get_data_as_data_frame, get_data_as_tuple
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import decode_token
from dash import html
from datetime import datetime


# gets list of request_ids for a given user id
def get_request_id_for_user(user_id : int , role:str) -> list[int] :


    if role.lower() == 'support':
        sql_query = 'select request_id from custom_rules_request where status != "Closed" order by request_id '
    else:
        sql_query = f'select request_id from custom_rules_request where user_id = {user_id} order by request_id '

    df = get_data_as_data_frame(sql_query=sql_query)
    
    request_ids = df[df.columns[0]].tolist()
    return request_ids

# loads comments from comment table for a given request id and automatically creates a layout of comments
def load_comments(request_id : int ) -> list[html.Div]:
    sql_query = f'select comment_by, comment, time_stamp from comments where request_id = {request_id} order by time_stamp asc'
    result = get_data_as_tuple(sql_query=sql_query)
    final_comments = []

    if len(result) == 0:
        layout = html.Div(children=[
            "No comments yet"
        ], className="my_req_comments")
        final_comments.append(layout)
        return final_comments
    
    for record in result:
        comment_by = record[0][0:2].upper()
        comment = record[1]
        time_stamp = record[2].strftime("%d %b %Y, %H:%M:%S")

        layout = html.Div(children=[
                    html.Div(children=comment_by,className='my_req_badge'),
                    html.Div(children=time_stamp,className='my_req_time_stamp'),
                    comment
                ],className='my_req_comments')
        final_comments.append(layout)

    return final_comments

    
    

@main_app.app.callback(
    Output('my_req_status','value'),
    Output('my_req_requested_user','value'),
    Output('my_req_description','value'),
    Output('my_req_comments_area','children'),
    Input('my_req_user_ids','value'),
    prevent_initial_call = True,
)
def update_my_request_screen(request_id : int):
    
    sql_query = f'select a.status , b.name , a.`description/sql` from custom_rules_request a inner join users b on a.user_id = b.id where a.request_id = {request_id} '
    df = get_data_as_data_frame(sql_query=sql_query)

    request_status = df.iloc[0,0]
    requested_user = df.iloc[0,1]
    request_description = df.iloc[0,2]
    comments = load_comments(request_id=request_id)

    return request_status,requested_user,request_description,comments


# if the logged in user has a role of "suppport" then all request id's will be displayed
# else only the request id's for the logged in user alone will be shown
@main_app.app.callback(
    Output("my_req_user_ids","options"),
    Input("url1","pathname"),
    State("token","data")
)
def refresh_request_id(url,token):
    if url == main_app.environment_details["custom_rules_my_req"]:
        tok = decode_token(token=token)
        user_id , role= tok['user_id'],tok['role']
        return get_request_id_for_user(user_id=user_id,role=role)
    

@main_app.app.callback(
    Output("my_req_comments_area","children",allow_duplicate=True),
    Output("my_req_post_comments","value"),
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Input("my_req_submit_comment","n_clicks"),
    State("my_req_comments_area","children"),
    State("my_req_post_comments","value"),
    State("token","data"),
    State("my_req_user_ids","value"),
    prevent_initial_call = True
)
def update_comments_section(n_clicks , existing_comments,new_comment,token,request_id):

    if n_clicks is None :
        raise PreventUpdate
    
    comment_by = decode_token(token=token)["user_name"]
    comment_is_not_empy = new_comment is not None and len(new_comment.strip())!=0

    if comment_is_not_empy :
        sql_query  = f'insert into comments (`request_id` , `comment_by` , `comment` , `time_stamp`) values ({request_id},"{comment_by}","{new_comment}" ,"{datetime.now()}" )'            
        comment_added = get_data_as_tuple(sql_query)
        if comment_added != 'Error':
            layout = html.Div(children=[
                            html.Div(children=comment_by[0:2].upper(),className='my_req_badge'),
                            html.Div(children=datetime.now().strftime("%d %b %Y, %H:%M:%S"),className='my_req_time_stamp'),
                            new_comment
                        ],className='my_req_comments')
        
            # if there is no comment for the existing request id then try block will execute
            # we get an error while trying to get 'No comments yet' section if its not there
            # at that time we append the new comment to the existing comment and return it

            try:
                if existing_comments[0]['props']['children'][0] == 'No comments yet' :
                    return  [layout], "" , no_update, no_update, no_update, no_update, no_update
            except:
                pass
            existing_comments.append(layout)
            return  existing_comments, "" , no_update, no_update, no_update, no_update, no_update
        else:
            return no_update , no_update , "Something went wrong! Please try again" ,"Error!","danger",2500,True
    
    return no_update , no_update , "Comment can not be empty" ,"Error!","danger",2500,True




@main_app.app.callback(
    Output("my_req_status","value",allow_duplicate=True),
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Input("my_req_close_button","n_clicks"),
    State("my_req_user_ids","value"),
    State("my_req_status","value"),
    prevent_initial_call = True
)
def close_ticket(n_clicks ,request_id,exisitng_status):
    if n_clicks is None :
        raise PreventUpdate

    if exisitng_status == 'Closed':
        return no_update, "Request already Closed" ,"Warning!","warning",2500,True

    sql_query  = f'update custom_rules_request set `status` ="Closed" where `request_id` = {request_id};'            
    status_updated = get_data_as_tuple(sql_query)
    if status_updated != 'Error':
        return  "Closed", "Request Closed" ,"Info!","info",2500,True
    else:
        return no_update , "Something went wrong! Please try again" ,"Error!","danger",2500,True

