from dash import html, Output, Input,State,ALL,ctx
from dash.exceptions import PreventUpdate
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import create_dash_table_from_data_frame
from connections.MySQL import get_data_as_data_frame
from plotly.express import pie,line
from datetime import datetime,timedelta

# @main_app.app.callback(
    
#     Output('trend_chart','figure',allow_duplicate=True),
#     Input("trend_chart_option","value"),
#     prevent_initial_call='initial_duplicate'
# )
# def update_trend_chart(trend_chart_type):

#     sql_query = f'select * from trend_chart_data_{trend_chart_type}_months where rule_name = "{main_app.score_card_selected_rule}"'
#     trend_data = get_data_as_data_frame(sql_query=sql_query , cursor = main_app.cursor)
#     trend_chart = line(data_frame=trend_data,
#                      x='MONTH_YEAR',
#                      y=['PASS_PERCENTAGE','FAIL_PERCENTAGE'],
#                      title = 'Trend Chart',
#                      color_discrete_sequence = ['#61876E','#FB2576'],
#                      hover_data = ['PASSED_RECORDS','FAILED_RECORDS'],
#                      width =550,
#                      height=250)
    
#     trend_chart.update_layout(margin=dict(l=20,r=20,t=40,b=20))
#     trend_chart.update_xaxes(title='', visible=True, showticklabels=False)
#     trend_chart.update_yaxes(title='', visible=True, showticklabels=True)
#     trend_chart.update_layout(showlegend=False)
    
#     return trend_chart



@main_app.app.callback(
    
    Output('score_card_rules_table','children',allow_duplicate=True),
    Output({'type' : f"{main_app.environment_details['score_card_top_table_id']}_row_number",'index' : 0},'n_clicks'),
    # Output('pie_chart2','figure',allow_duplicate=True),
    State({'type' : f"{main_app.environment_details['score_card_top_table_id']}_row_number",'index' : 0},'n_clicks'),
    [Input(filter_id,"value") for filter_id in main_app.environment_details["filter_ids_rule_binding"].split(",")],
    prevent_initial_call='initial_duplicate'
)
def filter_score_card_rules(n_click,*filter_values):

    
    filter_columns = main_app.environment_details['filter_table_columns_rule_binding'].split(',')

    dictionary = dict([filter_columns[index],filter_values[index]] for index,value in enumerate(filter_values))

    

    sql_query = main_app.environment_details['query_for_score_card_top_table']

    index = 0
    for column_name,filter_value in dictionary.items():

        if(len(filter_value) != 0):
            sql_query+=f" {' and ' if sql_query.find('where')!=-1 else ' where '} {column_name} in {filter_value} "
        index+=1

    sql_query = sql_query.replace("[","(").replace("]",")")

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    data_frame.rename(columns = {
        'FAILED_RECORDS_0_DAYS_BACK':datetime.now().strftime('%b-%d'),
        'FAILED_RECORDS_1_DAYS_BACK':(datetime.now()-timedelta(days=1)).strftime('%b-%d'),
        'FAILED_RECORDS_2_DAYS_BACK':(datetime.now()-timedelta(days=2)).strftime('%b-%d'),
        'FAILED_RECORDS_3_DAYS_BACK':(datetime.now()-timedelta(days=3)).strftime('%b-%d'),
        'FAILED_RECORDS_4_DAYS_BACK':(datetime.now()-timedelta(days=4)).strftime('%b-%d')
    },inplace=True)
    
    main_app.score_card_filtered_rules = list(data_frame['RULE_NAME'])

    rules_table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,
            table_id= main_app.environment_details["score_card_top_table_id"],
            key_col_number=int(main_app.environment_details["score_card_top_table_primary_key_col_number"]),
            use_mulitiple_keys = True,
            col_numbers_to_omit= [ int(num) for num in main_app.environment_details['score_card_top_table_col_numbers_to_omit'].split(',')],
            primary_kel_column_numbers=[int(num) for num in main_app.environment_details["score_card_top_table_primary_key_col_numbers"].split(",")],
            select_record_type='radio',
            select_record_positon=0,
            )
    

    
    # sql_query2 = f"select * from pie_chart2_data where rule_name in {str(main_app.score_card_filtered_rules).replace('[','(').replace(']',')')}"
    
    # pie_data2 = get_data_as_data_frame(sql_query=sql_query2 , cursor = main_app.cursor)
    
    # pie_chart2 = pie(data_frame=pie_data2,
    #                values = pie_data2.columns[2],
    #                names = pie_data2.columns[1],
    #                title = 'Total Records VS Failed Records',
    #                color_discrete_sequence = ['#61876E','#FB2576'],
    #                hole = 0.45,
    #                width =300,
    #                height=200)
    
    # pie_chart2.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    
    
    
    return rules_table,n_click+1 if n_click is not None else 1#,pie_chart2


@main_app.app.callback(
    
    [Output(filter_id,"value",allow_duplicate=True) for filter_id in main_app.environment_details['filter_ids_rule_binding'].split(",")],
    Input("clear_filter_button","n_clicks"),
    prevent_initial_call="initial_duplicate"
)
def clear_all_button_score_card_page(n_clicks):

    return [[] for i in main_app.environment_details['filter_ids_rule_binding'].split(",")]

