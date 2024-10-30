from dash import html, Input, Output , State,ALL,ctx, MATCH,no_update
from dash.exceptions import PreventUpdate
from callback_functions.main_app_class import main_app
from connections.MySQL import get_data_as_data_frame
from connections.MySQL import execute_stored_procedure
import time
from callback_functions.custom_helpers import decode_token

# Old function for updating options and values of selected rules
# @main_app.app.callback(
#     Output({"type":"field_mapper","index":ALL},"options"),
#     Output({"type":"field_mapper","index":ALL},"value"),
#     Input("table_selector","value"),
# )
# def update_column_values_in_rule_binding(table_name):

#     if table_name is None:
#         return [[] for i in range(main_app.rule_details["NO_OF_FIELDS"])],["" for i in range(main_app.rule_details["NO_OF_FIELDS"])]

#     sql_query = f"show columns from {table_name}"
#     data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

#     options = [{"label" : column_name, "value" : column_name} for column_name in data_frame[data_frame.columns[0]]]
#     return [ options for i in range(main_app.rule_details["NO_OF_FIELDS"])],[ options[0]["value"] for i in range(main_app.rule_details["NO_OF_FIELDS"])]


@main_app.app.callback(
    Output({"type":"field_mapper","index":ALL},"options",allow_duplicate=True),
    Output({"type":"field_mapper","index":ALL},"value",allow_duplicate=True),
    Input({"type":"source_table_mapper","index":ALL},"value"),
    prevent_initial_call = True
)
def update_column_values_in_rule_binding_2(table_name):


    table_param_names = main_app.rule_details["TABLE_PARAM_NAME"].split("||")
    field_order = main_app.rule_details["PARAM_VALUE_MAPPER"]

    if field_order is not None and field_order !="" and len(table_name) > 1:

        options = []
        values = []

        for i in range(len(table_param_names)):
            field_order = field_order.replace(table_param_names[i],table_name[i] if table_name[i] is not None else "")

        field_order=field_order.split("||")
        for i in range(len(field_order)):
            sql_query = f"show columns from {field_order[i]}"
            option = []
            value = ""
            if field_order[i] != "" and field_order[i] is not None:
                data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)
                option = [{"label" : column_name, "value" : column_name} for column_name in data_frame[data_frame.columns[0]]]
                value = option[0]["value"]
            options.append(option)
            values.append(value)

        return options,values
    
    else:

        if table_name[0] is None:
            return [[] for i in range(main_app.rule_details["NO_OF_FIELDS"])],["" for i in range(main_app.rule_details["NO_OF_FIELDS"])]

        sql_query = f"show columns from {table_name[0]}"
        data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

        options = [{"label" : column_name, "value" : column_name} for column_name in data_frame[data_frame.columns[0]]]
        return [ options for i in range(main_app.rule_details["NO_OF_FIELDS"])],[ options[0]["value"] for i in range(main_app.rule_details["NO_OF_FIELDS"])]



@main_app.app.callback(
    Output("info_toast","children"),
    Output("info_toast","header"),
    Output("info_toast","icon"),
    Output("info_toast","duration"),
    Output("info_toast","is_open"),
    Input("bind_rule","n_clicks"),
    State({"type":"source_table_mapper","index":ALL},"value"),
    State({"type":"field_mapper","index":ALL},"value"),
    prevent_initial_call = True,
)
def bind_rules(n_clicks,table_names,fields):
    if n_clicks is None :
        raise PreventUpdate
    
    try:
        if  None in table_names or None in fields:
            msg = 'Please select Table and Field name before binding'
            header = 'Warning'
            icon = "warning"
        else :
            
            # args = (
            #         main_app.rule_details["RULE_ID"],
            #         table_names,
            #         fields[0],
            #         main_app.rule_details["RULE_TYPE"],
            #         main_app.rule_details["RULE_NAME"],
            #         0 # if this is set to 1 then Stored procedure will bind and run the rule. Else it will bind alone
            #     )
            
            # proc_name = 'bind_one_field_rule'

            args = (
                    main_app.rule_details["RULE_ID"],
                    "||".join(table_names),
                    "||".join(fields),
                    # main_app.rule_details["RULE_TYPE"],
                    # main_app.rule_details["RULE_NAME"],
                    0 # if this is set to 1 then Stored procedure will bind and run the rule. Else it will bind alone
                )
            proc_name = 'bind_rule'
            # main_app.cursor.callproc(proc_name,args=args)
            
            stored_results = execute_stored_procedure(procedure_name=proc_name,args=args)
            final_result  = None
            latest_result = None
            for stored_result in stored_results:#main_app.cursor.stored_results():
                latest_result= stored_result.fetchall()
            
            for result in latest_result:
                final_result = result

            if final_result[0] == 200:
                header = "Success!!"
                icon = "success"
            elif final_result[0] == 409:
                header = "Warning"
                icon = "warning"
            elif final_result[0] == 500:
                header = "Internal Error"
                icon = "warning"
            child2 = [msgs for msgs in final_result[1].split("<br/>")]
            child = [child2.pop(0)]
            while(child2):
                child.extend([html.Br(),child2.pop(0)])
            msg = html.Div(children=child)
    except Exception as e:
        print(f"--------------{e} -------------")
        msg = "Error in SQL Execution.Please contact Support"
        header = 'danger'
        icon = "Error!!"
    duration = 8000

    return msg,header,icon,duration,True

##############
# @main_app.app.callback(
#     Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
#     Input({"type":f"{main_app.environment_details['rule_binding_table_id']}_row_number","index":ALL},"value"),
#     State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"),
#     State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value")
# )
# def test(rows,name,values):
    
#     if ctx.triggered_id is None:
#         raise PreventUpdate
#     index = ctx.triggered_id['index']
#     binding_id = name[index]
#     flag = values[index]#ctx.triggered[0]["value"]
#     if(flag) and binding_id not in main_app.binding_id_list:
#         main_app.binding_id_list.append(binding_id)#insert(len(fl),binding_id)
#     else:
#         main_app.binding_id_list.remove(binding_id)

#     print(f"\n\n\n----\n1)ctx.triggered_id =  {ctx.triggered_id} \n2)index = {index}\n3)flag = {values}")
#     return values
###########################
###########################
# @main_app.app.callback(
#     Output({"type":"rule_binding_page_headeing","index":ALL},"children"),
#     Input({"type":"rule_binding_table_row_number","index":ALL},"n_clicks"),
#     # State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"),
#     # State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value")
# )
# def test(rows):#,name,values):
    
#     print ("++++++++++triggered+++++++++++++++=")
#     return f"changed_{rows}"

###############################

@main_app.app.callback(
    Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
    Output(f"cb_all_{main_app.environment_details['rule_binding_table_id']}","value"),
    Output("selected_rule_ids","value"),
    Input({"type":f"{main_app.environment_details['rule_binding_table_id']}_row_number","index":ALL},"n_clicks"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"), 
    State("selected_rule_ids","value"),
)
def check_box_function_for_selecting_rules_to_run(n_clicks,checkbox_flag,name, selected_rule_ids):
      

    if ctx.triggered_id is None or n_clicks.count(None) == len(n_clicks):
        raise PreventUpdate
    
    
    index = ctx.triggered_id['index']
    binding_id = str(name[index][0]["RULE_BINDING_ID"])

    list_of_ids = [x for x in selected_rule_ids.split(",")]

    # first we check if the selected binding id is in already selected string of binding id's or not 
    if binding_id not in list_of_ids:

        #if there are no previously selected binding id's we just add the selected binding id
        if len(selected_rule_ids)==0:
            selected_rule_ids=binding_id
        
        #else we add one comma and then add the selected binding id
        else:
            selected_rule_ids+=","+binding_id
    
    #else we need to remove the selected bindind id from exisiting one
    else:
        list_of_ids.remove(binding_id)
        selected_rule_ids = ",".join(list_of_ids)

    checkbox_flag[index] = not checkbox_flag[index]
    flag = checkbox_flag.count(True)==len(checkbox_flag)

    return checkbox_flag , True if flag else None ,selected_rule_ids #no_update if checkbox_flag.count(True)!=len(checkbox_flag) else True# f"changed--{main_app.binding_id_list} - {n_clicks} - {n_clicks_2}", 



# used for showing load screen in dashboard
@main_app.app.callback(
        Output("loading_screen","style",allow_duplicate=True),
        Output("loading_message","children",allow_duplicate=True),
        Input("run_binded_rule","n_clicks"),
        State("token","data"),
        State("selected_rule_ids","value"),
        prevent_initial_call='initial_duplicate'
)
def show_rule_loading_screen(n_clicks,token,selected_rule_ids):
    try : 
        payload = decode_token(token)
        session_not_over = payload['session_end_time'] > int(time.time())
        if (session_not_over and n_clicks is not None and selected_rule_ids != ''):
            return {"visibility":"visible","opacity":"0.6"},"Rules Execution in Progress please wait....⌛"
        raise PreventUpdate
    except Exception as e :
        raise PreventUpdate

@main_app.app.callback(
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value",allow_duplicate=True),
    Output(f"cb_all_{main_app.environment_details['rule_binding_table_id']}","value",allow_duplicate=True),
    Output("refresh_button_rule_binding_page","n_clicks",allow_duplicate=True),
    Output("confirm_dialog_box","is_open",allow_duplicate=True),
    Output("selected_rule_ids","value",allow_duplicate=True),
    Output("loading_screen","style",allow_duplicate=True),
    Input("run_binded_rule","n_clicks"),
    Input("proceed_delete","n_clicks"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value"),
    State("selected_rule_ids","value"),
    prevent_initial_call = 'initial_duplicate',
)
def run_selected_rules(n_clicks,n_clicks_2,no_of_records,selected_rule_ids):

    if ctx.triggered_id is None or(n_clicks is None and n_clicks_2 is None):
        raise PreventUpdate
    
    binding_id_list = selected_rule_ids.split(",")
    print(binding_id_list)
    print(binding_id_list[0]    )
    print(binding_id_list[0]==0)

    if ctx.triggered_id == 'run_binded_rule' :
        # below proc_name is according to old mysql code
        # proc_name = 'run_one_field_rule' 
        proc_name = 'run_rule'
        refresh = no_update
    else :
        proc_name = 'delete_rule_binding'
        refresh = 0
    try:
        if binding_id_list[0] != '':
            msg = ""
            for i in binding_id_list:
                
                # main_app.cursor.callproc(proc_name,args=[i])
                stored_results = execute_stored_procedure(procedure_name=proc_name,args=[i])
                final_result  = None
                latest_result = None
                for stored_result in stored_results: #main_app.cursor.stored_results():
                    latest_result= stored_result.fetchall()
                
                for result in latest_result:
                    final_result = result

                if final_result[0] == 200: 
                    header = "Success!!"
                    icon = "success"
                elif final_result[0] == 409:
                    header = "Warning"
                    icon = "warning"
                elif final_result[0] == 500:
                    header = "Internal Error"
                    icon = "warning"
                msg = msg + "\n"+ final_result[1]

            # main_app.cursor.callproc('REFRESH_SCORE_CARD_DATA')
            # time.sleep(1)
            # latest_result = None
            # for stored_result in main_app.cursor.stored_results():
            #     latest_result= stored_result.fetchall()

            # main_app.cursor.callproc('REFRESH_TREND_CHART_DATA')
            # time.sleep(1)
            # latest_result = None
            # for stored_result in main_app.cursor.stored_results():
            #     latest_result= stored_result.fetchall()
            
            
        else :
            header = "Warning"
            icon = "warning"
            msg = "Please select a rule before running"
    except Exception as e:
        print(f"--------------{e} -------------")
        msg = msg + "\n" + "Error in SQL Execution.Please contact Support"
        header = 'Error!!'
        icon = "danger"
    duration = 5000
    # main_app.binding_id_list=[]
    return msg,header,icon,duration,True,[False for i in range(len(no_of_records))],None,refresh,False,"",{}


@main_app.app.callback(
    Output({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"value",allow_duplicate=True),
    Output("selected_rule_ids","value",allow_duplicate=True),
    Input(f"cb_all_{main_app.environment_details['rule_binding_table_id']}","value"),
    State({"type":f"cb_{main_app.environment_details['rule_binding_table_id']}","index":ALL},"name"),
    prevent_initial_call='initial_duplicate',
)
def select_and_unselect_all_rulebindings(select_all,check_boxes):
        if select_all is None :
            raise PreventUpdate
        
        print(check_boxes)

        main_app.binding_id_list = []
        binding_id_list = []
        if select_all:
            for index in range(len(check_boxes)):
                main_app.binding_id_list.append(check_boxes[index][0]["RULE_BINDING_ID"])
                binding_id_list.append(str(check_boxes[index][0]["RULE_BINDING_ID"]))

        return [select_all for i in range(len(check_boxes))],",".join(binding_id_list)


@main_app.app.callback(
    Output("confirm_dialog_box","is_open"),
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Input("delete_binded_rule","n_clicks"),
    Input("cancel_delete","n_clicks"),
    State("selected_rule_ids","value"),
    prevent_initial_call = True
)
def open_close_modal(n_clicks,n_clicks_2,selected_rule_ids):

    if ctx.triggered_id is None or n_clicks is None:
        raise PreventUpdate

    binding_id_lis=selected_rule_ids.split(",")
    if binding_id_lis[0]=='' :
        return no_update,"Select a rule to delete","Warning","warning",5000,True
    
    modal_open_or_close = ctx.triggered_id == 'delete_binded_rule'

    return modal_open_or_close,no_update,no_update,no_update,no_update,no_update