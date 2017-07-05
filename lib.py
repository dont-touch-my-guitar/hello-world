import mysql.connector
from mysql.connector import errorcode
import time

query_dict = {
    "select_all" : "SELECT  * FROM new_schema.test_table",
    "select_by_id" : "SELECT * FROM new_schema.test_table WHERE id = {0}",
    "insert_data" : 'INSERT INTO `new_schema`.`test_table`(`data`) VALUES ("{0}")'
}

def commonSelect (query):
    #print 0
    returnvalue = None
    try:
        cnx = mysql.connector.connect(user='root', password='toor',
                                      host='127.0.0.1',
                                      database='new_schema')
        cursor = cnx.cursor()

        cursor.execute(query)

        returnvalue = list()
        for line in cursor:
            returnvalue.append(line)

        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return returnvalue

def selectAll():
    return commonSelect(query_dict["select_all"])

def selectByID(id):
    return commonSelect(query_dict["select_by_id"].format(id))

def insertData(name):
    try:
        cnx = mysql.connector.connect(user='root', password='toor',
                                      host='127.0.0.1',
                                      database='new_schema')
        cursor = cnx.cursor()

        #name = "{0}".format(time.time())

        #query = 'INSERT INTO `new_schema`.`test_table`(`data`) VALUES ("{0}")'.format(name)
        #s = query_dict["insert_data"]


        cursor.execute(query_dict["insert_data"].format(name))

        cnx.commit()
        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()



if __name__ == '__main__':
    import  argparse
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('id', type=int, help='database id')
    args = parser.parse_args()
    insertData(name = args.id)


#print selectByID(args.id)