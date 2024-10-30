i=1
curr_query = ""
curr_delimiter = ";"
dict = {
    ";" : ";",
    "DELIMITER //" : "END//"
}

with open("app\connections\mysql_queries_final.txt","r") as file:
    lines = file.readlines()
    queries = []
    for line in lines : 
        if(line[:2] != "--" and line.lstrip()!=""):
            if line[:12] == "DELIMITER //" : curr_delimiter = "DELIMITER //"
            curr_query += line
            if(line[-2:-1] == dict[curr_delimiter] or line[-6:-1] == dict[curr_delimiter]):
                queries.append(curr_query)
                curr_query=""
                curr_delimiter = ";"

# for query in queries:
#     print(query)
        
print(len(queries))