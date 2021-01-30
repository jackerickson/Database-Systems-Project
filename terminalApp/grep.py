
# grep: accept the (partial) name of the file and seek the relevant pattern in 
# the matching file(s).Output the line number and line for the matching lines.

#for file in subdirectory
#  for data in file
#       parse the file data for the searchkey

import mysql.connector
from mysql.connector import Error
import utils
from stat import *
import datetime
import find
import utils

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


        grep([412524,None,"test_folder"], "file2", "this",raw_cursor,  cursor)


    except Error as e:
            print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")




def grep(parentDir, partial_name, searchKey, raw_cursor, cursor):

    # get all the files that match the pattern
    files = find.find_ret_files(parentDir,partial_name, cursor)

    
    for f in files:
        #grab the file contents
        raw_cursor.execute(f"Select * from Locations natural join Content where inodeSN = {int(f[0])} and sequence = 0")
        res = raw_cursor.fetchone()
        data = bytearray()
        if res != None:
            i=1
            
            while res != None:
        
                data += res[4]
                raw_cursor.execute(f"Select * from Locations natural join Content where inodeSN = {int(f[0])} and sequence = {i}")
                res = raw_cursor.fetchone()
                i += 1
        # split file contents into lines using newline symbols
        contents = str(data, 'utf-8').split('\n')

        #check each line for the searchkey
        for i in range(len(contents)):
            if searchKey in contents[i]:
                print (f"{utils.get_file_path(int(f[0]), cursor)} -> line {i+1}: {contents[i]}")

    

if __name__ == "__main__":
    main()