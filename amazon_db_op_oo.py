from datetime import date, datetime
import mysql.connector
from mysql.connector import errorcode
import logging

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
class accountinfo_db(object):
    sql_lock_read = ("LOCK TABLE accountinfo READ;")
    sql_lock_write = ("LOCK TABLE accountinfo WRITE;")
    sql_unlock_all = ("UNLOCK TABLES;")
    #args in tuple form
    sql_add_info_tuple = ("INSERT INTO accountinfo"
                    "(username, password, cookies, createdate, logindate, lastbuy, in_use, alive, MAC)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
    sql_update_pw_tuple = ("UPDATE accountinfo SET password=%s WHERE username=%s;")
    sql_update_cookie_tuple = ("UPDATE accountinfo SET cookies=%s WHERE username=%s;")
    sql_update_createdate_tuple = ("UPDATE accountinfo SET createdate=%s WHERE username=%s;")
    sql_update_logindate_tuple = ("UPDATE accountinfo SET logindate=%s WHERE username=%s;")
    sql_update_lastbuy_tuple = ("UPDATE accountinfo SET lastbuy=%s WHERE username=%s;")
    sql_update_in_use_tuple = ("UPDATE accountinfo SET in_use=%s WHERE username=%s;")
    sql_update_alive_tuple = ("UPDATE accountinfo SET alive=%s WHERE username=%s;")
    sql_update_MAC_tuple = ("UPDATE accountinfo SET MAC=%s WHERE username=%s;")

    #args in dict form
    sql_add_info_dict = ("INSERT INTO accountinfo"
                          "(username, password, cookies, createdate, logindate, lastbuy, alive, MAC)"
                          "VALUES (%(username)s, %(passwd)s, %(cookies)s, %(createdate)s, %(logindate)s, %(lastbuy)s, %(alive)s, %(MAC)s);")
    sql_update_pw_dict = ("UPDATE accountinfo SET password=%(passwd)s WHERE username=%(username)s;")
    sql_update_cookies_dict = ("UPDATE accountinfo SET cookies=%(cookies)s WHERE username=%(username)s;")
    sql_update_createdate_dict = ("UPDATE accountinfo SET createdate=%(createdate)s WHERE username=%(username)s;")
    sql_update_logindate_dict = ("UPDATE accountinfo SET logindate=%(logindate)s WHERE username=%(username)s;")
    sql_update_lastbuy_dict = ("UPDATE accountinfo SET lastbuy=%(lastbuy)s WHERE username=%(username)s;")
    sql_update_in_use_dict = ("UPDATE accountinfo SET in_use=%(in_use)s WHERE username=%(username)s;")
    sql_update_alive_dict = ("UPDATE accountinfo SET alive=%(alive)s WHERE username=%(username)s;")
    sql_update_MAC_dict = ("UPDATE accountinfo SET MAC=%(MAC)s WHERE username=%(username)s;")

    sql_get_info = ("SELECT * FROM accountinfo;")
    accountinfo_fields = ('username', 'password', 'cookies', 'createdate', 'logindate', 'lastbuy', 'in_use', 'alive', 'MAC')

    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        return
    def add_item(self, username, passwd, createdate=datetime.now(), logindate=datetime.now(), lastbuy=datetime(1997,1,1), in_use=0, alive=1, cookies=None, MAC=None):
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
        print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_add_info_dict, add_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def get_available_user(self, min_val, time_cond, **asin_task):
        #user-->wquota
        #user->mquota

        pass
    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_get_info)
        result = self.cursor.fetchall()
        #print(result)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return result
    def update_passwd(self, username, passwd):
        update_dll = {}
        update_dll['username'] = username
        if passwd:
            update_dll['passwd'] = passwd
        #print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_pw_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_createdate(self, username, createdate):
        update_dll = {}
        update_dll['username'] = username
        if createdate:
            update_dll['createdate'] = createdate
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_createdate_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_logindate(self, username, logindate):
        update_dll = {}
        update_dll['username'] = username
        if logindate:
            update_dll['logindate'] = logindate
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_logindate_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_lastbuy(self, username, lastbuy):
        update_dll = {}
        update_dll['username'] = username
        if lastbuy:
            update_dll['lastbuy'] = lastbuy
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_lastbuy_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_in_use(self, username, in_use):
        update_dll = {}
        update_dll['username'] = username
        if in_use:
            update_dll['in_use'] = in_use
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_in_use_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_alive(self, username, alive):
        update_dll = {}
        update_dll['username'] = username
        if alive:
            update_dll['alive'] = alive
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_alive_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_cookies(self, username, cookies):
        update_dll = {}
        update_dll['username'] = username
        if cookies:
            update_dll['cookies'] = cookies
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_cookies_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_MAC(self, username, MAC):
        update_dll = {}
        update_dll['username'] = username
        if MAC:
            update_dll['MAC'] = MAC
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_write)
        self.cursor.execute(accountinfo_db.sql_update_MAC_dict, update_dll)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def close(self):
        self.cnx.close()


class shipaddress_db(object):
    sql_lock_read = ("LOCK TABLE shipaddress READ;")
    sql_lock_write = ("LOCK TABLE shipaddress WRITE;")
    sql_unlock_all = ("UNLOCK TABLES;")
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
    sql_get_info = ("SELECT * FROM shipaddress;")
    shipaddress_fields = ('username', 'fullname', 'address', 'postalcode', 'city', 'state', 'phonenumber')

    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        return

    def add_item(self, username, fullname, address=None, postalcode=None, city=None, state=None, phonenumber=None):
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
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(shipaddress_db.sql_add_shipaddr_dict, add_dll)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_get_info)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return result

    def update_fullname(self, username, fullname):
        update_dll = {}
        update_dll['username'] = username
        if fullname:
            update_dll['fullname'] = fullname
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(shipaddress_db.sql_update_shipaddress_fullname_dict, update_dll)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_address(self, username, address):
        update_dll = {}
        update_dll['username'] = username
        if address:
            update_dll['address'] = address
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(shipaddress_db.sql_update_shipaddress_address_dict, update_dll)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_postalcode(self, username, postalcode):
        update_dll = {}
        update_dll['username'] = username
        if postalcode:
            update_dll['postalcode'] = postalcode
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(shipaddress_db.sql_update_shipaddress_postalcode_dict, update_dll)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_city(self, username, city):
        update_dll = {}
        update_dll['username'] = username
        if city:
            update_dll['city'] = city
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(shipaddress_db.sql_update_shipaddress_city_dict, update_dll)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_state(self, username, state):
        update_dll = {}
        update_dll['username'] = username
        if state:
            update_dll['state'] = state
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(shipaddress_db.sql_update_shipaddress_state_dict, update_dll)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_phonenumber(self, username, phonenumber):
        update_dll = {}
        update_dll['username'] = username
        if phonenumber:
            update_dll['phonenumber'] = phonenumber
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(shipaddress_db.sql_update_shipaddress_phonenumber_dict, update_dll)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def close(self):
        self.cnx.close()


class finance_db(object):
    sql_lock_read = ("LOCK TABLE finance READ;")
    sql_lock_write = ("LOCK TABLE finance WRITE;")
    sql_unlock_all = ("UNLOCK TABLES;")
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
    sql_update_finance_ccmonth_dict= ("UPDATE finance SET ccmonth=%(ccmonth)s WHERE username=%(username)s;")
    sql_update_finance_fullname_dict = ("UPDATE finance SET fullname=%(fullname)s WHERE username=%(username)s;")
    sql_update_finance_address_dict = ("UPDATE finance SET address=%(address)s WHERE username=%(username)s;")
    sql_update_finance_ccyear_dict = ("UPDATE finance SET ccyear=%(ccyear)s WHERE username=%(username)s;")
    sql_update_finance_postalcode_dict = ("UPDATE finance SET postalcode=%(postalcode)s WHERE username=%(username)s;")
    sql_update_finance_city_dict = ("UPDATE finance SET city=%(city)s WHERE username=%(username)s;")
    sql_update_finance_state_dict = ("UPDATE finance SET state=%(state)s WHERE username=%(username)s;")
    sql_update_finance_phonenumber_dict = ("UPDATE finance SET phonenumber=%(phonenumber)s WHERE username=%(username)s;")
    sql_update_finance_checkaccount_dict = ("UPDATE finance SET checkaccount=%(checkaccount)s WHERE username=%(username)s;")
    finance_fields = ('username', 'nameoncard', 'ccnumber', 'ccmonth', 'ccyear',
                      'checkaccount', 'fullname', 'address', 'postalcode', 'city', 'state', 'phonenumber')
    sql_get_info = ("SELECT * FROM finance;")

    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        return

    def add_item(self, username, nameoncard, ccnumber, ccmonth, ccyear,
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
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_add_finance_dict, add_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_get_info)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return result

    def update_nameoncard(self, username, nameoncard):
        update_dll = {}
        update_dll['username'] = username
        if nameoncard:
            update_dll['nameoncard'] = nameoncard
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_nameoncard_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_ccnumber(self, username, ccnumber):
        update_dll = {}
        update_dll['username'] = username
        if ccnumber:
            update_dll['ccnumber'] = ccnumber
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_ccnumber_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_ccmonth(self, username, ccmonth):
        update_dll = {}
        update_dll['username'] = username
        if ccmonth:
            update_dll['ccmonth'] = ccmonth
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_ccmonth_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_ccyear(self, username, ccyear):
        update_dll = {}
        update_dll['username'] = username
        if ccyear:
            update_dll['ccyear'] = ccyear
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_ccyear_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_checkaccount(self, username, checkaccount):
        update_dll = {}
        update_dll['username'] = username
        if checkaccount:
            update_dll['checkaccount'] = checkaccount
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_checkaccount_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_fullname(self, username, fullname):
        update_dll = {}
        update_dll['username'] = username
        if fullname:
            update_dll['fullname'] = fullname
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_fullname_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_address(self, username, address):
        update_dll = {}
        update_dll['username'] = username
        if address:
            update_dll['address'] = address
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_address_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_postalcode(self, username, postalcode):
        update_dll = {}
        update_dll['username'] = username
        if postalcode:
            update_dll['postalcode'] = postalcode
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_postalcode_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_city(self, username, city):
        update_dll = {}
        update_dll['username'] = username
        if city:
            update_dll['city'] = city
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_city_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_state(self, username, state):
        update_dll = {}
        update_dll['username'] = username
        if state:
            update_dll['state'] = state
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_state_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def update_phonenumber(self, username, phonenumber):
        update_dll = {}
        update_dll['username'] = username
        if phonenumber:
            update_dll['phonenumber'] = phonenumber
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(finance_db.sql_update_finance_phonenumber_dict, update_dll)
        self.cursor.execute(finance_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
    def close(self):
        self.cnx.close()


class accountquota_db(object):
    sql_lock_read = ("LOCK TABLE accountquota READ;")
    sql_lock_write = ("LOCK TABLE accountquota WRITE;")
    sql_unlock_all = ("UNLOCK TABLES;")
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
    sql_get_info = ("SELECT * FROM accountquota;")

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print('haha1', err)
        return

    def add_item(self, checkaccount,wquota,mquota,yquota):
        add_dll = {}
        add_dll['checkaccount'] = checkaccount
        add_dll['wquota'] = wquota
        add_dll['mquota'] = mquota
        add_dll['yquota'] = yquota
        print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_write)
        self.cursor.execute(accountquota_db.sql_add_quota_dict, add_dll)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_get_info)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return result

    def update_wquota(self, checkaccount, wquota):
        update_dll = {}
        update_dll['checkaccount'] = checkaccount
        if wquota:
            update_dll['wquota'] = wquota
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_write)
        self.cursor.execute(accountquota_db.sql_update_accountquota_wquota_dict, update_dll)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_mquota(self, checkaccount, mquota):
        update_dll = {}
        update_dll['checkaccount'] = checkaccount
        if mquota:
            update_dll['mquota'] = mquota
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_write)
        self.cursor.execute(accountquota_db.sql_update_accountquota_mquota_dict, update_dll)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_yquota(self, checkaccount, yquota):
        update_dll = {}
        update_dll['checkaccount'] = checkaccount
        if yquota:
            update_dll['yquota'] = yquota
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_write)
        self.cursor.execute(accountquota_db.sql_update_accountquota_yquota_dict, update_dll)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def close(self):
        self.cnx.close()

class ordertask_db(object):
    sql_lock_read = ("LOCK TABLE ordertask READ;")
    sql_lock_write = ("LOCK TABLE ordertask WRITE;")
    sql_unlock_all = ("UNLOCK TABLES;")
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
    sql_get_info = ("SELECT * FROM ordertask;")

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print('haha2', err)
        return

    def add_item(self, username,asin,num,order_date=datetime.now()):
        add_dll = {}
        add_dll['username'] = username
        add_dll['asin'] = asin
        add_dll['num'] = num
        add_dll['order_date'] = order_date
        print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(ordertask_db.sql_lock_write)
        self.cursor.execute(ordertask_db.sql_add_ordertask_dict, add_dll)
        self.cursor.execute(ordertask_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(ordertask_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(ordertask_db.sql_get_info)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(ordertask_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return result

    def close(self):
        self.cnx.close()





def dbg_accountinfo():
    first_time = 0
    db = accountinfo_db()
    rslt = db.get_item()
    for row in rslt:
        print(row)

    if first_time == 1:
        db.add_item('lee', '456456')
    else:
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_passwd('lee', '123345')
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_cookies('lee', 'asdfsdfghgh')
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_alive('lee', 1)
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_createdate('lee', datetime.now())
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_logindate('lee', datetime.now())
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_lastbuy('lee', datetime.now())
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_in_use('lee', 1)
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_MAC('lee', '00-11-22-33-44-55')
        rslt = db.get_item()
        for row in rslt:
            print(row)
    db.close()
    del db


def dbg_shipaddr():
    first_time = 1
    db = shipaddress_db()
    rslt = db.get_item()
    for row in rslt:
        print(row)
    if first_time == 1:
        db.add_item('MarvinDickerson987@foxairmail.com', 'Jack Chan',  '1776 Bicentennial way, apt i-5','02911','North Providence','RI','6232295326')
    else:
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_address('MarvinDickerson987@foxairmail.com', 'hetianshangcheng')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_city('MarvinDickerson987@foxairmail.com', 'hz')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_fullname('MarvinDickerson987@foxairmail.com', 'lleeeooo')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_phonenumber('MarvinDickerson987@foxairmail.com', '123123123')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_postalcode('MarvinDickerson987@foxairmail.com', '310000')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_state('MarvinDickerson987@foxairmail.com', 'zj')
        rslt = db.get_item()
        for row in rslt:
            print(row)

    db.close()
    del db

def dbg_finance():
    first_time = 1
    db = finance_db()
    rslt = db.get_item()
    for row in rslt:
        print(row)

    if first_time == 1:
        db.add_item('SteveCarsey@foxairmail.com','George Troni','4859103482757156',
                 '04','2022','TDLan-549','George Troni','6 redglobe ct','29681-3615',
                 'simpsonville','SC','8645612655')
        db.add_item('AnnieLee@foxairmail.com', 'Annie Lee', '4859109471703325',
                    '04', '2022', 'TDLan-549', 'Annie Lee', '193 central st. ste W102', '03051',
                    'nashua', 'NH', '3054146488')
        db.add_item('BingTan89@foxairmail.com', 'Bing Tan', '4859101936347160',
                    '04', '2022', 'TDLan-549', 'Bing Tan', '3308 Trappers Cove Trail, Apt 3D', '48910',
                    'Lansing', 'MI', '6508890052')
        db.add_item('MineralDick@foxairmail.com', 'Mineral Dick', '4859107167920401',
                    '04', '2022', 'TDLan-549', 'Mineral Dick', '193 central st. Apt W253', '03051',
                    'nashua', 'NH', '4242237285')
        rslt = db.get_item()
        for row in rslt:
            print(row)
    else:
        db.update_state('SteveCarsey@foxairmail.com', 'zj')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_postalcode('SteveCarsey@foxairmail.com', '310000')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_fullname('SteveCarsey@foxairmail.com', 'leooooooo')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_phonenumber('SteveCarsey@foxairmail.com', '123123345345')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_city('SteveCarsey@foxairmail.com', 'hz')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_address('SteveCarsey@foxairmail.com', 'HTSC')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_ccmonth('SteveCarsey@foxairmail.com', '05')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_ccnumber('SteveCarsey@foxairmail.com', '99999999')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_ccyear('SteveCarsey@foxairmail.com', '2011')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_checkaccount('SteveCarsey@foxairmail.com', 'shawnelee88')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_nameoncard('SteveCarsey@foxairmail.com', 'XML')
        rslt = db.get_item()
        for row in rslt:
            print(row)

    db.close()
    del db

def dbg_accountquota():
    first_time = 1
    db = accountquota_db()
    rslt = db.get_item()
    for row in rslt:
        print(row)
    if first_time == 1:
        db.add_item('TDLan-549',200,800,10000)
        db.add_item('BOALI-848', 200, 800, 10000)
    else:
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_mquota('TDLan-549',300)
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_wquota('TDLan-549',900)
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_yquota('TDLan-549',10010)
        rslt = db.get_item()
        for row in rslt:
            print(row)
    db.close()
    del db

def dbg_ordertask():
    db = ordertask_db()
    rslt = db.get_item()
    for row in rslt:
        print(row)
    db.add_item('lee','B077RYNF82',10)
    db.add_item('lee', 'B07439HNFT', 20)
    db.add_item('AnnieLee@foxairmail.com', 'B07439HNFT', 30)
    db.add_item('BingTan89@foxairmail.com', 'B07439HNFT', 40)
    db.add_item('MineralDick@foxairmail.com', 'B077RYNF82', 50)
    db.close()
    del db

#dbg_accountinfo()
#dbg_shipaddr()
#dbg_finance()
#dbg_accountquota()
#dbg_ordertask()

if __name__=='__main__':
    pass
    #test_accountinfo()
    #test_shipaddr()
    #test_finance()
    #test_accountquota()