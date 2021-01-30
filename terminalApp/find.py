
import mysql.connector
from mysql.connector import Error
import utils
from stat import *
import datetime

def main():

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='DB_FS',
                                            user='root',
                                            password='admin')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print("You're connected to database: ", record)
        
        
        cursor.execute("Select * from Locations where parentinode is null")
        curr_dir = cursor.fetchone()


        find([412531, 412524, 'subdir'], 'fi', cursor)


    except Error as e:
            print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")



def find(parentDir, searchKey, cursor):


    # start the recursion
    res = search_dir(parentDir, searchKey, cursor)
    
    # print ls -l info for each of the resulting files
    for row in res:
        name = utils.get_file_path(row[0],cursor, parentDir[0])
        mode = oct(row[3])
        size = row[5]
        readable_time = datetime.datetime.fromtimestamp(row[6]).isoformat()
        
        print(f"{mode} {size} {readable_time} {name}")


# Alternative of find, instead of printing just return the files
def find_ret_files(parentDir, searchKey, cursor):
    
    
    res = search_dir(parentDir, searchKey, cursor)
    
        
    return res


# 
def search_dir(parentDir, searchKey, cursor):
    
  
    # get all the matching files in this directory and add it to our result
    query = f"SELECT * from Locations natural join Metadata where parentinode = {parentDir[0]} and filepath like '%{searchKey}%'"
    
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return []

    # now find the subdirectories and recurse into them, add any resutls they return to our result
    cursor.execute(f"SELECT * from Locations Natural Join Metadata where parentinode = {parentDir[0]}")
    all_files = cursor.fetchall()
    for f in all_files:
        if f[0] != parentDir[0] and S_ISDIR(f[3]):
            for item in search_dir(f[:3], searchKey, cursor):
                res.append(item)

    
     
    
    return res

if __name__ == "__main__":
    main()