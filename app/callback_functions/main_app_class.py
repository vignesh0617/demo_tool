from dash import Dash
import dash_bootstrap_components as dbc
import mysql.connector as sql

#class for creating the reconciliation app
class reconciliation_app:
    def __init__(self):
        self.app:Dash = Dash(name = "__main__",external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP],title="CIDM")
        self.connector:sql.connect = None
        self.cursor = None
        self.rule_details = None
        self.failed_data_query:str = None
        self.environment_details:dict = {}
        self.current_url:str = None
        self.binding_id_list:list[int] = []
        self.score_card_filtered_rules = []
        self.select_all_filter_id:dict = {}
        # self.score_card_selected_rule:str = None
        self.assign_environment_details()
        
    #used to read the environment.txt file and assign the values to reconciliation_app
    def assign_environment_details(self):
        # file = open(file = "app\environment.txt",mode ="r")
        file = open(file = "environment.txt",mode ="r")
        for line in file:
            if(line != "\n" and line.replace(" ","")!=""):
                for[key,value] in [line.rstrip().split(" = ")]:
                    self.environment_details[key] = value
                    
main_app = reconciliation_app() 