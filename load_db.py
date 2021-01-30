import mysql.connector
from mysql.connector import Error
import os
from stat import *

Data_query = """
                INSERT INTO Content VALUES (%s,%s,%s)
                """
Locations_query = """
                INSERT INTO Locations VALUES (%s, %s, %s)
                    """
Metadata_query = """
                INSERT INTO Metadata VALUES (%s,%s,%s,%s,%s,%s,%s)
                """


def write_to_locations(args, connection):
    cursor = connection.cursor()
    try:
        result = cursor.execute(Locations_query, args)
        connection.commit()
    except Error as e:
        print(e)

def write_to_meta_data(args, connection):
    cursor = connection.cursor()
    try:
        result = cursor.execute(Metadata_query, args)
        connection.commit()
    except Error as e:
        print(e)

def write_to_data(args, connection):
    cursor = connection.cursor()
    try:
        result = cursor.execute(Data_query, args)
        connection.commit()
    except Error as e:
        print(e)





try:
    connection = mysql.connector.connect(host='localhost',
                                         database='DB_FS',
                                         user='root',
                                         password='admin')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

       
        
    base_dir = os.path.expanduser("/")

    bs = os.stat(base_dir) #base states


    for dirpath, dirs, files in os.walk(base_dir):
        print(dirpath)

        #directory stats
        ds = os.stat(dirpath)
        write_to_meta_data(
            (ds.st_ino, ds.st_mode,ds.st_dev, ds.st_size, ds.st_ctime, ds.st_mtime, ds.st_atime)
                ,connection
                )
        if dirpath == base_dir:
            write_to_locations(
                (ds.st_ino, None, dirpath.split('/')[-1]),connection  
                )
        else:
            dir_parent_ino = os.stat('/'.join(dirpath.split('/')[:-1])).st_ino
            write_to_locations(
                (ds.st_ino, dir_parent_ino, dirpath.split('/')[-1]), connection
                )
        parent_inode = ds.st_ino

        for f in files: 
            full_path = dirpath + '/' + f
            ft = os.stat(full_path)
            
            write_to_locations(
                (ft.st_ino,parent_inode,f),connection)
            write_to_meta_data(
                (ft.st_ino, ft.st_mode, ft.st_dev, ft.st_size, ft.st_ctime, ft.st_mtime, ft.st_atime)
                ,connection)

            
            i = 0
            file_in = open(full_path, 'rb')
            while True: 
                data = file_in.read(65000)
                if not data:
                    break
                write_to_data(
                    (ft.st_ino, i, data)
                    ,connection)
                    #(ft.st_ino, i, open(full_path,'rb').read()),connection)
                
                i += 1

        
    connection.commit()

    print("Finished with success")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")