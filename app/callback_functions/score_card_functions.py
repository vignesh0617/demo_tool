from dash import html, Output, Input,State,ALL,ctx,clientside_callback,dcc
from dash.exceptions import PreventUpdate
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import create_dash_table_from_data_frame
from connections.MySQL import get_data_as_data_frame
from plotly.express import pie,line
from callback_functions.side_filter_tab_function import *
from datetime import datetime as dt
import pandas as pd


@main_app.app.callback(
    
    Output({"type":f'rb_{main_app.environment_details["score_card_top_table_id"]}',"index":ALL},"value"),
    Output('trend_chart_1_month','figure'),
    Output('trend_chart_3_month','figure'),
    Output('trend_chart_6_month','figure'),
    Output('score_card_binded_rules','children'),
    Output('pie_chart2','figure'),
    # Output("client_side_data","data"),
    Input({'type' : f"{main_app.environment_details['score_card_top_table_id']}_row_number",'index' : ALL},'n_clicks'),
    State({'type' : f"{main_app.environment_details['score_card_top_table_id']}_row_number",'index' : ALL},'key'),
    State({"type":f'rb_{main_app.environment_details["score_card_top_table_id"]}',"index":ALL},"name"),
)
def update_bottom_table1_failed_records(n_clicks,keys,key_for_radio_button,):

    if(ctx.triggered_id is None ):
        raise PreventUpdate
    
    rule_name = keys[ctx.triggered_id['index']]['RULE_NAME']
    table_name = keys[ctx.triggered_id['index']]['TABLE_NAME']
    column_name = keys[ctx.triggered_id['index']]['COLUMN_NAME']
    failed_data_table_name = keys[ctx.triggered_id['index']]['FAILED_DATA_TABLE_NAME']
    run_id = keys[ctx.triggered_id['index']]['LATEST_RUN_ID']



    sql_query2 = f"select * from pie_chart2_data where run_id = {run_id}"
    
    pie_data2 = get_data_as_data_frame(sql_query=sql_query2 , cursor = main_app.cursor)

    sum_of_values = pie_data2[pie_data2.columns[3]].sum()
 
    pie_chart2 = pie(data_frame=pie_data2,
                   values = pie_data2.columns[3],
                   names = pie_data2.columns[2],
                   color = pie_data2.columns[2],
                   color_discrete_map={ 'Passed_Records' : '#00cc96' , 'Failed_Records' : '#FB2576'},
                   title = f'Passed Vs Failed Records<br>Total Records : {sum_of_values} ',
                   hole = 0.45,
                   width =300,
                   height=200)
    
    pie_chart2.update_layout(margin=dict(l=1, r=1, t=60, b=1) , legend_y=0 , title_y = 0.9)
    
    # main_app.score_card_selected_rule = selected_rule

    sql_query = f'select * from {failed_data_table_name} where run_id = "{run_id}"'

    main_app.failed_data_query = sql_query

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)



    score_card_binded_rules_table = create_dash_table_from_data_frame(
            data_frame_original=data_frame.iloc[0:40,:],
            table_id= main_app.environment_details["score_card_bottom1_table_id"],
            key_col_number=int(main_app.environment_details["score_card_bottom1_table_primary_key_col_number"]),
            col_numbers_to_omit= [ int(num) for num in main_app.environment_details['score_card_bottom1_table_col_numbers_to_omit'].split(',')],
            create_simmple_table=True,
            # primary_kel_column_numbers=[int(num) for num in main_app.environment_details["score_card_bottom1_table_primary_key_col_numbers"].split(",")],
            # action_col_numbers=[int(num) for num in main_app.environment_details['score_card_bottom1_table_col_action_col_number'].split(",")],
            )
    


    trend_charts=[]

    
    sql_queries = [f'select * from trend_chart_data where rule_name = "{rule_name}" and table_name = "{table_name}" and column_name = "{column_name}" and date2 > sysdate() - interval day(sysdate()) day',f'select * from trend_chart_data where rule_name = "{rule_name}" and table_name = "{table_name}" and column_name = "{column_name}" and date2 > sysdate() - interval 3 month',f'select * from trend_chart_data where rule_name = "{rule_name}" and table_name = "{table_name}" and column_name = "{column_name}"']
    chart_titles = ["1 Month","3 Months","6 Months"]
    for i in range(3):

        sql_query = sql_queries[i]
        
        trend_data = get_data_as_data_frame(sql_query=sql_query , cursor = main_app.cursor)

        
        trend_chart = line(data_frame=trend_data,
                        x='DATE',
                        y='FAILED_RECORDS',
                        title = chart_titles[i],
                        color_discrete_sequence = ['#FB2576'],
                        #  hover_data = ['PASSED_RECORDS','FAILED_RECORDS'],
                        width =615,
                        height=200)
        
        trend_chart.update_layout(margin=dict(l=20,r=20,t=40,b=20))
        
        trend_chart.update_xaxes(title='', visible=True, showticklabels=False)
        trend_chart.update_yaxes(title='', visible=True, showticklabels=True)
        trend_chart.update_layout(showlegend=False)
        trend_chart.update_layout(yaxis_range=[-5,trend_data['FAILED_RECORDS'].max()+10 if trend_data['FAILED_RECORDS'].max() != 0 else 100])

        trend_charts.append(trend_chart)
        
    return [True if ctx.triggered_id["index"] == i else False for i in range(len(key_for_radio_button))],trend_charts[0],trend_charts[1],trend_charts[2],score_card_binded_rules_table,pie_chart2

    # return [True if ctx.triggered_id["index"] == i else False for i in range(len(key_for_radio_button))],trend_charts[0],trend_charts[1],trend_charts[2]

    # return [True if ctx.triggered_id["index"] == i else False for i in range(len(key_for_radio_button))],trend_charts[0],trend_charts[1],trend_charts[2],data_frame.to_html()


# clientside_callback(
#     '''
#     function sample(dict_data){
#         console.log("received data :  ");
#         return "dumil"
#     }
#     ''',
#     Output("score_card_binded_rules","children"),#,allow_duplicate=True),
#     Input({'type' : f"{main_app.environment_details['score_card_top_table_id']}_row_number",'index' : ALL},'n_clicks'),
#     # Input("client_side_data","data"),
#     # prevent_initial_call = 'initial_duplicate'
    
# )


@main_app.app.callback(
    Output('failed_dataset','data'),
    Output("info_toast","children",allow_duplicate=True),
    Output("info_toast","header",allow_duplicate=True),
    Output("info_toast","icon",allow_duplicate=True),
    Output("info_toast","duration",allow_duplicate=True),
    Output("info_toast","is_open",allow_duplicate=True),
    Input('download_failed_data','n_clicks'),
    prevent_initial_call = True
)
def download_failed_dataset(n_clicks):

    print("=====================\n\nDownload executed\n\n===========================")

    if n_clicks is None:
        raise PreventUpdate
    data_frame = get_data_as_data_frame(sql_query=main_app.failed_data_query,cursor=main_app.cursor)
    timestamp = str(dt.now())
    return dcc.send_data_frame(data_frame.iloc[:,4:].to_csv,filename = f"CIDM_Export_{timestamp[:10]}_{timestamp[11:19]}.csv"),"File downloaded!","Info","info",2000,True
    # return dcc.send_data_frame(data_frame.iloc[:,4:].to_excel,filename = f"CIDM_Export_{timestamp[:10]}_{timestamp[11:19]}.xlsx",sheet_name = "Failed Data"),"File downloaded!","Info","info",2000,True
