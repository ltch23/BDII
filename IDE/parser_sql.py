import sqlparse

filename = 'texto.txt'
with open(filename) as f:
    data = f.readlines()

dicc=open("diccionario.txt","a+") #"a+"

for n, sql in enumerate(data, 1): # read the entire text
    sql = sql.rstrip()
    parsed = sqlparse.parse(sql)
    stmt = parsed[0]
    
    if str(stmt.tokens[0]) == "CREATE":
        number_tokens = 4 # 
        nombre =str(stmt.tokens[4]) 
        f=open("data/"+nombre+".txt","a+") #"a+"
        f.close
        dicc.write(nombre+" "+str(stmt.tokens[6])+'\n')

    if str(stmt.tokens[0]) == "INSERT":
        number_tokens = 5 # 
        nombre =str(stmt.tokens[4]) 
        f=open("data/"+nombre+".txt","a+") #"a+"
        f.write(str(stmt.tokens[8]).rstrip()+'\n')
        f.close

    if str(stmt.tokens[0]) == "DELETE":
        number_tokens = 4 # 
