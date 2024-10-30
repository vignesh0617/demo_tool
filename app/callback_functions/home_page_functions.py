from dash.dependencies import Output, Input, State
from dash import no_update,ctx,html
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import create_dash_table_from_data_frame
import pandas as pd
import plotly.express as px
from connections.MySQL import get_data_as_data_frame
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import dcc,MATCH,ALL


#this function is for filtering the table names according to domain filter
# @main_app.callback(
#         Output(),
# )

#this function will apply the filter values to rules repo table 
@main_app.app.callback(
    Output("rules_repo_table_container", "children",allow_duplicate=True),
    # Input("apply_filter_button_rules_repo2","n_clicks"),
    [[State(filter_id,"options"),Input(filter_id,"value")] for filter_id in main_app.environment_details['filter_ids_rule_repo'].split(',')],
    prevent_initial_call = True 
)
def apply_filter_for_rules_repo_table(*filter_options_and_values):

    if ctx.triggered_id is None : raise PreventUpdate

    filter_columns = main_app.environment_details['filter_table_columns_rules_repo'].split(',')

    filter_options = [filter_options_and_values[index][0] for index in range(0,len(filter_options_and_values))]
    
    filter_values = [filter_options_and_values[index][1] for index in range(0,len(filter_options_and_values))]

    dictionary = dict([filter_columns[index],filter_values[index]] for index in range(len(filter_values)))
    
    sql_query = f'select * from {main_app.environment_details["rules_repo_table_name"]}'

    index = 0
    for column_name,filter_value in dictionary.items():
        if(filter_value is not None):
            if(len(filter_value)!=0 and len(filter_options[index]) != len(filter_value)):
                sql_query+=f" {' and ' if sql_query.find('where')!=-1 else ' where '} {column_name} in {filter_value} "
        index+=1

    sql_query = sql_query.replace("[","(").replace("]",")")

    # print(f"SQL Query =========== \n\n\n\n{sql_query}\n\n\n\n")

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    if(len(data_frame != 0)):
        table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,
            table_id= main_app.environment_details["rules_repo_table_id"],
            key_col_number=int(main_app.environment_details["rules_repo_table_primary_key_col_number"]),
            col_numbers_to_omit= [int(num) for num in main_app.environment_details["rules_repo_table_col_numbers_to_omit"].split(",")],
            primary_kel_column_numbers=[int(num) for num in main_app.environment_details["rules_repo_table_primary_key_col_numbers"].split(",")],
            select_record_positon=0,
            select_record_type='radio'
            )
       
    else :
        table = "No records found for the applied filter"
    
    print("-------------------Filter Applied-----------------")
    print(sql_query)

    return table


# function for clear all button
@main_app.app.callback(
    [Output(filter_id+"_select_all","value",allow_duplicate=True) for filter_id in main_app.environment_details["filter_ids_rule_repo"].split(",")],
    Input("clear_filter_button_rules_repo","n_clicks"),
    prevent_initial_call=True
)
def clear_all_filters(n_clicks):
    return [False for filter_id in main_app.environment_details["filter_ids_rule_repo"].split(",")]


# helper function for getting the tables belonging to particular domain
def get_tables_for_domain(domain : list[str] )-> list[str]:
    sql_query = f'select distinct {main_app.environment_details["table_col_name"]} from {main_app.environment_details["information_schema_table_name"]} where {main_app.environment_details["database_col_name"]} = "{main_app.environment_details["database_name"]}" and {main_app.environment_details["table_col_name"]} not in ("rule_binding","rules_repo","run_history","trend_chart_base","trend_chart_data","trend_chart_data_1_months","trend_chart_data","trend_chart_data_3_months","trend_chart_data","trend_chart_data_6_months","ui_score_card_top_table","binded_rules","pie_chart1_data","pie_chart2_data","score_card","score_card_history","score_card_latest","ui_score_card_top_table_latest_data","custom_rules_request","users","comments","last_update_time","domain_table_map")and {main_app.environment_details["table_col_name"]} not in (select distinct failed_data_table_name from rule_binding)'

    if domain :
        sql_query += f' and {main_app.environment_details["table_col_name"]} IN (SELECT `TABLE_NAME` FROM DOMAIN_TABLE_MAP WHERE DOMAIN IN {domain})'
        sql_query = sql_query.replace("[","(").replace("]",")")

    data_frame = get_data_as_data_frame(sql_query=sql_query)

    tables_names = [ table_name for table_name in data_frame[data_frame.columns[0]]]

    return tables_names

# it will also filter the tables accodring to domain name wise if domain filter is chosen
@main_app.app.callback(
    Output({"type":"source_table_mapper","index":ALL},"options",allow_duplicate= True),
    Input("rr_domain_f","value"),
    State({"type":"source_table_mapper","index":ALL},"options"),
    prevent_initial_call= True
)
def update_source_tables(domain,no_of_source_tables):#,key,filter_domain_value):

    table_names = get_tables_for_domain(domain=domain)
    options= [{"label" : table_name.upper(), "value":table_name} for table_name in table_names]

    return [options for i in range(len(no_of_source_tables))]


# function that will run when radio button is clicked in rules repo table.
@main_app.app.callback(
    Output({"type":f'rb_{main_app.environment_details["rules_repo_table_id"]}',"index":ALL},"value"),
    Output('home_page_contents_bottom','children'),
    Input({"type":f'{main_app.environment_details["rules_repo_table_id"]}_row_number',"index":ALL},"n_clicks"),
    State({"type":f'rb_{main_app.environment_details["rules_repo_table_id"]}',"index":ALL},"name"),
    State("rr_domain_f","value"),
)
def rule_binding_layout_creator(row_numbers,key,domain):#domain,key,filter_domain_value):

    if ctx.triggered_id is None:
        raise PreventUpdate
    
    
    rule_details = {}

    for dictionary in key[ctx.triggered_id["index"]] : # returns an array of dict obj's with colname:col value pairs
        rule_details = {**rule_details,**dictionary}
        
    
    main_app.rule_details = rule_details

    table_names = get_tables_for_domain(domain=domain)

    source_table_mapper = []
    for i in range(rule_details["NO_OF_SOURCE_TABLES"]):
        label = rule_details["TABLE_PARAM_NAME"].split("||")[i]

        # it tries to take default label value from back end. If that default label is not present in backend
        # then "Source Table 1, Source Table 2 .... Source Table n" will be used as default label
        label = f"Source Table {i+1} : " if  label == "" or label is None else label
        layout = html.Div(id=f'source{i+1}',children=[
            dbc.Label(label),
            dbc.Select(id={"type":"source_table_mapper","index":i+1},
                   options= [{"label" : table_name.upper(), "value":table_name} for table_name in table_names],
                   placeholder='Choose Table First...',
                   className = 'field_mapper'),
        ],
        className='label_dropdown_container')
        source_table_mapper.append(layout)



    field_mapper = []
    for i in range(rule_details["NO_OF_FIELDS"]):
        label = rule_details["PARAM_NAME"].split("||")[i]
        label = f"Field {i+1} : " if  label == "" or label is None else label
        layout = html.Div(id=f'field{i+1}',children=[
            dbc.Label(label),
            dbc.Select(id={"type":"field_mapper","index":i+1},
                   options= [],
                   placeholder='Select Table',
                   className = 'field_mapper'),
        ],
        className='label_dropdown_container')
        field_mapper.append(layout)

    layout = html.Div(children = [
            html.Div(id="rule_heading",children=[
            html.Span(id='rule_label',children=f'Selected Rule : '), 
            html.Span(id="rule_name",children=f'{rule_details["RULE_NAME"]}')
        ]),
        
        html.Div(id='rule_binding_container_inside',
                 children=[
                    # Old layout for updating options and values of selected rules
                    # html.Div(id="table_selecotr_container",children=[
                    #     dbc.Label(f"Select Table : "),
                    #     dbc.Select(id='table_selector',
                    #             options= [{"label" : table_name.upper(), "value":table_name} for table_name in data_frame[data_frame.columns[0]]],
                    #             placeholder='Select Table ...',
                    #             className = 'table_selector'
                    #         ),
                    # ]),
                    
                    html.Div(id = 'source_mapper_container',children=[
                            layout for layout in source_table_mapper
                        ]),

                    html.Div(id = 'field_mapper_container',children=[
                            layout for layout in field_mapper
                        ]),

                    dbc.Button("Bind",id="bind_rule",className = "btn-theme1"),
                    # dbc.Button("Bind & Run",id="bind_and_run_rule"),
                 ]),
        
    ],className = 'rule_binding_container')
    return [True if ctx.triggered_id["index"] == i else False for i in range(len(key))],layout
            
