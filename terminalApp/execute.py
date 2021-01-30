import mysql.connector
from mysql.connector import Error
import utils
from stat import *
import datetime
import find
import utils
import subprocess
import os

dbconfig = {
    "host": "localhost",
    "database": "DB_FS",
    "user":     "root",
    "password":   "admin"
}


def main():

    try:
        connection = mysql.connector.connect(**dbconfig,
                                            raw = False)
        connection2 = mysql.connector.connect(**dbconfig,
                                            raw = True)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            raw_cursor = connection2.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print("You're connected to database: ", record)
        
        
        cursor.execute("Select * from Locations where parentinode is null")
        curr_dir = cursor.fetchone()


        #execute(curr_dir, "executable",raw_cursor,  cursor)
        execute([412531, 412524, 'subdir'], "sub_executable",raw_cursor,  cursor)


    except Error as e:
            print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")


def execute(pathdir, target, raw_cursor, cursor):
    #retrieve the data from the selected file
    raw_cursor.execute(f"SELECT data from Locations Natural Join Content where parentinode = {pathdir[0]} and filepath='{target}' order by sequence asc")

    res = raw_cursor.fetchone()
    #make sure we got a result
    if res == None:
        print("Could not find the file specified")
        return

    data = bytearray()
    data += res[0]

    #while there are still results, add them to the data bytearray
    if res != None:
        
        while res != None:
    
            data += res[0]
            res = raw_cursor.fetchone()

    # run it on through the console by creating a temporary file and running it
    with open('tempfile', 'wb') as f:
        f.write(data)
    
    print(str(subprocess.check_output('./tempfile'), 'utf-8'))

    #cleanup
    os.remove("tempfile")
    

if __name__ == "__main__":
    main()