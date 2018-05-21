#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import mysql.connector
from mysql.connector import errorcode
import logging

local_config = {
  'user': 'root',
  'password': 'lee'
}

remote_config = {
  'user': 'root',
  'password': 'Max123',
  'host': 'czds68.yicp.io',
  'port':'4406',
  'database': 'amazon'
}

mac_config = {
  'user': 'root',
  'password': 'lee',
  'host': '192.168.0.3',
  'port':'3306',
  'database': 'amazon'
}

config = remote_config

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
    " `lastbuy` DATETIME,"
    " `in_use` CHAR(1),"
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

TABLES['productinfo'] = (
    "CREATE TABLE `productinfo` ("
    "`productid` INT UNSIGNED AUTO_INCREMENT,"
    "`asin` VARCHAR(50), "
    "`department` VARCHAR(50),"
    "`busybox_price` FLOAT ,"
    "`order_price` FLOAT,"
    "`keyword` VARCHAR(100),"
    "`brand` VARCHAR(50),"
    "PRIMARY KEY (`productid`)"
    ") ENGINE=InnoDB")

TABLES['ordertask'] = (
    "CREATE TABLE `ordertask` ("
    "`ordertaskid` INT UNSIGNED AUTO_INCREMENT,"
    "`username` VARCHAR(80), "
    "`asin` VARCHAR(50),"
    "`num` INT,"
    "`order_date` DATETIME,"
    "PRIMARY KEY (`ordertaskid`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
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