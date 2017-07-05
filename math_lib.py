import mysql.connector
from mysql.connector import errorcode
import time


def summ(data):
    return "{0}+{1}={2}".format(int (data[1]),int (data[2]),int (data[1])+ int (data[2]))

def sum_all(data):
    ret_list = list()
    for i in data:
        ret_list.append(summ(i))
    return ret_list

def test(data):
    print "got data {0}".format(data)
    return data

math_dict = {
        "sum": summ,
        "sum_all": sum_all,
        "test" : test
    }



#if __name__ == '__main__':
 #   import  argparse
 #   parser = argparse.ArgumentParser(description='HTTP Server')
  #  parser.add_argument('id', type=int, help='database id')
   # args = parser.parse_args()
    #insertData(name = args.id)


#print selectByID(args.id)