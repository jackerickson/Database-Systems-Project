import mysql.connector
from mysql.connector import Error
import datetime
import sys

dbconfig = {
    "host": "localhost",
    "database": "DB_FS",
    "user":     "root",
    "password":   "admin"
}


def main():

    if len(sys.argv) > 1 and sys.argv[1] =="-l":
        optionL = True
    else:
        optionL = False
    try:
        connection = mysql.connector.connect(**dbconfig)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print("You're connected to database: ", record)

        cursor.execute("Select * from Locations where parentinode is null")
        # cursor.execute("Select * from Locations where inodeSN = 411846")

        curr_dir = cursor.fetchone()

        ls(curr_dir, cursor, optionL)


    except Error as e:
            print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")



def print_optionL_info(rows):
    for row in rows:
        #on each of the rows, grab specific info from its metadata
        name = row[2]
        mode = oct(row[3])
        size = row[5]
        readable_time = datetime.datetime.fromtimestamp(row[6]).isoformat()
        
        print(f"{mode} {size} {readable_time} {name}")
    


# change this to take current Inode. use that to get the parentInode
def ls(directory, cursor, optionL = False):
    
    # get all the files in the directory supplied
    query = f"SELECT * FROM Locations natural join Metadata where parentinode = {directory[0]}"
    cursor.execute(query)

    rows = cursor.fetchall()

    
    print(f"total {len(rows)}")

    # if -l get more in depth info
    if optionL:
        print_optionL_info(rows)
    # print the files
    else: 
        for row in rows:     
            print(f"{row[2]}", end= ' ')
        print()

    return
if __name__ == "__main__":
    main()
