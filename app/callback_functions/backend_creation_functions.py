#this will read the queries from queries.txt file and return a dictionary as { table_name1 : query1, table_name2 : query2 .... }
def return_sql_queries_from_file():
    file = open(file = "queries.txt",mode = 'r')
    lines = file.readlines()
    queries = {}
    temp_query = ""
    table_name = ""
    for line in lines :
        if len(line.strip()) :
            if line.lower().find("table_name :") != -1 or line.lower().find("view_name :") != -1:
                table_name = line.split(" : ")[1][:-1]
            elif line[-2] != ";":
                temp_query+=line
            elif line[-2] == ";":
                temp_query+=line[:-2]
                queries[table_name] = temp_query
                temp_query = ""
    return queries