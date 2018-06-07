from datetime import date, datetime, timedelta
import mysql.connector
from mysql.connector import errorcode
import logging
from enum import IntEnum


remote_config = {
    'user': 'root',
    'password': 'Max123',
    'host': 'czds68.yicp.io',
    'port': '4406',
    'database': 'amazon'
}

local_config = {
    'user': 'root',
    'password': 'Max123',
    'host': 'czds68.yicp.io',
    'port': '4406',
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


class DB(IntEnum):
    ACCOUNTINFO = 0
    SHIPADDRESS = 1
    FINANCE = 2
    ACCOUNTQUOTA = 3
    PRODUCTINFO = 4
    ORDERTASK = 5


class amazon_db(object):
    db_names = ['accountinfo', 'shipaddress', 'finance', 'accountquota', 'productinfo', 'ordertask']

    accountinfo_fields = ['userid', 'username', 'password', 'cookies', 'createdate', 'logindate', 'lastbuy', 'in_use', 'alive', 'MAC']
    shipaddress_fields = ['addrid', 'username', 'fullname', 'address', 'postalcode', 'city', 'state', 'phonenumber']
    finance_fields = ['cardid', 'username', 'nameoncard', 'ccnumber', 'ccmonth', 'ccyear', 'checkaccount', 'fullname', 'address', 'postalcode', 'city', 'state', 'phonenumber']
    accountquota_fields = ['accountid', 'checkaccount', 'wquota', 'mquota', 'yquota']
    productinfo_fields = ['productid', 'asin', 'department', 'busybox_price', 'order_price', 'keyword', 'brand']
    order_task_fields = ['ordertaskid', 'username', 'asin', 'num', 'order_date']

    # args in tuple form
    sql_add_accountinfo_tuple = ("INSERT INTO accountinfo"
                          "(username, password, cookies, createdate, logindate, lastbuy, in_use, alive, MAC)"
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
    sql_update_accountinfo_pw_tuple = ("UPDATE accountinfo SET password=%s WHERE username=%s;")
    sql_update_accountinfo_cookie_tuple = ("UPDATE accountinfo SET cookies=%s WHERE username=%s;")
    sql_update_accountinfo_createdate_tuple = ("UPDATE accountinfo SET createdate=%s WHERE username=%s;")
    sql_update_accountinfo_logindate_tuple = ("UPDATE accountinfo SET logindate=%s WHERE username=%s;")
    sql_update_accountinfo_lastbuy_tuple = ("UPDATE accountinfo SET lastbuy=%s WHERE username=%s;")
    sql_update_accountinfo_in_use_tuple = ("UPDATE accountinfo SET in_use=%s WHERE username=%s;")
    sql_update_accountinfo_alive_tuple = ("UPDATE accountinfo SET alive=%s WHERE username=%s;")
    sql_update_accountinfo_MAC_tuple = ("UPDATE accountinfo SET MAC=%s WHERE username=%s;")

    # args in dict form
    sql_add_accountinfo_dict = ("INSERT INTO accountinfo"
                         "(username, password, cookies, createdate, logindate, lastbuy, alive, MAC)"
                         "VALUES (%(username)s, %(passwd)s, %(cookies)s, %(createdate)s, %(logindate)s, %(lastbuy)s, %(alive)s, %(MAC)s);")
    sql_update_accountinfo_pw_dict = ("UPDATE accountinfo SET password=%(passwd)s WHERE username=%(username)s;")
    sql_update_accountinfo_cookies_dict = ("UPDATE accountinfo SET cookies=%(cookies)s WHERE username=%(username)s;")
    sql_update_accountinfo_createdate_dict = ("UPDATE accountinfo SET createdate=%(createdate)s WHERE username=%(username)s;")
    sql_update_accountinfo_logindate_dict = ("UPDATE accountinfo SET logindate=%(logindate)s WHERE username=%(username)s;")
    sql_update_accountinfo_lastbuy_dict = ("UPDATE accountinfo SET lastbuy=%(lastbuy)s WHERE username=%(username)s;")
    sql_update_accountinfo_in_use_dict = ("UPDATE accountinfo SET in_use=%(in_use)s WHERE username=%(username)s;")
    sql_update_accountinfo_alive_dict = ("UPDATE accountinfo SET alive=%(alive)s WHERE username=%(username)s;")
    sql_update_accountinfo_MAC_dict = ("UPDATE accountinfo SET MAC=%(MAC)s WHERE username=%(username)s;")

    sql_get_accountinfo_all = ("SELECT * FROM accountinfo;")
    sql_get_accountinfo_by_lastbuy_tuple = ("SELECT * FROM accountinfo WHERE lastbuy < %s AND in_use=0;")
    sql_get_accountinfo_by_lastbuy_dict = ("SELECT * FROM accountinfo WHERE lastbuy < %(lastbuy)s AND in_use=0;")

    # args in tuple form
    sql_add_shipaddr_tuple = ("INSERT INTO shipaddress "
                              "(username, fullname, address, postalcode, city, state, phonenumber)"
                              "VALUES (%s,%s,%s,%s,%s,%s,%s)")
    sql_update_shipaddress_fullname_tuple = ("UPDATE shipaddress SET fullname=%s WHERE username=%s;")
    sql_update_shipaddress_address_tuple = ("UPDATE shipaddress SET address=%s WHERE username=%s;")
    sql_update_shipaddress_postalcode_tuple = ("UPDATE shipaddress SET postalcode=%s WHERE username=%s;")
    sql_update_shipaddress_city_tuple = ("UPDATE shipaddress SET city=%s WHERE username=%s;")
    sql_update_shipaddress_state_tuple = ("UPDATE shipaddress SET state=%s WHERE username=%s;")
    sql_update_shipaddress_phonenumber_tuple = ("UPDATE shipaddress SET phonenumber=%s WHERE username=%s;")

    # args in dict form
    sql_add_shipaddr_dict = ("INSERT INTO shipaddress "
                             "(username, fullname, address, postalcode, city, state, phonenumber)"
                             "VALUES (%(username)s,%(fullname)s,%(address)s,%(postalcode)s,%(city)s,%(state)s,%(phonenumber)s)")
    sql_update_shipaddress_fullname_dict = ("UPDATE shipaddress SET fullname=%(fullname)s WHERE username=%(username)s;")
    sql_update_shipaddress_address_dict = ("UPDATE shipaddress SET address=%(address)s WHERE username=%(username)s;")
    sql_update_shipaddress_postalcode_dict = ("UPDATE shipaddress SET postalcode=%(postalcode)s WHERE username=%(username)s;")
    sql_update_shipaddress_city_dict = ("UPDATE shipaddress SET city=%(city)s WHERE username=%(username)s;")
    sql_update_shipaddress_state_dict = ("UPDATE shipaddress SET state=%(state)s WHERE username=%(username)s;")
    sql_update_shipaddress_phonenumber_dict = ("UPDATE shipaddress SET phonenumber=%(phonenumber)s WHERE username=%(username)s;")
    sql_get_shipaddress_all = ("SELECT * FROM shipaddress;")
    sql_get_shipaddress_by_username_tuple = ("SELECT * FROM shipaddress WHERE username=%s;")
    sql_get_shipaddress_by_username_dict = ("SELECT * FROM shipaddress WHERE username=%(username)s;")

    # args in tuple form
    sql_add_finance_tuple = ("INSERT INTO finance "
                             "(username,nameoncard,ccnumber,ccmonth,ccyear,checkaccount,fullname,address, postalcode,city,state,phonenumber) "
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    sql_update_finance_nameoncard_tuple = ("UPDATE finance SET nameoncard=%s WHERE username=%s;")
    sql_update_finance_ccnumber_tuple = ("UPDATE finance SET ccnumber=%s WHERE username=%s;")
    sql_update_finance_ccmonth_tuple = ("UPDATE finance SET ccmonth=%s WHERE username=%s;")
    sql_update_finance_fullname_tuple = ("UPDATE finance SET fullname=%s WHERE username=%s;")
    sql_update_finance_address_tuple = ("UPDATE finance SET address=%s WHERE username=%s;")
    sql_update_finance_ccyear_tuple = ("UPDATE finance SET ccyear=%s WHERE username=%s;")
    sql_update_finance_postalcode_tuple = ("UPDATE finance SET postalcode=%s WHERE username=%s;")
    sql_update_finance_city_tuple = ("UPDATE finance SET city=%s WHERE username=%s;")
    sql_update_finance_state_tuple = ("UPDATE finance SET state=%s WHERE username=%s;")
    sql_update_finance_phonenumber_tuple = ("UPDATE finance SET phonenumber=%s WHERE username=%s;")
    sql_update_finance_checkaccount_tuple = ("UPDATE finance SET checkaccount=%s WHERE username=%s;")

    # args in dict form
    sql_add_finance_dict = ("INSERT INTO finance "
                            "(username,nameoncard,ccnumber,ccmonth,ccyear,checkaccount,fullname,address, postalcode,city,state,phonenumber) "
                            "VALUES (%(username)s,%(nameoncard)s,%(ccnumber)s,%(ccmonth)s,%(ccyear)s,%(checkaccount)s,%(fullname)s,%(address)s,%(postalcode)s,%(city)s,%(state)s,%(phonenumber)s)")
    sql_update_finance_nameoncard_dict = ("UPDATE finance SET nameoncard=%(nameoncard)s WHERE username=%(username)s;")
    sql_update_finance_ccnumber_dict = ("UPDATE finance SET ccnumber=%(ccnumber)s WHERE username=%(username)s;")
    sql_update_finance_ccmonth_dict = ("UPDATE finance SET ccmonth=%(ccmonth)s WHERE username=%(username)s;")
    sql_update_finance_fullname_dict = ("UPDATE finance SET fullname=%(fullname)s WHERE username=%(username)s;")
    sql_update_finance_address_dict = ("UPDATE finance SET address=%(address)s WHERE username=%(username)s;")
    sql_update_finance_ccyear_dict = ("UPDATE finance SET ccyear=%(ccyear)s WHERE username=%(username)s;")
    sql_update_finance_postalcode_dict = ("UPDATE finance SET postalcode=%(postalcode)s WHERE username=%(username)s;")
    sql_update_finance_city_dict = ("UPDATE finance SET city=%(city)s WHERE username=%(username)s;")
    sql_update_finance_state_dict = ("UPDATE finance SET state=%(state)s WHERE username=%(username)s;")
    sql_update_finance_phonenumber_dict = ("UPDATE finance SET phonenumber=%(phonenumber)s WHERE username=%(username)s;")
    sql_update_finance_checkaccount_dict = ("UPDATE finance SET checkaccount=%(checkaccount)s WHERE username=%(username)s;")

    sql_get_finance_all = ("SELECT * FROM finance;")
    sql_get_finance_by_username_tuple = ("SELECT * FROM finance WHERE username=%s;")
    sql_get_finance_by_username_dict = ("SELECT * FROM finance WHERE username=%(username)s;")

    # args in tuple form
    sql_add_quota_tuple = ("INSERT INTO accountquota"
                           "(checkaccount,wquota,mquota,yquota)"
                           "VALUES (%s,%s,%s,%s)")
    sql_update_accountquota_wquota_tuple = ("UPDATE accountquota SET wquota=%s WHERE checkaccount=%s;")
    sql_update_accountquota_mquota_tuple = ("UPDATE accountquota SET mquota=%s WHERE checkaccount=%s;")
    sql_update_accountquota_yquota_tuple = ("UPDATE accountquota SET yquota=%s WHERE checkaccount=%s;")

    # args in dict form
    sql_add_quota_dict = ("INSERT INTO accountquota"
                          "(checkaccount,wquota,mquota,yquota)"
                          "VALUES (%(checkaccount)s,%(wquota)s,%(mquota)s,%(yquota)s)")
    sql_update_accountquota_wquota_dict = ("UPDATE accountquota SET wquota=%(wquota)s WHERE checkaccount=%(checkaccount)s;")
    sql_update_accountquota_mquota_dict = ("UPDATE accountquota SET mquota=%(mquota)s WHERE checkaccount=%(checkaccount)s;")
    sql_update_accountquota_yquota_dict = ("UPDATE accountquota SET yquota=%(yquota)s WHERE checkaccount=%(checkaccount)s;")
    sql_get_accountquota_all = ("SELECT * FROM accountquota;")
    sql_get_accountquota_by_account_tuple = ("SELECT * FROM accountquota WHERE checkaccount=%s;")
    sql_get_accountquota_by_account_dict = ("SELECT * FROM accountquota WHERE checkaccount=%(checkaccount)s;")

    # args in tuple form
    sql_add_productinfo_tuple = ("INSERT INTO productinfo"
                                 "(asin, department, busybox_price, order_price, keyword, brand)"
                                 "VALUES (%s,%s,%s,%s,%s,%s)")
    sql_update_productinfo_department_tuple = ("UPDATE productinfo SET department=%s WHERE asin=%s;")
    sql_update_productinfo_busybox_price_tuple = ("UPDATE productinfo SET busybox_price=%s WHERE asin=%s;")
    sql_update_productinfo_order_price_tuple = ("UPDATE productinfo SET order_price=%s WHERE asin=%s;")
    sql_update_productinfo_keyword_tuple = ("UPDATE productinfo SET keyword=%s WHERE asin=%s;")
    sql_update_productinfo_brand_tuple = ("UPDATE productinfo SET brand=%s WHERE asin=%s;")

    # args in dict form
    sql_add_productinfo_dict = ("INSERT INTO productinfo"
                                "(asin, department, busybox_price, order_price, keyword, brand)"
                                "VALUES (%(asin)s,%(department)s,%(busybox_price)s,%(order_price)s,%(keyword)s,%(brand)s)")
    sql_update_productinfo_department_dict = ("UPDATE productinfo SET department=%(department)s WHERE asin=%(asin)s;")
    sql_update_productinfo_busybox_price_dict = ("UPDATE productinfo SET busybox_price=%(busybox_price)s WHERE asin=%(asin)s;")
    sql_update_productinfo_order_price_dict = ("UPDATE productinfo SET order_price=%(order_price)s WHERE asin=%(asin)s;")
    sql_update_productinfo_keyword_dict = ("UPDATE productinfo SET keyword=%(keyword)s WHERE asin=%(asin)s;")
    sql_update_productinfo_brand_dict = ("UPDATE productinfo SET brand=%(brand)s WHERE asin=%(asin)s;")
    sql_get_productinfo_all = ("SELECT * FROM productinfo;")
    sql_get_productinfo_by_asin_tuple = ("SELECT * FROM productinfo WHERE asin=%s;")
    sql_get_productinfo_by_asin_dict = ("SELECT * FROM productinfo WHERE asin=%(asin)s;")

    # args in tuple form
    sql_add_ordertask_tuple = ("INSERT INTO ordertask"
                               "(username, asin, num, order_date)"
                               "VALUES (%s,%s,%s,%s)")
    sql_update_ordertask_asin_tuple = ("UPDATE ordertask SET asin=%s WHERE username=%s;")
    sql_update_ordertask_num_tuple = ("UPDATE ordertask SET num=%s WHERE username=%s;")
    sql_update_ordertask_order_date_tuple = ("UPDATE ordertask SET order_date=%s WHERE username=%s;")

    # args in dict form
    sql_add_ordertask_dict = ("INSERT INTO ordertask"
                              "(username, asin, num, order_date)"
                              "VALUES (%(username)s,%(asin)s,%(num)s, %(order_date)s)")
    sql_update_ordertask_asin_dict = ("UPDATE ordertask SET asin=%s WHERE username=%s;")
    sql_update_ordertask_num_dict = ("UPDATE ordertask SET num=%s WHERE username=%s;")
    sql_update_ordertask_order_date_dict = ("UPDATE ordertask SET order_date=%s WHERE username=%s;")
    sql_get_ordertask_all = ("SELECT * FROM ordertask;")

    def __init__(self):
        #for rd lock table
        self.sql_rd_lock = []
        self.sql_rd_lock_all = "LOCK TABLES "
        for item in list(enumerate(amazon_db.db_names)):
            #print(item)
            lock_statement = "LOCK TABLE %s READ;" % item[1]
            if item[0] == 0:
                self.sql_rd_lock_all += "%s READ" % item[1]
            else:
                self.sql_rd_lock_all += ",%s READ" % item[1]
            self.sql_rd_lock.append(lock_statement)
        self.sql_rd_lock_all += ";"


        #for wr lock table
        self.sql_wr_lock = []
        self.sql_wr_lock_all = "LOCK TABLES "
        for item in list(enumerate(amazon_db.db_names)):
            #print(item)
            lock_statement = "LOCK TABLE %s WRITE;" % item[1]
            if item[0] == 0:
                self.sql_wr_lock_all += "%s WRITE" % item[1]
            else:
                self.sql_wr_lock_all += ",%s WRITE" % item[1]
            self.sql_wr_lock.append(lock_statement)
        self.sql_wr_lock_all += ";"

        #for unlock all table
        self.sql_unlock_all = "UNLOCK TABLES;"

        self.sql_fields = {}
        self.sql_fields[amazon_db.db_names[DB.ACCOUNTINFO]] = amazon_db.accountinfo_fields
        self.sql_fields[amazon_db.db_names[DB.SHIPADDRESS]] = amazon_db.shipaddress_fields
        self.sql_fields[amazon_db.db_names[DB.FINANCE]] = amazon_db.finance_fields
        self.sql_fields[amazon_db.db_names[DB.ACCOUNTQUOTA]] = amazon_db.accountquota_fields
        self.sql_fields[amazon_db.db_names[DB.PRODUCTINFO]] = amazon_db.productinfo_fields
        self.sql_fields[amazon_db.db_names[DB.ORDERTASK]] = amazon_db.order_task_fields
        # for key, val in self.sql_fields.items():
        #    print(key, val)
        #print(self.sql_fields[amazon_db.db_names[DB.ACCOUNTINFO]])
        return
    def open(self):
        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print('connect err:', err)
        return
    def accountinfo_add_item(self, username, passwd, createdate=datetime.now(), logindate=datetime.now(), lastbuy=datetime(1997,1,1), in_use=0, alive=1, cookies=None, MAC=None):
        add_dll = {}
        add_dll['username'] = username
        add_dll['passwd'] = passwd
        add_dll['cookies'] = cookies
        add_dll['createdate'] = createdate
        add_dll['logindate'] = logindate
        add_dll['lastbuy'] = lastbuy
        add_dll['in_use'] = in_use
        add_dll['alive'] = alive
        add_dll['MAC'] = MAC
        #print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_add_accountinfo_dict, add_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def accountinfo_get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_get_shipaddr_all)
        result = self.cursor.fetchall()
        print(result)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return result

    def accountinfo_get_item_by_lastbuy(self, interval):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.ACCOUNTINFO])
        tdiff = timedelta(hours=interval)
        self.cursor.execute(amazon_db.sql_get_accountinfo_by_lastbuy_tuple, (datetime.now() + tdiff,))
        result = self.cursor.fetchall()
        # print(result)
        candidate_users = []
        for row in result:
            #print(row)
            item = dict(zip(amazon_db.accountinfo_fields, row))
            #print(item)
            candidate_users.append(item)
        print(candidate_users)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return candidate_users
    def accountinfo_update_passwd(self, username, passwd):
        update_dll = {}
        update_dll['username'] = username
        if passwd:
            update_dll['passwd'] = passwd
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_pw_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def accountinfo_update_createdate(self, username, createdate):
        update_dll = {}
        update_dll['username'] = username
        if createdate:
            update_dll['createdate'] = createdate
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_createdate_tuple, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def accountinfo_update_logindate(self, username, logindate):
        update_dll = {}
        update_dll['username'] = username
        if logindate:
            update_dll['logindate'] = logindate
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_logindate_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def accountinfo_update_lastbuy(self, username, lastbuy):
        update_dll = {}
        update_dll['username'] = username
        if lastbuy:
            update_dll['lastbuy'] = lastbuy
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_lastbuy_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def accountinfo_update_in_use(self, username, in_use):
        update_dll = {}
        update_dll['username'] = username
        if in_use:
            update_dll['in_use'] = in_use
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_in_use_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def accountinfo_update_alive(self, username, alive):
        update_dll = {}
        update_dll['username'] = username
        if alive:
            update_dll['alive'] = alive
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_alive_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def accountinfo_update_cookies(self, username, cookies):
        update_dll = {}
        update_dll['username'] = username
        if cookies:
            update_dll['cookies'] = cookies
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_cookies_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def accountinfo_update_MAC(self, username, MAC):
        update_dll = {}
        update_dll['username'] = username
        if MAC:
            update_dll['MAC'] = MAC
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTINFO])
        self.cursor.execute(amazon_db.sql_update_accountinfo_MAC_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def shipaddress_add_item(self, username, fullname, address=None, postalcode=None, city=None, state=None, phonenumber=None):
        add_dll = {}
        add_dll['username'] = username
        add_dll['fullname'] = fullname
        add_dll['address'] = address
        add_dll['postalcode'] = postalcode
        add_dll['city'] = city
        add_dll['state'] = state
        add_dll['phonenumber'] = phonenumber
        print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_add_shipaddr_dict, add_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def shipaddress_get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_get_shipaddress_all)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return result

    def shipaddress_get_item_by_username(self, username):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.SHIPADDRESS])
        query = {}
        query['username'] = username

        self.cursor.execute(amazon_db.sql_get_shipaddress_by_username_dict, query)
        result = self.cursor.fetchall()
        print(result)
        candidate_shipaddr = []
        for row in result:
            item = dict(zip(amazon_db.shipaddress_fields, row))
            candidate_shipaddr.append(item)
        # print(candidate_users)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return candidate_shipaddr

    def shipaddress_update_fullname(self, username, fullname):
        update_dll = {}
        update_dll['username'] = username
        if fullname:
            update_dll['fullname'] = fullname
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_update_shipaddress_fullname_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def shipaddress_update_address(self, username, address):
        update_dll = {}
        update_dll['username'] = username
        if address:
            update_dll['address'] = address
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_update_shipaddress_address_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def shipaddress_update_postalcode(self, username, postalcode):
        update_dll = {}
        update_dll['username'] = username
        if postalcode:
            update_dll['postalcode'] = postalcode
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_update_shipaddress_postalcode_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def shipaddress_update_city(self, username, city):
        update_dll = {}
        update_dll['username'] = username
        if city:
            update_dll['city'] = city
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_update_shipaddress_city_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def shipaddress_update_state(self, username, state):
        update_dll = {}
        update_dll['username'] = username
        if state:
            update_dll['state'] = state
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_update_shipaddress_state_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def shipaddress_update_phonenumber(self, username, phonenumber):
        update_dll = {}
        update_dll['username'] = username
        if phonenumber:
            update_dll['phonenumber'] = phonenumber
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.SHIPADDRESS])
        self.cursor.execute(amazon_db.sql_update_shipaddress_phonenumber_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()


    def finance_add_item(self, username, nameoncard, ccnumber, ccmonth, ccyear,
                 checkaccount, fullname, address, postalcode,city,state,phonenumber):
        add_dll = {}
        add_dll['username'] = username
        add_dll['nameoncard'] = nameoncard
        add_dll['ccnumber'] = ccnumber
        add_dll['ccmonth'] = ccmonth
        add_dll['ccyear'] = ccyear
        add_dll['checkaccount'] = checkaccount
        add_dll['fullname'] = fullname
        add_dll['address'] = address
        add_dll['postalcode'] = postalcode
        add_dll['city'] = city
        add_dll['state'] = state
        add_dll['phonenumber'] = phonenumber
        print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_add_finance_dict, add_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def finance_get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_get_finance_all)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return result

    def finance_get_item_by_username(self, username):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_get_finance_by_username_tuple, (username,))
        result = self.cursor.fetchall()
        # print(result)
        candidate_finance = []
        for row in result:
            item = dict(zip(amazon_db.finance_fields, row))
            candidate_finance.append(item)
        # print(candidate_finance)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return candidate_finance

    def finance_update_nameoncard(self, username, nameoncard):
        update_dll = {}
        update_dll['username'] = username
        if nameoncard:
            update_dll['nameoncard'] = nameoncard
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_nameoncard_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def finance_update_ccnumber(self, username, ccnumber):
        update_dll = {}
        update_dll['username'] = username
        if ccnumber:
            update_dll['ccnumber'] = ccnumber
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_ccnumber_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def finance_update_ccmonth(self, username, ccmonth):
        update_dll = {}
        update_dll['username'] = username
        if ccmonth:
            update_dll['ccmonth'] = ccmonth
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_ccmonth_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def finance_update_ccyear(self, username, ccyear):
        update_dll = {}
        update_dll['username'] = username
        if ccyear:
            update_dll['ccyear'] = ccyear
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_ccyear_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def finance_update_checkaccount(self, username, checkaccount):
        update_dll = {}
        update_dll['username'] = username
        if checkaccount:
            update_dll['checkaccount'] = checkaccount
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_checkaccount_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def finance_update_fullname(self, username, fullname):
        update_dll = {}
        update_dll['username'] = username
        if fullname:
            update_dll['fullname'] = fullname
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_fullname_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def finance_update_address(self, username, address):
        update_dll = {}
        update_dll['username'] = username
        if address:
            update_dll['address'] = address
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_address_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def finance_update_postalcode(self, username, postalcode):
        update_dll = {}
        update_dll['username'] = username
        if postalcode:
            update_dll['postalcode'] = postalcode
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_postalcode_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def finance_update_city(self, username, city):
        update_dll = {}
        update_dll['username'] = username
        if city:
            update_dll['city'] = city
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_city_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def finance_update_state(self, username, state):
        update_dll = {}
        update_dll['username'] = username
        if state:
            update_dll['state'] = state
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_state_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def finance_update_phonenumber(self, username, phonenumber):
        update_dll = {}
        update_dll['username'] = username
        if phonenumber:
            update_dll['phonenumber'] = phonenumber
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.FINANCE])
        self.cursor.execute(amazon_db.sql_update_finance_phonenumber_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def accountquota_add_item(self, checkaccount,wquota,mquota,yquota):
        add_dll = {}
        add_dll['checkaccount'] = checkaccount
        add_dll['wquota'] = wquota
        add_dll['mquota'] = mquota
        add_dll['yquota'] = yquota
        #print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTQUOTA])
        self.cursor.execute(amazon_db.sql_add_quota_dict, add_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    #get all accounts' quota
    def accountquota_get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.ACCOUNTQUOTA])
        self.cursor.execute(amazon_db.sql_get_accountquota_all)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return result

    #input specific user
    #output all related info
    def accountquota_get_one_item(self, checkaccount):
        query = {}
        query['checkaccount'] = checkaccount
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.ACCOUNTQUOTA])
        self.cursor.execute(amazon_db.sql_get_accountquota_by_account_dict, query)
        result = self.cursor.fetchall()
        quota_rslt = []
        for row in result:
            item = dict(zip(amazon_db.accountquota_fields, row))
            quota_rslt.append(item)
        #print(quota_rslt)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return quota_rslt

    def accountquota_update_wquota(self, checkaccount, wquota):
        update_dll = {}
        update_dll['checkaccount'] = checkaccount
        if wquota:
            update_dll['wquota'] = wquota
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTQUOTA])
        self.cursor.execute(amazon_db.sql_update_accountquota_wquota_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def accountquota_update_mquota(self, checkaccount, mquota):
        update_dll = {}
        update_dll['checkaccount'] = checkaccount
        if mquota:
            update_dll['mquota'] = mquota
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTQUOTA])
        self.cursor.execute(amazon_db.sql_update_accountquota_mquota_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def accountquota_update_yquota(self, checkaccount, yquota):
        update_dll = {}
        update_dll['checkaccount'] = checkaccount
        if yquota:
            update_dll['yquota'] = yquota
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ACCOUNTQUOTA])
        self.cursor.execute(amazon_db.sql_update_accountquota_yquota_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def productinfo_add_item(self, asin, department, busybox_price, order_price, keyword, brand):
        add_dll = {}
        add_dll['asin'] = asin
        add_dll['department'] = department
        add_dll['busybox_price'] = busybox_price
        add_dll['order_price'] = order_price
        add_dll['keyword'] = keyword
        add_dll['brand'] = brand
        #print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_add_productinfo_dict, add_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def productinfo_get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_get_productinfo_all)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return result

    def productinfo_get_one_item(self, asin):
        query = {}
        query['asin'] = asin
        print('query', query)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_get_productinfo_by_asin_dict, query)

        result = self.cursor.fetchall()
        assert self.cursor.rowcount == 1

        product_rslt = dict(zip(amazon_db.productinfo_fields, result[0]))
        #print(product_rslt)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return product_rslt
    def productinfo_update_department(self, asin, department):
        update_dll = {}
        update_dll['asin'] = asin
        if department:
            update_dll['department'] = department
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_update_productinfo_department_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def productinfo_update_busybox_price(self, asin, busybox_price):
        update_dll = {}
        update_dll['asin'] = asin
        if busybox_price:
            update_dll['busybox_price'] = busybox_price
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_update_productinfo_busybox_price_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def productinfo_update_order_price(self, asin, order_price):
        update_dll = {}
        update_dll['asin'] = asin
        if order_price:
            update_dll['order_price'] = order_price
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_update_productinfo_order_price_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def productinfo_update_keyword(self, asin, keyword):
        update_dll = {}
        update_dll['asin'] = asin
        if keyword:
            update_dll['keyword'] = keyword
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_update_productinfo_keyword_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def productinfo_update_brand(self, asin, brand):
        update_dll = {}
        update_dll['asin'] = asin
        if brand:
            update_dll['brand'] = brand
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.PRODUCTINFO])
        self.cursor.execute(amazon_db.sql_update_productinfo_brand_dict, update_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()


    def ordertask_add_item(self, username,asin,num,order_date=datetime.now()):
        add_dll = {}
        add_dll['username'] = username
        add_dll['asin'] = asin
        add_dll['num'] = num
        add_dll['order_date'] = order_date
        #print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_wr_lock[DB.ORDERTASK])
        self.cursor.execute(amazon_db.sql_add_ordertask_dict, add_dll)
        self.cursor.execute(self.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def ordertask_get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(self.sql_rd_lock[DB.ORDERTASK])
        self.cursor.execute(amazon_db.sql_get_ordertask_all)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(self.sql_unlock_all)
        self.cursor.close()
        return result
    def close(self):
        self.cnx.close()

db_test = amazon_db()
print(db_test.sql_rd_lock)
print(db_test.sql_wr_lock)
print(db_test.sql_rd_lock_all)
print(db_test.sql_wr_lock_all)