import mysql.connector
from mysql.connector import Error
import os
import ls
import find
import utils
from stat import *
import datetime
import execute
import grep


dbconfig = {
    "host": "localhost",
    "database": "DB_FS",
    "user":     "root",
    "password":   "admin"
}



try: 
    connection = mysql.connector.connect(**dbconfig)
    raw_connection = mysql.connector.connect(**dbconfig, raw=True)
                                            
    if connection.is_connected() and raw_connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Connected to ", record)

    else:
        print("Unable to connect to DB, exiting.")
        exit()


   
    cursor = connection.cursor()
    raw_cursor = raw_connection.cursor()

    cursor.execute("select * from Locations where parentinode is NULL")
    curr_dir = cursor.fetchone()

    PATH=curr_dir

    ###### Input Loop
    while True:
        try:
            command = input(f"/{utils.get_file_path(curr_dir[0],cursor)}$ ").split(' ')

            ## CD
            if command[0] == "cd":

                    

                    if len(command) != 2:
                        print("Incorrect Usage")
                    elif command[1] == '..':
                        if curr_dir[2] != None:
                            cursor.execute(f'SELECT * from Locations where inodeSN = {curr_dir[1]}')
                            curr_dir = cursor.fetchone()
                        
                    else:
                        destination = command[1]
                        # Absolute Change
                        if destination[0] == '/':
                            print("Not implemented yet, please use a relative path")
                        else:
                            cursor.execute(f'SELECT * from Locations natural join Metadata where parentinode = {curr_dir[0]} and filepath = "{destination}"')
                            res = cursor.fetchone()
                            if res == None or not S_ISDIR(res[3]):
                                print("directory not found")
                            else:
                                curr_dir = res[:3]


            ## PWD
            elif command[0] == "pwd":
               
                print(f"/{utils.get_file_path(curr_dir[0],cursor)}")
                
            elif command[0] == "ls":
                
                if len(command) > 1 and command[1] == "-l":
                    if len(command) == 2:
                        ls.ls(curr_dir, cursor, True)

                    elif len(command) == 3:
                    
                        cursor.execute(f"SELECT * from Locations Natural Join Metadata where parentinode = {curr_dir[0]} and filepath = '{command[2]}'")
                        res = cursor.fetchone()
                        name = res[2]
                        mode = oct(res[3])
                        size = res[5]
                        readable_time = datetime.datetime.fromtimestamp(res[6]).isoformat()
                        print(f"{mode} {size} {readable_time} {name}")

                    else: print("Incrrect Usage")

                elif len(command) == 1:
                    ls.ls(curr_dir, cursor)
                else:
                    print("incorrect usage of ls")

            elif command[0] == "find":
                if len(command) == 2:
                    
                    find.find(curr_dir, command[1], cursor)
                
                elif len(command) == 3:
                    search_dir = utils.get_file_from_path(command[1],cursor)
                    searchKey = command[2]
                    
                    find.find(search_dir, searchKey, cursor)

                else: print("incorrect usage of find")


            elif command[0] == "grep":
                if len(command) != 3:
                    print("Incorrect usage")
                else:
                    grep.grep(curr_dir, command[1], command[2], raw_cursor, cursor)    
                

            elif command[0] == "exe":
                
                execute.execute(PATH, command[1], raw_cursor, cursor)

            elif command[0] == "setpath":
                PATH = utils.get_file_from_path(command[1], cursor)

            elif command[0] == "path":
                print(f"/{utils.get_file_path(PATH[0],cursor)}")

            elif command[0] == "exit":
                break
        except Error as e:
            print("Error while connecting to MySQL", e)


except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
    if (raw_connection.is_connected()):
        raw_cursor.close()
        raw_connection.close()
    
    print("MySQL connection is closed")


