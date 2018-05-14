#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'Max123',
  'host': 'czds68.yicp.io',
  'port':'4406',
  'database': 'amazon'
}

DB_NAME = 'amazon'

TABLES = {}
TABLES['accountinfo'] = (
    "CREATE TABLE `accountinfo` ("
    " `userid` INT UNSIGNED AUTO_INCREMENT, "
    " `username` VARCHAR(80),"
    " `password` VARCHAR(30)," 
    " `cookies` VARCHAR(50)," 
    " `createdate` DATETIME,"
    " `logindate` DATETIME," 
    " `alive` CHAR(1)," 
    " `MAC` VARCHAR(20),"
    " PRIMARY KEY (`userid`)"
    ") ENGINE=InnoDB")


TABLES['shipaddress'] = (
    "CREATE TABLE `shipaddress` ("
    "`addrid` INT UNSIGNED AUTO_INCREMENT," 
    "`username` VARCHAR(80),"
    "`fullname` VARCHAR(40), "
    "`address` VARCHAR(100),"
    "`postalcode` VARCHAR(20),"
    "`city` VARCHAR(50),"
    "`state` VARCHAR(20),"
    "`phonenumber` VARCHAR(15),"
    "PRIMARY KEY (`addrid`)"
    ") ENGINE=InnoDB")

TABLES['finance'] = (
    "CREATE TABLE `finance` ("
    "`cardid` INT UNSIGNED AUTO_INCREMENT,"
    "`username` VARCHAR(80), "
    "`nameoncard` VARCHAR(40)," 
    "`ccnumber` CHAR(16),"
    "`ccmonth` CHAR(2),"
    "`ccyear` CHAR(4),"
    "`checkaccount` VARCHAR(50),"
    "`fullname` VARCHAR(40),"
    "`address` VARCHAR(100),"
    "`postalcode` VARCHAR(20),"
    "`city` VARCHAR(50),"
    "`state` VARCHAR(20),"
    "`phonenumber` VARCHAR(15),"
    "PRIMARY KEY (`cardid`)"
    ") ENGINE=InnoDB")


TABLES['accountquota'] = (
    "CREATE TABLE `accountquota` ("
    "`accountid` INT UNSIGNED AUTO_INCREMENT," 
    "`checkaccount` VARCHAR(50), "
    "`wquota` INT UNSIGNED,"
    "`mquota` INT UNSIGNED,"
    "`yquota` INT UNSIGNED,"
    "PRIMARY KEY (`accountid`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name))
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()