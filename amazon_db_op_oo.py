from datetime import date, datetime, timedelta
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
    'port': '3306',
    'database': 'amazon'
}
config = remote_config


class accountinfo_db(object):
    sql_lock_read = ("LOCK TABLE accountinfo READ;")
    sql_lock_write = ("LOCK TABLE accountinfo WRITE;")
    sql_unlock_all = ("UNLOCK TABLES;")
    # args in tuple form
    sql_add_info_tuple = ("INSERT INTO accountinfo"
                          "(username, password, cookies, createdate, logindate, lastbuy, in_use, alive, MAC)"
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
    sql_update_pw_tuple = (
        "UPDATE accountinfo SET password=%s WHERE username=%s;")
    sql_update_cookie_tuple = (
        "UPDATE accountinfo SET cookies=%s WHERE username=%s;")
    sql_update_createdate_tuple = (
        "UPDATE accountinfo SET createdate=%s WHERE username=%s;")
    sql_update_logindate_tuple = (
        "UPDATE accountinfo SET logindate=%s WHERE username=%s;")
    sql_update_lastbuy_tuple = (
        "UPDATE accountinfo SET lastbuy=%s WHERE username=%s;")
    sql_update_in_use_tuple = (
        "UPDATE accountinfo SET in_use=%s WHERE username=%s;")
    sql_update_alive_tuple = (
        "UPDATE accountinfo SET alive=%s WHERE username=%s;")
    sql_update_MAC_tuple = ("UPDATE accountinfo SET MAC=%s WHERE username=%s;")

    # args in dict form
    sql_add_info_dict = ("INSERT INTO accountinfo"
                         "(username, password, cookies, createdate, logindate, lastbuy, alive, MAC)"
                         "VALUES (%(username)s, %(passwd)s, %(cookies)s, %(createdate)s, %(logindate)s, %(lastbuy)s, %(alive)s, %(MAC)s);")
    sql_update_pw_dict = (
        "UPDATE accountinfo SET password=%(passwd)s WHERE username=%(username)s;")
    sql_update_cookies_dict = (
        "UPDATE accountinfo SET cookies=%(cookies)s WHERE username=%(username)s;")
    sql_update_createdate_dict = (
        "UPDATE accountinfo SET createdate=%(createdate)s WHERE username=%(username)s;")
    sql_update_logindate_dict = (
        "UPDATE accountinfo SET logindate=%(logindate)s WHERE username=%(username)s;")
    sql_update_lastbuy_dict = (
        "UPDATE accountinfo SET lastbuy=%(lastbuy)s WHERE username=%(username)s;")
    sql_update_in_use_dict = (
        "UPDATE accountinfo SET in_use=%(in_use)s WHERE username=%(username)s;")
    sql_update_alive_dict = (
        "UPDATE accountinfo SET alive=%(alive)s WHERE username=%(username)s;")
    sql_update_MAC_dict = (
        "UPDATE accountinfo SET MAC=%(MAC)s WHERE username=%(username)s;")

    sql_get_info = ("SELECT * FROM accountinfo;")
    sql_get_info_by_lastbuy_tuple = (
        "SELECT * FROM accountinfo WHERE lastbuy < %s;")
    sql_get_info_by_lastbuy_dict = (
        "SELECT * FROM accountinfo WHERE lastbuy < %(lastbuy)s;")
    accountinfo_fields = [
        'userid',
        'username',
        'password',
        'cookies',
        'createdate',
        'logindate',
        'lastbuy',
        'in_use',
        'alive',
        'MAC']

    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        return

    def add_item(self, username, passwd, createdate=datetime.now(), logindate=datetime.now(
    ), lastbuy=datetime(1997, 1, 1), in_use=0, alive=1, cookies=None, MAC=None):
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

    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_get_info)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return result

    def get_item_by_lastbuy(self, interval):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountinfo_db.sql_lock_read)
        self.cursor = self.cnx.cursor()

        tdiff = timedelta(hours=interval)
        self.cursor.execute(
            accountinfo_db.sql_get_info_by_lastbuy_tuple, (datetime.now() + tdiff,))
        result = self.cursor.fetchall()
        # print(result)
        candidate_users = []
        for row in result:
            # print(row)
            item = dict(zip(accountinfo_db.accountinfo_fields, row))
            # print(item)
            candidate_users.append(item)
        # print(candidate_users)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return candidate_users

    def update_passwd(self, username, passwd):
        update_dll = {}
        update_dll['username'] = username
        if passwd:
            update_dll['passwd'] = passwd
        # print(update_dll)
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
        self.cursor.execute(
            accountinfo_db.sql_update_createdate_dict,
            update_dll)
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
        self.cursor.execute(
            accountinfo_db.sql_update_logindate_dict,
            update_dll)
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
    sql_update_shipaddress_fullname_tuple = (
        "UPDATE shipaddress SET fullname=%s WHERE username=%s;")
    sql_update_shipaddress_address_tuple = (
        "UPDATE shipaddress SET address=%s WHERE username=%s;")
    sql_update_shipaddress_postalcode_tuple = (
        "UPDATE shipaddress SET postalcode=%s WHERE username=%s;")
    sql_update_shipaddress_city_tuple = (
        "UPDATE shipaddress SET city=%s WHERE username=%s;")
    sql_update_shipaddress_state_tuple = (
        "UPDATE shipaddress SET state=%s WHERE username=%s;")
    sql_update_shipaddress_phonenumber_tuple = (
        "UPDATE shipaddress SET phonenumber=%s WHERE username=%s;")

    # args in dict form
    sql_add_shipaddr_dict = ("INSERT INTO shipaddress "
                             "(username, fullname, address, postalcode, city, state, phonenumber)"
                             "VALUES (%(username)s,%(fullname)s,%(address)s,%(postalcode)s,%(city)s,%(state)s,%(phonenumber)s)")
    sql_update_shipaddress_fullname_dict = (
        "UPDATE shipaddress SET fullname=%(fullname)s WHERE username=%(username)s;")
    sql_update_shipaddress_address_dict = (
        "UPDATE shipaddress SET address=%(address)s WHERE username=%(username)s;")
    sql_update_shipaddress_postalcode_dict = (
        "UPDATE shipaddress SET postalcode=%(postalcode)s WHERE username=%(username)s;")
    sql_update_shipaddress_city_dict = (
        "UPDATE shipaddress SET city=%(city)s WHERE username=%(username)s;")
    sql_update_shipaddress_state_dict = (
        "UPDATE shipaddress SET state=%(state)s WHERE username=%(username)s;")
    sql_update_shipaddress_phonenumber_dict = (
        "UPDATE shipaddress SET phonenumber=%(phonenumber)s WHERE username=%(username)s;")
    sql_get_info = ("SELECT * FROM shipaddress;")
    sql_get_info_by_username_tuple = (
        "SELECT * FROM shipaddress WHERE username=%s;")
    sql_get_info_by_username_dict = (
        "SELECT * FROM shipaddress WHERE username=%(username)s;")
    shipaddress_fields = [
        'addrid',
        'username',
        'fullname',
        'address',
        'postalcode',
        'city',
        'state',
        'phonenumber']

    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        return

    def add_item(self, username, fullname, address=None,
                 postalcode=None, city=None, state=None, phonenumber=None):
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

    def get_item_by_username(self, username):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        query = {}
        query['username'] = username

        self.cursor.execute(
            shipaddress_db.sql_get_info_by_username_dict, query)
        result = self.cursor.fetchall()
        print(result)
        candidate_shipaddr = []
        for row in result:
            # print(row)
            item = dict(zip(shipaddress_db.shipaddress_fields, row))
            # print(item)
            candidate_shipaddr.append(item)
        # print(candidate_users)
        self.cursor.execute(shipaddress_db.sql_unlock_all)
        self.cursor.close()
        return candidate_shipaddr

    def update_fullname(self, username, fullname):
        update_dll = {}
        update_dll['username'] = username
        if fullname:
            update_dll['fullname'] = fullname
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(shipaddress_db.sql_lock_write)
        self.cursor.execute(
            shipaddress_db.sql_update_shipaddress_fullname_dict,
            update_dll)
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
        self.cursor.execute(
            shipaddress_db.sql_update_shipaddress_address_dict,
            update_dll)
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
        self.cursor.execute(
            shipaddress_db.sql_update_shipaddress_postalcode_dict,
            update_dll)
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
        self.cursor.execute(
            shipaddress_db.sql_update_shipaddress_city_dict,
            update_dll)
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
        self.cursor.execute(
            shipaddress_db.sql_update_shipaddress_state_dict,
            update_dll)
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
        self.cursor.execute(
            shipaddress_db.sql_update_shipaddress_phonenumber_dict,
            update_dll)
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
    sql_update_finance_nameoncard_tuple = (
        "UPDATE finance SET nameoncard=%s WHERE username=%s;")
    sql_update_finance_ccnumber_tuple = (
        "UPDATE finance SET ccnumber=%s WHERE username=%s;")
    sql_update_finance_ccmonth_tuple = (
        "UPDATE finance SET ccmonth=%s WHERE username=%s;")
    sql_update_finance_fullname_tuple = (
        "UPDATE finance SET fullname=%s WHERE username=%s;")
    sql_update_finance_address_tuple = (
        "UPDATE finance SET address=%s WHERE username=%s;")
    sql_update_finance_ccyear_tuple = (
        "UPDATE finance SET ccyear=%s WHERE username=%s;")
    sql_update_finance_postalcode_tuple = (
        "UPDATE finance SET postalcode=%s WHERE username=%s;")
    sql_update_finance_city_tuple = (
        "UPDATE finance SET city=%s WHERE username=%s;")
    sql_update_finance_state_tuple = (
        "UPDATE finance SET state=%s WHERE username=%s;")
    sql_update_finance_phonenumber_tuple = (
        "UPDATE finance SET phonenumber=%s WHERE username=%s;")
    sql_update_finance_checkaccount_tuple = (
        "UPDATE finance SET checkaccount=%s WHERE username=%s;")

    # args in dict form
    sql_add_finance_dict = ("INSERT INTO finance "
                            "(username,nameoncard,ccnumber,ccmonth,ccyear,checkaccount,fullname,address, postalcode,city,state,phonenumber) "
                            "VALUES (%(username)s,%(nameoncard)s,%(ccnumber)s,%(ccmonth)s,%(ccyear)s,%(checkaccount)s,%(fullname)s,%(address)s,%(postalcode)s,%(city)s,%(state)s,%(phonenumber)s)")
    sql_update_finance_nameoncard_dict = (
        "UPDATE finance SET nameoncard=%(nameoncard)s WHERE username=%(username)s;")
    sql_update_finance_ccnumber_dict = (
        "UPDATE finance SET ccnumber=%(ccnumber)s WHERE username=%(username)s;")
    sql_update_finance_ccmonth_dict = (
        "UPDATE finance SET ccmonth=%(ccmonth)s WHERE username=%(username)s;")
    sql_update_finance_fullname_dict = (
        "UPDATE finance SET fullname=%(fullname)s WHERE username=%(username)s;")
    sql_update_finance_address_dict = (
        "UPDATE finance SET address=%(address)s WHERE username=%(username)s;")
    sql_update_finance_ccyear_dict = (
        "UPDATE finance SET ccyear=%(ccyear)s WHERE username=%(username)s;")
    sql_update_finance_postalcode_dict = (
        "UPDATE finance SET postalcode=%(postalcode)s WHERE username=%(username)s;")
    sql_update_finance_city_dict = (
        "UPDATE finance SET city=%(city)s WHERE username=%(username)s;")
    sql_update_finance_state_dict = (
        "UPDATE finance SET state=%(state)s WHERE username=%(username)s;")
    sql_update_finance_phonenumber_dict = (
        "UPDATE finance SET phonenumber=%(phonenumber)s WHERE username=%(username)s;")
    sql_update_finance_checkaccount_dict = (
        "UPDATE finance SET checkaccount=%(checkaccount)s WHERE username=%(username)s;")
    finance_fields = ['cardid', 'username', 'nameoncard', 'ccnumber', 'ccmonth', 'ccyear',
                      'checkaccount', 'fullname', 'address', 'postalcode', 'city', 'state', 'phonenumber']
    sql_get_info = ("SELECT * FROM finance;")
    sql_get_info_by_username_tuple = (
        "SELECT * FROM finance WHERE username=%s;")
    sql_get_info_by_username_dict = (
        "SELECT * FROM finance WHERE username=%(username)s;")

    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        return

    def add_item(self, username, nameoncard, ccnumber, ccmonth, ccyear,
                 checkaccount, fullname, address, postalcode, city, state, phonenumber):
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

    def get_item_by_username(self, username):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(
            finance_db.sql_get_info_by_username_tuple, (username,))
        result = self.cursor.fetchall()
        # print(result)
        candidate_finance = []
        for row in result:
            # print(row)
            item = dict(zip(finance_db.finance_fields, row))
            # print(item)
            candidate_finance.append(item)
        # print(candidate_finance)
        self.cursor.execute(accountinfo_db.sql_unlock_all)
        self.cursor.close()
        return candidate_finance

    def update_nameoncard(self, username, nameoncard):
        update_dll = {}
        update_dll['username'] = username
        if nameoncard:
            update_dll['nameoncard'] = nameoncard
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(finance_db.sql_lock_write)
        self.cursor.execute(
            finance_db.sql_update_finance_nameoncard_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_ccnumber_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_ccmonth_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_ccyear_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_checkaccount_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_fullname_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_address_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_postalcode_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_city_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_state_dict,
            update_dll)
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
        self.cursor.execute(
            finance_db.sql_update_finance_phonenumber_dict,
            update_dll)
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
    sql_update_accountquota_wquota_tuple = (
        "UPDATE accountquota SET wquota=%s WHERE checkaccount=%s;")
    sql_update_accountquota_mquota_tuple = (
        "UPDATE accountquota SET mquota=%s WHERE checkaccount=%s;")
    sql_update_accountquota_yquota_tuple = (
        "UPDATE accountquota SET yquota=%s WHERE checkaccount=%s;")

    # args in dict form
    sql_add_quota_dict = ("INSERT INTO accountquota"
                          "(checkaccount,wquota,mquota,yquota)"
                          "VALUES (%(checkaccount)s,%(wquota)s,%(mquota)s,%(yquota)s)")
    sql_update_accountquota_wquota_dict = (
        "UPDATE accountquota SET wquota=%(wquota)s WHERE checkaccount=%(checkaccount)s;")
    sql_update_accountquota_mquota_dict = (
        "UPDATE accountquota SET mquota=%(mquota)s WHERE checkaccount=%(checkaccount)s;")
    sql_update_accountquota_yquota_dict = (
        "UPDATE accountquota SET yquota=%(yquota)s WHERE checkaccount=%(checkaccount)s;")
    sql_get_info = ("SELECT * FROM accountquota;")

    sql_get_one_info_tuple = (
        "SELECT * FROM accountquota WHERE checkaccount=%s;")
    sql_get_one_info_dict = (
        "SELECT * FROM accountquota WHERE checkaccount=%(checkaccount)s;")
    accountquota_fields = [
        'accountid',
        'checkaccount',
        'wquota',
        'mquota',
        'yquota']

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print('haha1', err)
        return

    def add_item(self, checkaccount, wquota, mquota, yquota):
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

    # get all accounts' quota
    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_get_info)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cursor.close()
        return result

    # input specific user
    # output all related info
    def get_one_item(self, checkaccount):
        query = {}
        query['checkaccount'] = checkaccount
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_get_one_info_dict, query)
        result = self.cursor.fetchall()
        quota_rslt = []
        for row in result:
            item = dict(zip(accountquota_db.accountquota_fields, row))
            # print(item)
            quota_rslt.append(item)
        # print(quota_rslt)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cursor.close()
        return quota_rslt

    def update_wquota(self, checkaccount, wquota):
        update_dll = {}
        update_dll['checkaccount'] = checkaccount
        if wquota:
            update_dll['wquota'] = wquota
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(accountquota_db.sql_lock_write)
        self.cursor.execute(
            accountquota_db.sql_update_accountquota_wquota_dict,
            update_dll)
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
        self.cursor.execute(
            accountquota_db.sql_update_accountquota_mquota_dict,
            update_dll)
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
        self.cursor.execute(
            accountquota_db.sql_update_accountquota_yquota_dict,
            update_dll)
        self.cursor.execute(accountquota_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def close(self):
        self.cnx.close()


class productinfo_db(object):
    sql_lock_read = ("LOCK TABLE productinfo READ;")
    sql_lock_write = ("LOCK TABLE productinfo WRITE;")
    sql_unlock_all = ("UNLOCK TABLES;")
    # args in tuple form
    sql_add_productinfo_tuple = ("INSERT INTO productinfo"
                                 "(asin, department, busybox_price, order_price, keyword, brand)"
                                 "VALUES (%s,%s,%s,%s,%s,%s)")
    sql_update_productinfo_department_tuple = (
        "UPDATE productinfo SET department=%s WHERE asin=%s;")
    sql_update_productinfo_busybox_price_tuple = (
        "UPDATE productinfo SET busybox_price=%s WHERE asin=%s;")
    sql_update_productinfo_order_price_tuple = (
        "UPDATE productinfo SET order_price=%s WHERE asin=%s;")
    sql_update_productinfo_keyword_tuple = (
        "UPDATE productinfo SET keyword=%s WHERE asin=%s;")
    sql_update_productinfo_brand_tuple = (
        "UPDATE productinfo SET brand=%s WHERE asin=%s;")

    # args in dict form
    sql_add_productinfo_dict = ("INSERT INTO productinfo"
                                "(asin, department, busybox_price, order_price, keyword, brand)"
                                "VALUES (%(asin)s,%(department)s,%(busybox_price)s,%(order_price)s,%(keyword)s,%(brand)s)")
    sql_update_productinfo_department_dict = (
        "UPDATE productinfo SET department=%(department)s WHERE asin=%(asin)s;")
    sql_update_productinfo_busybox_price_dict = (
        "UPDATE productinfo SET busybox_price=%(busybox_price)s WHERE asin=%(asin)s;")
    sql_update_productinfo_order_price_dict = (
        "UPDATE productinfo SET order_price=%(order_price)s WHERE asin=%(asin)s;")
    sql_update_productinfo_keyword_dict = (
        "UPDATE productinfo SET keyword=%(keyword)s WHERE asin=%(asin)s;")
    sql_update_productinfo_brand_dict = (
        "UPDATE productinfo SET brand=%(brand)s WHERE asin=%(asin)s;")
    sql_get_info = ("SELECT * FROM productinfo;")
    sql_get_one_info_tuple = ("SELECT * FROM productinfo WHERE asin=%s;")
    sql_get_one_info_dict = ("SELECT * FROM productinfo WHERE asin=%(asin)s;")
    productinfo_fields = [
        'productid',
        'asin',
        'department',
        'busybox_price',
        'order_price',
        'keyword',
        'brand']

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print('haha2', err)
        return

    def add_item(self, asin, department, busybox_price,
                 order_price, keyword, brand):
        add_dll = {}
        add_dll['asin'] = asin
        add_dll['department'] = department
        add_dll['busybox_price'] = busybox_price
        add_dll['order_price'] = order_price
        add_dll['keyword'] = keyword
        add_dll['brand'] = brand
        print(add_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_write)
        self.cursor.execute(productinfo_db.sql_add_productinfo_dict, add_dll)
        self.cursor.execute(productinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return

    def get_item(self):
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_get_info)
        result = self.cursor.fetchall()
        # print(result)
        self.cursor.execute(productinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()
        return result

    def get_one_item(self, asin):
        query = {}
        query['asin'] = asin
        print('query', query)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_read)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_get_one_info_dict, query)

        result = self.cursor.fetchall()
        assert self.cursor.rowcount == 1

        product_rslt = dict(zip(productinfo_db.productinfo_fields, result[0]))
        # print(product_rslt)
        self.cursor.execute(productinfo_db.sql_unlock_all)
        self.cursor.close()
        return product_rslt

    def update_department(self, asin, department):
        update_dll = {}
        update_dll['asin'] = asin
        if department:
            update_dll['department'] = department
        # print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_write)
        self.cursor.execute(
            productinfo_db.sql_update_productinfo_department_dict,
            update_dll)
        self.cursor.execute(productinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_busybox_price(self, asin, busybox_price):
        update_dll = {}
        update_dll['asin'] = asin
        if busybox_price:
            update_dll['busybox_price'] = busybox_price
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_write)
        self.cursor.execute(
            productinfo_db.sql_update_productinfo_busybox_price_dict,
            update_dll)
        self.cursor.execute(productinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_order_price(self, asin, order_price):
        update_dll = {}
        update_dll['asin'] = asin
        if order_price:
            update_dll['order_price'] = order_price
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_write)
        self.cursor.execute(
            productinfo_db.sql_update_productinfo_order_price_dict,
            update_dll)
        self.cursor.execute(productinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_keyword(self, asin, keyword):
        update_dll = {}
        update_dll['asin'] = asin
        if keyword:
            update_dll['keyword'] = keyword
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_write)
        self.cursor.execute(
            productinfo_db.sql_update_productinfo_keyword_dict,
            update_dll)
        self.cursor.execute(productinfo_db.sql_unlock_all)
        self.cnx.commit()
        self.cursor.close()

    def update_brand(self, asin, brand):
        update_dll = {}
        update_dll['asin'] = asin
        if brand:
            update_dll['brand'] = brand
        print(update_dll)
        self.cursor = self.cnx.cursor()
        self.cursor.execute(productinfo_db.sql_lock_write)
        self.cursor.execute(
            productinfo_db.sql_update_productinfo_brand_dict,
            update_dll)
        self.cursor.execute(productinfo_db.sql_unlock_all)
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
    sql_update_ordertask_asin_tuple = (
        "UPDATE ordertask SET asin=%s WHERE username=%s;")
    sql_update_ordertask_num_tuple = (
        "UPDATE ordertask SET num=%s WHERE username=%s;")
    sql_update_ordertask_order_date_tuple = (
        "UPDATE ordertask SET order_date=%s WHERE username=%s;")

    # args in dict form
    sql_add_ordertask_dict = ("INSERT INTO ordertask"
                              "(username, asin, num, order_date)"
                              "VALUES (%(username)s,%(asin)s,%(num)s, %(order_date)s)")
    sql_update_ordertask_asin_dict = (
        "UPDATE ordertask SET asin=%s WHERE username=%s;")
    sql_update_ordertask_num_dict = (
        "UPDATE ordertask SET num=%s WHERE username=%s;")
    sql_update_ordertask_order_date_dict = (
        "UPDATE ordertask SET order_date=%s WHERE username=%s;")
    sql_get_info = ("SELECT * FROM ordertask;")
    order_task_fields = [
        'ordertaskid',
        'username',
        'asin',
        'num',
        'order_date']

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print('haha3', err)
        return

    def add_item(self, username, asin, num, order_date=datetime.now()):
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
        db.add_item(
            'MarvinDickerson987@foxairmail.com',
            'Jack Chan',
            '1776 Bicentennial way, apt i-5',
            '02911',
            'North Providence',
            'RI',
            '6232295326')
    else:
        rslt = db.get_item()
        for row in rslt:
            print(row)

        db.update_address(
            'MarvinDickerson987@foxairmail.com',
            'hetianshangcheng')
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
        db.add_item('SteveCarsey@foxairmail.com', 'George Troni', '4859103482757156',
                    '04', '2022', 'TDLan-549', 'George Troni', '6 redglobe ct', '29681-3615',
                    'simpsonville', 'SC', '8645612655')
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
        db.add_item('TDLan-549', 200, 800, 10000)
        db.add_item('BOALI-848', 200, 800, 10000)
    else:
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_mquota('TDLan-549', 300)
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_wquota('TDLan-549', 900)
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_yquota('TDLan-549', 10010)
        rslt = db.get_item()
        for row in rslt:
            print(row)
    db.close()
    del db


def dbg_productinfo():
    first_time = 0
    db = productinfo_db()
    rslt = db.get_item()
    for row in rslt:
        print(row)
    if first_time == 1:
        db.add_item(
            'B077RYNF82',
            'Electronics',
            '89.99',
            '89.99',
            'wireless bluetooth earbud',
            'STERIO')
        db.add_item(
            'B07439HNFT',
            'Electronics',
            '94.99',
            '94.99',
            'dash cam 4k',
            'STERIO')
    else:
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_department('B077RYNF82', 'telecom')
        db.update_department('B07439HNFT', 'unicorn')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_busybox_price('B077RYNF82', '100.00')
        db.update_busybox_price('B07439HNFT', '120.00')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_busybox_price('B077RYNF82', '110.00')
        db.update_busybox_price('B07439HNFT', '130.00')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_keyword('B077RYNF82', 'asdfasdfasdfasdf')
        db.update_keyword('B07439HNFT', 'oiuiuououou')
        rslt = db.get_item()
        for row in rslt:
            print(row)
        db.update_brand('B077RYNF82', 'huawei')
        db.update_brand('B07439HNFT', 'HIK')
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
    db.add_item('lee', 'B077RYNF82', 10)
    db.add_item('lee', 'B07439HNFT', 20)
    db.add_item('AnnieLee@foxairmail.com', 'B07439HNFT', 30)
    db.add_item('BingTan89@foxairmail.com', 'B07439HNFT', 40)
    db.add_item('MineralDick@foxairmail.com', 'B077RYNF82', 50)
    db.close()
    del db

# select candidates which meets some requirements
# min_val:each buyer should spend minimum money
# buyer_interval:lastbuy time should be more than this, in hrs


def get_available_user(min_val, buyer_interval, **asin_task):
    # get available users according to buyer_interval, should not use users
    # which have purchased recently
    db1_accountinfo = accountinfo_db()
    db2_finance = finance_db()
    db3_accountquota = accountquota_db()
    db4_productinfo = productinfo_db()
    db5_shipaddr = shipaddress_db()
    accountinfo_rslt = db1_accountinfo.get_item_by_lastbuy(buyer_interval)
    print('**********get users according to buyer_interval**********')
    for row in accountinfo_rslt:
        print(row['username'])

    # get users' shipaddress
    shipaddr_result = db5_shipaddr.get_item_by_username(
        'MarvinDickerson987@foxairmail.com')
    print('\n**********get shipaddreess**********')
    print(shipaddr_result)

    # get bank-account those users are using, check if quota enough
    print('\n**********get finance according to user candidate**********')
    finance_rslt = db2_finance.get_item_by_username(
        'SteveCarsey@foxairmail.com')
    # print(finance_rslt)
    for row in finance_rslt:
        # print(row['checkaccount'])
        quota_rslt = db3_accountquota.get_one_item(row['checkaccount'])
        print(quota_rslt)

    print('asin_task', asin_task)
    asin_products = []
    for key in asin_task.keys():
        # print(key)
        product = db4_productinfo.get_one_item(key)
        # print(product)
        asin_products.append(product)

    db1_accountinfo.close()
    del db1_accountinfo
    db2_finance.close()
    del db2_finance
    pass


# dbg_accountinfo()
# dbg_shipaddr()
# dbg_finance()
# dbg_accountquota()
# dbg_productinfo()
# dbg_ordertask()
get_available_user(100, 24, **{'B077RYNF82': 10, 'B07439HNFT': 20})

if __name__ == '__main__':
    pass
    # test_accountinfo()
    # test_shipaddr()
    # test_finance()
    # test_accountquota()
