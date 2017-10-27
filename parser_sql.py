import csv
import fileinput
import datetime
import time
import sqlparse
import collections
import json
import ast
import pandas as pd
import sys
import chilkat
from collections import OrderedDict
from tabulate import tabulate



max_size = 17
string_queue = '_QUEUE.csv'

# for print csv
def print_csv(filepath):
    with open(filepath) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            print row

# to modify the long of list with a maximum value
def size_modifier_list(list_normal):
    for i in range(len(list_normal)):
        largo = len(str(list_normal[i]))
        s = str(list_normal[i])+' '*(max_size-largo)+''
        list_normal[i] = s

# to create the csv with header    
def creator_csv(pathfile, header):
    with open(pathfile, 'w') as csvfile: # only for create a .csv with header
            fieldnames = header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # to create the CSV, it'll contain the linked list when you delete a register
    indice_1 = pathfile.index('/')
    indice_2 = pathfile.index('.csv')
    path = pathfile[:indice_1]
    rest = pathfile[indice_1+1:indice_2]

    path_final = path+'/'+rest+string_queue
    with open(path_final, 'w') as csvfile: # only for create a .csv with header
            fieldnames = ['NUMERO_LINEA']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

# to fill the csv with contents 
def fill_csv(pathfile, content):
    with open(pathfile, 'a') as csvfile:

            # change this function, cuz is too expensive
            # only is necesary read the first line and dont charge all the .csv in one line
            # CHANGE BROOO !
            with open(pathfile, 'rb') as f: # for extract the header and add to dictionary for add to .csv
                reader = csv.reader(f)
                list_reader = list(reader)
    
            data_header = list_reader[0] # we only extract the header -> first line
            writer = csv.DictWriter(csvfile, fieldnames=data_header) # indicate the order and Dictionary
            
            line_contain=OrderedDict() # create line_contain dictionary and order by default with OrderedDict

            for i in range(len(content)): # fill the dictionary with header values and fieldcontain values
                line_contain.__setitem__(data_header[i], content[i])
            writer.writerow(line_contain)


# to create a file with .csv extension
def create_file(stmt):
    list_1 = str(stmt.tokens[8]) # extract the block 8 (its contains name_column and type of name_column)
    list_1 = (list_1[1:-1]).upper() # extract only the values between {...}

    tags=json.loads(list_1, object_pairs_hook=collections.OrderedDict) # transform str to json ordered OrderedDict

    list_header = []
    for key,value in tags.items(): # pass all values of tags to a list 
        list_header.append(str(key)+':'+str(value))
    size_modifier_list(list_header) # to modify the size and adjust to maximun_size
    nombre =str(stmt.tokens[4]) # obtain the name of table
    creator_csv('data/'+nombre+'.csv', list_header) # create the file with a list and pathfile

# to fill a .csv fill with values of table from .txt
def fill_file(stmt):
    name_table = str(stmt.tokens[4])            
    filename = "data/"+name_table+string_queue

    import os.path

    input_file = open(filename,"r+")
    reader_file = csv.reader(input_file)
    value = len(list(reader_file))
    # print value

    if value!=1:
    # if os.path.isfile(filename): # check if a file *_QUEUE.csv exist
        pathfile = filename
        # print_csv_tabulate(pathfile)

        rdr = csv.reader(open(filename))
        line1 = rdr.next() # read only the 1st row
        row_to_delete = 0

        list_1 = str(stmt.tokens[8]) # extract the block 8 (its contains name_column and type of name_column)
        list_1 = (list_1[1:-1]).upper() # extract only the values between {...}
        list_1 = '['+list_1+']'
        list_contain = ast.literal_eval(list_1) # best way to convert str to list
        # print list_contain


        for lin in rdr:
            row_to_fill = int(lin[0]) # the number of row
            row_to_delete+=1


            csv_ = chilkat.CkCsv()
            csv_.put_HasColumnNames(True) # loading the csv file, indicate that the 1st row is the column of NAMES
            success = csv_.LoadFile('data/'+name_table+'.csv') # load the csv file

            intVal = csv_.get_NumColumns();

            for i in range(intVal):
                sub_string = str(list_contain[i])
                largo = len(sub_string)
                sub_string_f = sub_string+' '*(max_size-largo)
                success = csv_.SetCell(row_to_fill, i,sub_string_f) # change the row=0, column=3 to "baguette" 

            csvDoc = csv_.saveToString() # write the updated CSV to a string    # print csvDoc
            success = csv_.SaveFile('data/'+name_table+'.csv') # save the CSV to a file
                

            # for delete the index in *_QUEUE.csv
            csv_ = chilkat.CkCsv()
            csv_.put_HasColumnNames(True) # loading the csv file, indicate that the 1st row is the column of NAMES
            success = csv_.LoadFile(filename) # load the csv file

            success = csv_.DeleteRow(row_to_delete-1);
            csvDoc = csv_.saveToString() # write the updated CSV to a string    
            # print csvDoc
            success = csv_.SaveFile(filename) # save the CSV to a file
            break # for don't overwrite more rows in .csv
           


    else:   # the file doesnt exist, so the insertion is normal at the end of .csv
        list_1 = str(stmt.tokens[8]) # extract the block 8 (its contains name_column and type of name_column)
        list_1 = (list_1[1:-1]).upper() # extract only the values between {...}
        list_1 = '['+list_1+']'
        list_contain = ast.literal_eval(list_1) # best way to convert str to list
        size_modifier_list(list_contain)
        name_table = str(stmt.tokens[4])
        fill_csv('data/'+name_table+'.csv',list_contain)            

    df1=pd.read_csv('data/'+name_table+'.csv')    # print(df1)
    print tabulate(df1, headers='keys', tablefmt='psql')

def print_csv_tabulate(pathfile):
    df1=pd.read_csv(pathfile)    # print(df1)
    print tabulate(df1, headers='keys', tablefmt='psql')

def update_csv (stmt):
    name_table = str(stmt.tokens[2]) # to obtaine NAME of table

    campo = str(stmt.tokens[6])
    indice_nombre_campo_inicio = campo.index('(')
    indice_nombre_campo_final  = campo.index('=')
    field_name = campo[indice_nombre_campo_inicio+1:indice_nombre_campo_final].upper() # to obtain NAME of COLUMN

    indice_valor_campo_final  = campo.index(")")
    field_value  = campo[indice_nombre_campo_final+1:indice_valor_campo_final].upper() 

    condicion = str(stmt.tokens[8])
    indice_condicion_campo_inicio = condicion.index('(')
    indice_condicion_campo_final  = condicion.index('=')
    field_condicion = condicion[indice_condicion_campo_inicio+1:indice_condicion_campo_final].upper()

    indice_condicion_valor_campo_final= condicion.index(")")
    condicion_value = condicion[indice_condicion_campo_final+1:indice_condicion_valor_campo_final].upper()

    # pathfile = 'data/'+name_table+'.csv'
    # print_csv_tabulate(pathfile)

    rdr = csv.reader(open('data/'+name_table+'.csv'))
    line1 = rdr.next() # read only the 1st row
            
    field_condicion = field_condicion[1:-1]   # to delete " " of the field_name
    field_header = ''
    column_csv = 0     
    column_bool = 0

    field_name = field_name[1:-1]   # to delete " " of the field_name
    column_to_modify = 0

    for i in range(len(line1)): # to search only the FIELD of Where Condition
        if field_condicion in line1[i]:
            column_csv = i
            column_bool = 1
            field_header=line1[i]
        if field_name in line1[i]:
            column_to_modify = i
                    
    df = pd.read_csv('data/'+name_table+'.csv') # to open .csv with Pandas
    saved_column = df[field_header] # to only obtain the COLUMN necesary

    condicion_value = condicion_value[1:-1]
    lenght_condicion_value = len(condicion_value)
    condicion_value = condicion_value+' '*(max_size-lenght_condicion_value)
                 
    iterador = 0
    row_csv = 0
    row_bool = 0

    for line in saved_column:
        s = str(line)
        s_bool = s.isdigit()
        if s_bool == True:
                largo_s = len(s)
                s = s+' '*(max_size-largo_s)
                if condicion_value in s:
                    row_csv = iterador
                    row_bool = 1
        elif s_bool == False:
            if condicion_value in str(line):
                row_csv = iterador
                row_bool = 1
        iterador+=1

    # to assurance the existence of register of condition 
    if column_bool == 1 and row_bool == 1: 

        field_value = field_value[1:-1]  # to delete " " of the field_value
        lenght_ = len(field_value)
        field_value = field_value+' '*(max_size-lenght_) # to format the field_value

        csv_ = chilkat.CkCsv()
        csv_.put_HasColumnNames(True) # loading the csv file, indicate that the 1st row is the column of NAMES
        success = csv_.LoadFile('data/'+name_table+'.csv') # load the csv file

        success = csv_.SetCell(row_csv,column_to_modify,field_value) # change the row=0, column=3 to "baguette" 

        csvDoc = csv_.saveToString() # write the updated CSV to a string    #print csvDoc
        success = csv_.SaveFile('data/'+name_table+'.csv') # save the CSV to a file

        pathfile = 'data/'+name_table+'.csv'
        print_csv_tabulate(pathfile)

def select_from_csv(stmt):
    field_table =  str(stmt.tokens[2]) # to prove if it has '*' or have fields
    name_table = str(stmt.tokens[6])   # obtain the NAME of TABLE
    condicion_completa = str(stmt.tokens[8]) # obtain the condition

    indice_condicion_campo_inicio = condicion_completa.index('(')
    indice_condicion_campo_final  = condicion_completa.index('=')
    field_condicion = condicion_completa[indice_condicion_campo_inicio+1:indice_condicion_campo_final].upper()
    field_condicion = field_condicion[1:-1]
                
    indice_condicion_valor_campo_final= condicion_completa.index(")")
    condicion_value = condicion_completa[indice_condicion_campo_final+1:indice_condicion_valor_campo_final].upper()
    condicion_value = condicion_value[1:-1]

    if field_table == '*' :         
        rdr = csv.reader(open('data/'+name_table+'.csv'))
        line1 = rdr.next() # read only the 1st row
                        
        col_number_csv = 0
        bool_col_number = 0
        for i in range(len(line1)): # to search only the FIELD of Where Condition
            if field_condicion in str(line1[i]):
                col_number_csv = i
                bool_col_number = 1

        if bool_col_number == 1: # to probe if the FIELD exist in CSV
            length_condicion_value = len(condicion_value)
            condicion_value = condicion_value+' '*(max_size-length_condicion_value)
                    
            # filepath = 'data/'+name_table+'.csv'
            # print_csv_tabulate(filepath)
            print '\n'
            print stmt
            print '\n'
            for line1 in rdr:

                if condicion_value in str(line1[col_number_csv]): # print only if the condicion is csv
                    print line1
                    # print line1
                    break # comment this section if you want to search all the 
    else:
        field_to_print = str(stmt.tokens[2])
        field_to_print = field_to_print[1:-1].upper()

        rdr = csv.reader(open('data/'+name_table+'.csv'))
        line1 = rdr.next() # read only the 1st row
                        
        col_number_csv = 0
        bool_col_number = 0
        col_to_print = 0

        for i in range(len(line1)): # to search only the FIELD of Where Condition
            if field_condicion in str(line1[i]):
                col_number_csv = i
                bool_col_number = 1
            elif field_to_print in str(line1[i]):
                col_to_print = i

        if bool_col_number == 1: # to probe if the FIELD exist in CSV
            length_condicion_value = len(condicion_value)
            condicion_value = condicion_value+' '*(max_size-length_condicion_value)
                    
            # filepath = 'data/'+name_table+'.csv'
            # print_csv_tabulate(filepath)
            print '\n'.rstrip()
            print stmt
            print '\n'.rstrip()
            for line1 in rdr:
                if condicion_value in str(line1[col_number_csv]): # print only if the condicion is csv
                    print '|'+line1[0]+'|'+line1[col_to_print]+'|'

def delete_row_csv(stmt):
    name_table =  str(stmt.tokens[4])
            
    condicion_completa = str(stmt.tokens[6]) # obtain the condition
    indice_condicion_campo_inicio = condicion_completa.index('(')
    indice_condicion_campo_final  = condicion_completa.index('=')
    field_condicion = condicion_completa[indice_condicion_campo_inicio+1:indice_condicion_campo_final].upper()
    field_condicion = field_condicion[1:-1]

    indice_condicion_valor_campo_final= condicion_completa.index(")")
    condicion_value = condicion_completa[indice_condicion_campo_final+1:indice_condicion_valor_campo_final].upper()
    condicion_value = condicion_value[1:-1]


    pathfile = 'data/'+name_table+'.csv'
    print_csv_tabulate(pathfile)
    print '\n'.rstrip()
    print stmt
    print '\n'.rstrip()
            
    rdr = csv.reader(open('data/'+name_table+'.csv'))
    line1 = rdr.next() # read only the 1st row
                    
    field_condicion = field_condicion[1:-1]   # to delete " " of the field_name
    field_header = ''
    column_csv = 0     
    column_bool = 0

    for i in range(len(line1)): # to search only the FIELD of Where Condition
        if field_condicion in line1[i]:
            column_csv = i
            column_bool = 1
            field_header=line1[i]

    if column_bool==1: # if the column exist in TABLE
                
        df = pd.read_csv('data/'+name_table+'.csv') # to open .csv with Pandas
        saved_column = df[field_header] # to only obtain the COLUMN necesary

        condicion_value = condicion_value
        lenght_condicion_value = len(condicion_value)
        condicion_value = condicion_value+' '*(max_size-lenght_condicion_value)

        iterador = 0
        row_csv = 0
        row_bool = 0

        for line in saved_column:
            s = str(line)
            s_bool = s.isdigit()
            if s_bool == True:
                largo_s = len(s)
                s = s+' '*(max_size-largo_s)
                if condicion_value in s:
                    row_csv = iterador
                    row_bool = 1
            elif s_bool == False:
                if condicion_value in str(line):
                    row_csv = iterador
                    row_bool = 1
            iterador+=1

        if row_bool == 1:
                    
            csv_ = chilkat.CkCsv()
            csv_.put_HasColumnNames(True) # loading the csv file, indicate that the 1st row is the column of NAMES
            success = csv_.LoadFile('data/'+name_table+'.csv') # load the csv file

            intVal = csv_.get_NumColumns();
            substring_empty = " "*(max_size)

            for i in range(intVal):
                success = csv_.SetCell(row_csv, i,substring_empty) # change the row=0, column=3 to "baguette" 

                    # # success = csv_.DeleteRow(2);
            csvDoc = csv_.saveToString() # write the updated CSV to a string    # print csvDoc
            success = csv_.SaveFile('data/'+name_table+'.csv') # save the CSV to a file
                
            print_csv_tabulate(pathfile)

            # to save in *_QUEUE.csv , save the row number
            header_pos = str(row_csv).split()
            path_to = 'data/'+name_table+string_queue
            fill_csv(path_to,header_pos)

def main():
    
    start_time = time.time()
    filename = 'sql.txt'    # to open .txt with sql sentences
    with open(filename) as f:
        data = f.readlines()

    for n, sql in enumerate(data, 1): # read the entire text of sql sentences
        sql = sql.rstrip() # delete spaces
        parsed = sqlparse.parse(sql) # parser .txt to sql keywords (CREATE, DELETE, etc)
        stmt = parsed[0] 

        if str(stmt.tokens[0])   == "CREATE":
            create_file(stmt)
        
        elif str(stmt.tokens[0]) == "INSERT":      
            fill_file(stmt)
                


            

        elif str(stmt.tokens[0]) == "UPDATE":
            update_csv(stmt)

        elif str(stmt.tokens[0]) == "SELECT":
            select_from_csv(stmt)

        elif str(stmt.tokens[0]) == "DELETE":
            delete_row_csv(stmt)

        # UPDATE and DELETE     IS INCOMPLETE
        # THE CHANGE and DELETE     BY BLOCK IS NOT IMPLEMENTED

    print("--- %s seconds ---" % (time.time() - start_time))
if __name__ == "__main__":
    main()
