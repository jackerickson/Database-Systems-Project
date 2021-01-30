import mysql.connector
from mysql.connector import Error


def get_file_path(inode, cursor, top_inode = None):

    cursor.execute(f"Select parentinode, filepath from Locations where inodeSN = {inode}")
  
    res = cursor.fetchone()
    file_path = res[1]
    curr_parent_inode = res[0]
    while curr_parent_inode != top_inode:
        cursor.execute(f"Select parentinode, filepath from Locations where inodeSN = {curr_parent_inode}")
        f = cursor.fetchone()
        file_path = f[1] + '/' + file_path
        curr_parent_inode = f[0]


    return file_path


def get_file_from_path(path, cursor):
    path = path.split('/')
    cursor.execute("Select * from Locations where parentinode is null")
    res = cursor.fetchone()
    for dir in path[1:]:
        cursor.execute(f"Select * from Locations where parentinode = {res[0]} and filepath = '{dir}'")
        res = cursor.fetchone()

    return res

if __name__ == "__main__":

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
        
        
    

        # deep
        # get_file_path(412537, cursor, None)

        #root
        get_file_path(412524, cursor, None)


    except Error as e:
            print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")