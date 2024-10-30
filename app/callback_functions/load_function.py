from dash import Output,Input,ctx, html, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from callback_functions.main_app_class import main_app
from callback_functions.custom_helpers import load_filter_and_table_for_rule_binding_page,load_latest_rule_binding_table,load_filter_and_table_for_score_card_page,decode_token
from connections.MySQL import *
from plotly.express import pie
import time



# used for showing load screen in dashboard
@main_app.app.callback(
        Output("loading_screen","style"),
        Output("loading_message","children"),
        Input("url1","pathname"),
        State("token","data"),
)
def show_dahboard_loading_screen(url,token):
    try : 
        payload = decode_token(token)
        session_not_over = payload['session_end_time'] > int(time.time())
        if (session_not_over and url == main_app.environment_details["score_card_link"]):
            return {"visibility":"visible"},"Dashboard Loading...Please Wait ⌛"
        raise PreventUpdate
    except Exception as e :
        raise PreventUpdate



@main_app.app.callback(
        Output("filters_rules_repo","children",allow_duplicate=True),
        Output("rules_repo_table_container","children",allow_duplicate=True),
        Input("refresh_button_home_page","n_clicks"),
        prevent_initial_call = 'initial_duplicate'
)
def refresh_home_page_page(n_clicks):

    if (n_clicks is None  or ctx.triggered_id is None ):
        raise PreventUpdate
    
    filters,rules_repo_table = load_filter_and_table_for_rule_binding_page()

    
    return filters,rules_repo_table



@main_app.app.callback(
        Output("filters_rule_binding","children",allow_duplicate=True),
        Output("score_card_rules_table","children",allow_duplicate=True),
        Output('pie_chart1','figure'),
        Output("loading_screen","style",allow_duplicate=True),
        # Output('pie_chart2','figure',allow_duplicate=True),
        Input("refresh_button_score_card_page","n_clicks"),
        Input("url1","pathname"),
        prevent_initial_call = 'initial_duplicate'
)
def refresh_score_card_page(n_clicks,pathname):

    if ( (n_clicks is None  or ctx.triggered_id is None) and pathname !=  main_app.environment_details['score_card_link']):
        raise PreventUpdate
    
    
    filters,top_table = load_filter_and_table_for_score_card_page()
# #61876E
    sql_query1 = "select * from pie_chart1_data"
    pie_data1 = get_data_as_data_frame(sql_query=sql_query1 , cursor = main_app.cursor)
    sum_of_values=pie_data1[pie_data1.columns[1]].sum()
    pie_chart1 = pie(data_frame=pie_data1,
                   values = pie_data1.columns[1],
                   names = pie_data1.columns[0],
                   color = pie_data1.columns[0],
                   color_discrete_map={ 'Passed_Rules' : '#00cc96' , 'Failed_Rules' : '#FB2576'},
                   title = f'Passed VS Failed Rules<br>Total Rule Bindings: {sum_of_values}',
                   hole = 0.45,
                   width =300,
                   height=200)
    
    pie_chart1.update_layout(margin=dict(l=1, r=1, t=60, b=1) , legend_y=0 , title_y = 0.9)


    # OLD FUNCTION FOR UPDATING PIE CHART 2
    # sql_query2 = f"select * from pie_chart2_data where rule_name in {str(main_app.score_card_filtered_rules).replace('[','(').replace(']',')')}"
    
    # pie_data2 = get_data_as_data_frame(sql_query=sql_query2 , cursor = main_app.cursor)
    
    # pie_chart2 = pie(data_frame=pie_data2,
    #                values = pie_data2.columns[2],
    #                names = pie_data2.columns[1],
    #                title = 'Total Records vs Failed Records',
    #                color_discrete_sequence = ['#61876E','#FB2576'],
    #                hole = 0.45,
    #                width =300,
    #                height=200)
    
    # pie_chart2.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    


    return filters,top_table,pie_chart1,{}#,pie_chart2



@main_app.app.callback(
        Output("rule_binding_table_container","children",allow_duplicate=True),
        Input("refresh_button_rule_binding_page","n_clicks"),
        Input("url1","pathname"),
        prevent_initial_call = 'initial_duplicate'
)
def refresh_rule_binding_table(n_clicks,pathname):

    if ( (n_clicks is None  or ctx.triggered_id is None) and pathname !=  main_app.environment_details['rule_execution_link']):
        raise PreventUpdate

    rule_binding_table = load_latest_rule_binding_table()

    return rule_binding_table


