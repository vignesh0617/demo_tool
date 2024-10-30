
import jwt
import dash_bootstrap_components as dbc
from dash import html, Dash
from connections.MySQL import get_data_as_data_frame
from callback_functions.main_app_class import main_app
import pandas as pd
from dash import Output, Input, State
from dash.exceptions import PreventUpdate
from datetime import datetime, timedelta



# this function is used to create filter dropdown with select all feature
def create_filter_drop_down(
        filter_tables:list[str],
        filter_tables_columns:list[str],
        filter_tables_labels:list[str],
        filter_ids:list[str],
        add_filter_card:bool = False):

    filters = []

    print(f"\n\ncreating for : {filter_ids} \n\n")

    for i in range(len(filter_tables)):
        table_name = filter_tables[i]
        column_name = filter_tables_columns[i]
        column_label = filter_tables_labels[i]
        filter_id = filter_ids[i]

        
        if main_app.select_all_filter_id.get(filter_id) is None:
            main_app.select_all_filter_id[filter_id] = "function_not_created"
            
        sql_1 = f"select distinct {column_name} from {table_name}"
        data_frame = get_data_as_data_frame(sql_query=sql_1  , cursor= main_app.cursor)
        # this is the new layout model for the filter buttons with select all check box features
        layout = html.Div([
                    dbc.Label(column_label,className = "filter-label"),
                    dbc.DropdownMenu([
                        dbc.Checkbox(id=filter_id+"_select_all",label="Select All"),
                        dbc.Checklist(id=filter_id,
                                      options=data_frame[data_frame.columns[0]],
                                      value=[])
                    ],
                    label = "Select...",
                    id=filter_id+"_drop_down",
                    className= "filter_drop_down"
                    )
                ],className = "filter-card" if add_filter_card else '',
                  id = f"filter_card_{i}",
                )
        
        filters.append(layout)

    print(main_app.select_all_filter_id)
    # The below loop is used to update the labels of each filter passed and add select all functionality
    # for i in range(len(filter_ids)):
    #     filter_id = filter_ids[i]

    #     #this check prevets the app from crashing
    #     if main_app.select_all_filter_id[filter_id] == "function_not_created":

    #         #now we set it to function created. this prevents the app from creating the same function being binded
    #         #to the same filter_id.
    #         main_app.select_all_filter_id[filter_id] = "function_created"
            
    #         #trying to implement a new feature
    #         @main_app.app.callback(
    #             Output(filter_id+"_drop_down","label"),
    #             Output(filter_id+"_select_all","value"),
    #             Input(filter_id,"value"),
    #             State(filter_id,"options"),
    #             # prevent_initial_call='initial_duplicate',
    #             # State(filter_id+"_select_all","value"),
    #         )
    #         def update_filter_label_and_options(value,options):
                
    #             if(len(value)==len(options)):
    #                 return "All",True
    #             return str([item for item in value]).replace("[","").replace("]","").replace("'","") if len(value) !=0 else "Select...", None

    #         @main_app.app.callback(
    #             Output(filter_id+"_drop_down","label",allow_duplicate=True),
    #             Output(filter_id,"value",allow_duplicate=True),
    #             Input(filter_id+"_select_all","value"),
    #             State(filter_id,"options"),
    #             prevent_initial_call='initial_duplicate',
    #         )
    #         def update_filter_label_and_options(selected,options):
    #                 if selected == None :
    #                     raise PreventUpdate
    #                 elif selected :
    #                     return "All",[item for item in options]
    #                 else :
    #                     return "Select...",[]
                    

    
    print(main_app.select_all_filter_id)
    return filters


def load_filter_and_table_for_rule_binding_page():

    filter_tables = main_app.environment_details['filter_table_names_rules_repo'].split(',')
    filter_tables_columns = main_app.environment_details['filter_table_columns_rules_repo'].split(',')
    filter_tables_labels = main_app.environment_details['filter_table_labels_rules_repo'].split(',')
    filter_ids = main_app.environment_details['filter_ids_rule_repo'].split(',')

    filters = create_filter_drop_down(
        filter_tables = filter_tables,
        filter_tables_columns = filter_tables_columns,
        filter_tables_labels = filter_tables_labels,
        filter_ids = filter_ids
    )
    
    sql_query = f'select * from {main_app.environment_details["rules_repo_table_name"]}'

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,
            table_id= main_app.environment_details["rules_repo_table_id"],
            key_col_number=int(main_app.environment_details["rules_repo_table_primary_key_col_number"]),
            col_numbers_to_omit= [ int(num) for num in main_app.environment_details['rules_repo_table_col_numbers_to_omit'].split(',')],
            primary_kel_column_numbers=[int(num) for num in main_app.environment_details["rules_repo_table_primary_key_col_numbers"].split(",")],
            select_record_positon=0,
            select_record_type='radio'
            )
    
    return filters,table
    


def load_filter_and_table_for_score_card_page(): 

    filter_tables = main_app.environment_details['filter_table_names_rule_binding'].split(',')
    filter_tables_columns = main_app.environment_details['filter_table_columns_rule_binding'].split(',')
    filter_tables_labels = main_app.environment_details['filter_table_labels_rule_binding'].split(',')
    filter_ids = main_app.environment_details['filter_ids_rule_binding'].split(',')

    filters = create_filter_drop_down(
        filter_tables = filter_tables,
        filter_tables_columns = filter_tables_columns,
        filter_tables_labels = filter_tables_labels,
        filter_ids = filter_ids,
    )
    
    sql_query = main_app.environment_details['query_for_score_card_top_table']

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    data_frame.rename(columns = {
        'FAILED_RECORDS_0_DAYS_BACK':datetime.now().strftime('%b-%d'),
        'FAILED_RECORDS_1_DAYS_BACK':(datetime.now()-timedelta(days=1)).strftime('%b-%d'),
        'FAILED_RECORDS_2_DAYS_BACK':(datetime.now()-timedelta(days=2)).strftime('%b-%d'),
        'FAILED_RECORDS_3_DAYS_BACK':(datetime.now()-timedelta(days=3)).strftime('%b-%d'),
        'FAILED_RECORDS_4_DAYS_BACK':(datetime.now()-timedelta(days=4)).strftime('%b-%d')
    },inplace=True)

    
    main_app.score_card_filtered_rules = list(data_frame['RULE_NAME'])

    table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,
            table_id= main_app.environment_details["score_card_top_table_id"],
            key_col_number=int(main_app.environment_details["score_card_top_table_primary_key_col_number"]),
            col_numbers_to_omit= [ int(num) for num in main_app.environment_details['score_card_top_table_col_numbers_to_omit'].split(',')],
            primary_kel_column_numbers=[int(num) for num in main_app.environment_details["score_card_top_table_primary_key_col_numbers"].split(",")],
            select_record_type='radio',
            select_record_positon=0,
            use_mulitiple_keys=True
            )
    
    return filters,table



def load_latest_rule_binding_table():
    # sql_query = f"select * from {main_app.environment_details['rule_binding_table_name']} where is_active = 'Y'"
    sql_query = "select RULE_BINDING_ID,RULE_NAME, A.RULE_ID, DOMAIN,TABLE_NAME,COLUMN_NAME from rule_binding a inner join rules_repo b on a.RULE_ID = b.rule_id where a.is_active = 'Y' order by rule_binding_id asc"
    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    data_frame["TABLE_NAME"] = data_frame["TABLE_NAME"].apply(lambda x : x.replace("||"," , "))
    data_frame["COLUMN_NAME"] = data_frame["COLUMN_NAME"].apply(lambda x : x.replace("||"," , "))

       
    rule_binding_table = create_dash_table_from_data_frame(
        data_frame_original=data_frame,
        table_id= main_app.environment_details["rule_binding_table_id"],
        key_col_number= int(main_app.environment_details["rule_binding_table_primary_key_col_number"]),
        primary_kel_column_numbers= [int(x) for x in main_app.environment_details["rule_binding_table_primary_key_col_numbers"].split(",")],
        # col_numbers_to_omit=[int(x) for x in main_app.environment_details["rule_binding_table_col_numbers_to_omit"].split(",")],
        col_numbers_to_omit = [0],
        select_record_positon=1+len(data_frame.columns),#-len(main_app.environment_details["rule_binding_table_col_numbers_to_omit"].split(",")),
        select_record_type="checkbox",
    )

    return rule_binding_table
    

#for creating JWT
def create_token(payload, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    return jwt.encode(payload, secret_key, algorithm)

#for decoding JWT
def decode_token(token, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    
    return jwt.decode(token, secret_key, algorithm)
    
# For creating a dash table from a dataframe
# data_frame_original ---> table will be created based on this dataframe
# table_id ---> this table id should be unique for identifying a table
# key_col_number ----> 0th index. each row will store this correspoding data_frame_original.iloc[<row>,key_column_number] in its "key" attribute. This can be used later if required
# action_col_number --->0th index. a link kind of style will be applied to col_number mentioned here. Define a corresponding function to get executed when this data is pressed
# primary_key_col_numbers ----> 1st index . index's mentioned here, will get saved in form of dicitonary [{"col name1" : "vale1" },{"col name2" : "vale2" }......{{"col namen" : "valen" }}]
# capital_headings ----> Headings of the table header will be Capital letters if this value is True else it will be Title
# col_numbers_to_omit ---->0th index. these index's will be omitted while creating tables in front end  
# select_record_type ------> indicates if to select the single(radio button) or multiple(check box) records . Options to pass "single" or "multiple"
# select_record_positon ---> 0th index. where to insert the selected record
# generate_srno -----> if set to true it will generate S.no for each record
# no_record_msg ---> if the passed data frame has no records it will return a single row with the user specified msg.
def create_dash_table_from_data_frame(
        data_frame_original:pd.DataFrame,
        table_id:str,
        key_col_number:int,
        use_mulitiple_keys:bool = False,
        action_col_numbers:list[int] = [],
        primary_kel_column_numbers:list[int] = [],
        capital_headings:bool =False,
        col_numbers_to_omit:list[int] = [],
        select_record_type:str = "radio",
        select_record_positon:int = None,
        generate_srno:bool = True,
        disable_check_box:bool = True,
        no_records_msg:str = "No Records to display",
        create_simmple_table:bool = False
    ):
    
    # creates a duplicate data_frame which will omit the col_number mentioned in  "col_numbers_to_omit"
    if col_numbers_to_omit: # this if block will execute only if col_numbers_to_omit array is not empty
        col_range = []
        for i in range(data_frame_original.shape[1]):
            if(i not in col_numbers_to_omit):
                col_range.append(i)
        
        data_frame = data_frame_original.iloc[:,col_range]
    else :
        data_frame = data_frame_original

    
    table_headings = [] # stores all th html values
    table_records = [] # stores all td html vales
    no_of_rows = len(data_frame.index) 
    no_of_cols = len(data_frame.columns)

    for col_label in data_frame.columns:
    
        table_headings.append(
            html.Th(
                children = col_label.upper() if capital_headings else col_label.title()
            )
        )

    if generate_srno:
        table_headings.insert(0,
            html.Th(
                children = "S.NO" if capital_headings else "S.no"
            )
        )

    if select_record_positon is not None :#and (select_record_positon == index ):
        if select_record_type.lower() == 'radio':
            table_headings.insert(select_record_positon,
                html.Th(
                    children = "SELECT" if capital_headings else "Select"
                )
            )
        else : #select_record_type.lower() == 'checkbox' :
            # cb = dbc.Checkbox(id=f"cb_all_{table_id}",label=""),
            table_headings.insert(select_record_positon,
                html.Th(
                    children = [
                        # "Select all",
                        dbc.Checkbox(id=f"cb_all_{table_id}",label="SELECT ALL" if capital_headings else "Select All",disabled= (no_of_rows == 0))
                    ]
                )
            )
    
    #
    #
    #from here i need to try to improve the perfomance using multi processing in python
    #
    #
    #
    unique_id = 0 # this unique_id is used to identify each key attribute in "td" 
    for row in range(no_of_rows):
        records = []
        for col in range(no_of_cols):
            records.append(
                html.Td(data_frame.iloc[row,col]) if create_simmple_table else 
                html.Td(
                    children = data_frame.iloc[row,col],
                    id = {'type' : f"{table_id}_row_data",'index' : unique_id} if col in action_col_numbers else {"type":f"{table_id}_row{row}" ,"index" : col},#f"{table_id}_row_data_row-{row}_col-{col}" ,
                    key = {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] , "primary_keys" : [{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ]} if col in action_col_numbers else {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] },
                    className = "table_action" if col in action_col_numbers and data_frame.iloc[row,col]!=0 else ""
                ) 
            )

                       
            if col in action_col_numbers:
                unique_id+=1
        if generate_srno :
            records.insert(0,
                html.Td(
                    children = row+1,
                    )
            )
        if select_record_positon is not None:#  and select_record_positon == col:
                if select_record_type.lower() == 'radio':
                    records.insert(select_record_positon,
                        html.Td(
                            children = [
                                dbc.RadioButton(id={"type":f"rb_{table_id}","index":row},
                                                label="",
                                                name=[{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ],
                                                value=False)#=data_frame.iloc[row,key_col_number])
                            ],
                            
                        )
                    )
                else :
                    records.insert(select_record_positon,
                        html.Td(
                            children = [
                                dbc.Checkbox(id={"type":f"cb_{table_id}","index":row},
                                             label="",
                                             name=[{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ],
                                             disabled=disable_check_box,
                                             value=False)#=data_frame.iloc[row,key_col_number])
                            ],
                            
                        )
                    )
        if use_mulitiple_keys : 
            key_value = dict(data_frame_original.iloc[row,[num-1 for num in primary_kel_column_numbers]])
        else:
            key_value = data_frame_original.iloc[row,key_col_number] 
        table_records.append(
            html.Tr(
                children = records,
                id = {
                    'type' : f"{table_id}_row_number",
                    'index' : row
                },
                # id = f"{table_id}_row{row}",
                key = key_value
            )
        )

    
    #
    #
    #till here
    #
    #
    #
    
    if no_of_rows == 0:
        table_records.append(
            html.Tr(
                children = [
                    html.Td(
                        children=no_records_msg,
                        colSpan= len(table_headings),
                        style={'text-align':'center'}
                    )
                ]
            )
        )
    final_table = html.Table([
        html.Thead(
            html.Tr(
                table_headings
            )
        ),
        html.Tbody(
            table_records
        )
    ],id = table_id ,className="table table-hover table-light")


    return final_table



#below function adds select all functionality to specified filter ids
filter_ids = main_app.environment_details['filter_ids_rule_repo'].split(",")+main_app.environment_details['filter_ids_rule_binding'].split(",")
for i in range(len(filter_ids)):
    filter_id = filter_ids[i]
    #now we set it to function created. this prevents the app from creating the same function being binded
    #to the same filter_id.
    
    #trying to implement a new feature
    @main_app.app.callback(
        Output(filter_id+"_drop_down","label"),
        Output(filter_id+"_select_all","value"),
        Input(filter_id,"value"),
        State(filter_id,"options"),
        # prevent_initial_call='initial_duplicate',
        # State(filter_id+"_select_all","value"),
    )
    def update_filter_label_and_options(value,options):
        
        if(len(value)==len(options)):
            return "All",True
        return str([item for item in value]).replace("[","").replace("]","").replace("'","") if len(value) !=0 else "Select...", None

    @main_app.app.callback(
        Output(filter_id+"_drop_down","label",allow_duplicate=True),
        Output(filter_id,"value",allow_duplicate=True),
        Input(filter_id+"_select_all","value"),
        State(filter_id,"options"),
        prevent_initial_call='initial_duplicate',
    )
    def update_filter_label_and_options(selected,options):
            if selected == None :
                raise PreventUpdate
            elif selected :
                return "All",[item for item in options]
            else :
                return "Select...",[]
            
