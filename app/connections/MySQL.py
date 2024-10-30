import mysql.connector as sql
from mysql.connector import errorcode
from callback_functions.backend_creation_functions import return_sql_queries_from_file
from callback_functions.main_app_class import main_app
import pandas as pd

# its used for adding sample data into cidm for testing purpose:
def add_sample_data(cursor) -> None :

    if main_app.environment_details["add_sample_data"] == '0':
        return
    
    queries_output_path = "connections\sample_data\\"

    def execute_query(query):
        cursor.execute(query)
        print(f'Inserted rows : {cursor.rowcount}' )
        
    def execute_create_and_insert_queries(file_name):
        print("\n-----------------\nExecuting for file : ",file_name)
        query_file = open(queries_output_path+file_name+".txt",encoding="utf8")
        lines = query_file.readlines()
        query_file.close()

        total_insert_lines = 0
        flag = True
        sql_query = ''
        create_statement=''
        
        for line in lines:
            if flag:
                if line.find("INSERT INTO") != -1:
                    insert_into = line
                    sql_query = insert_into
                    # create_statement = create_statement.replace("VARCHAR(512)","TEXT").replace("INT,","TEXT,").replace("DOUBLE,","TEXT,")
                    print(f'creating table : {create_statement[13:create_statement.find("(")]}')
                    execute_query(create_statement)
                    flag = False
                else :
                    create_statement += line
                continue
                    
                
            sql_query += line

            total_insert_lines+=1

            if total_insert_lines == 3000:
                sql_query = sql_query[:-2]
                execute_query(sql_query)
                sql_query = insert_into
                total_insert_lines = 0

        execute_query(sql_query)

    table_names = ['LFA1', 'LFB1', 'LFBK', 'LFM1', 'LFBW', 'EKKO', 'DFKKBPTAXNUM', 'MARA', 'MBEW', 'MVKE', 'MLAN', 'MAKT', 'KNB1', 'KNVV', 'KNVP', 'KNBK']
    for file_name in table_names :
        try :
            execute_create_and_insert_queries(file_name)
        except Exception as e:
            print("\n============================\n\nWarning!!\n",e)
            
            
        
    print("\n\n+++++=Over=++++++")

# this function will return the queries from text file

def get_backend_queries()-> list[str]:
    curr_query = ""
    curr_delimiter = ";"
    dict = {
        ";" : ";",
        "DELIMITER //" : "END//"
    }

    # with open("app\connections\mysql_queries_final.txt","r") as file:
    with open("connections\mysql_queries_final.txt","r") as file:
        lines = file.readlines()
        queries = []
        for line in lines : 
            if(line[:2] != "--" and line.lstrip()!=""):
                if line[:12] == "DELIMITER //" : curr_delimiter = "DELIMITER //"
                curr_query += line
                if(line[-2:-1] == dict[curr_delimiter] or line[-6:-1] == dict[curr_delimiter]):
                    if curr_delimiter !=";":curr_query=curr_query[13:-3]
                    queries.append(curr_query)
                    curr_query=""
                    curr_delimiter = ";"
    return queries

                    
def create_the_required_backend_tables(username,password):
    connector = sql.connect(
            user = main_app.environment_details['username'], 
            password = main_app.environment_details['password'], 
            host = main_app.environment_details['host'] ,
            autocommit =True) 
    cursor = connector.cursor()
    cursor.execute(f"create database {main_app.environment_details['database_name']}")
    cursor.execute(f"use {main_app.environment_details['database_name']}")
    # queries = return_sql_queries_from_file()
    queries = get_backend_queries()

    # for table_name, query in queries.items():
    #     try : 
    #         cursor.execute(query)
    #     except Exception as e:
    #         print(f"\n\n\n======================Can not execute the below query\n\n {query}\n\n====================")

    
    for query in queries:
        try : 
            cursor.execute(query)
        except Exception as e:
            print(f"\n\n\n======================Can not execute the below query\n\n {query}\n\n because : {e}====================")
    
    add_sample_data(cursor=cursor)
    return connector,cursor,True
    

#creates a backend connection with mysql connector and return the connection
def get_connection(username=main_app.environment_details['username'],password=main_app.environment_details['password']):
    try:
        connector = sql.connect(
            user = username, 
            password = password, 
            host = main_app.environment_details['host'] , 
            database = main_app.environment_details["database_name"],
            autocommit =True) 
        return connector,connector.cursor(),True
    except sql.Error as error :
        if (error.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            print("Invalid username/password")
            return None,None,False
        elif (error.errno == errorcode.ER_BAD_DB_ERROR) :
            print("Required backend database and tables not found, creating the requeried tables and database")
            return create_the_required_backend_tables(username=username,password=password)
        else :
            print("Something unexpected happened. Contact support")
            print(error)
            return None,None,False
    
#gets tables data and returns it from the selected database as a dataframe obj
def get_data_as_data_frame(sql_query,cursor = None) -> pd.DataFrame:
    try :
        new_connector, new_cursor, flag = get_connection()
        new_cursor.execute(sql_query)
        fields = new_cursor.description
        data = new_cursor.fetchall()
        column_labels = [row[0] for row in fields]
        new_cursor.close()
        new_connector.close()
        return pd.DataFrame(data = data, columns= column_labels)
    except Exception as e :
        print(f'The sql query = {sql_query}')
        print('-----------------The exception is ---------------------\n',e)
        return 'Error'
        

main_app.connector, main_app.cursor, flag = get_connection() #connector,connector.cursor(),True



def get_data_as_tuple(sql_query:str):
    try :
        new_connector, new_cursor, flag = get_connection()
        new_cursor.execute(sql_query)
        res = new_cursor.fetchall()
        new_cursor.close()
        new_connector.close()
        return res
    except Exception as e :
        print(f'The sql query = {sql_query}')
        print('-----------------The exception is ---------------------\n',e)
        return 'Error'

def execute_stored_procedure(procedure_name :str ,args : list[str] = None ):

    connector,cursor,flag = get_connection()
    if args is None:
        cursor.callproc(procedure_name)
        stored_results = cursor.stored_results()
    else:
        cursor.callproc(procedure_name,args = args)
        stored_results = cursor.stored_results()
    cursor.close()
    connector.close()
    

    return stored_results
# main_app.connector, main_app.cursor, flag = get_connection()
# cursor.execute(sql_query)
# fields = cursor.description
# data = cursor.fetchall()
# column_labels = [row[0] for row in fields]
# return pd.DataFrame(data = data, columns= column_labels)





