import sqlite3
import sys
import types
import ctypes
import requests	
import pymysql
# Get argv */
def save(string):
	# Saving string in libreturn.txt
	# Document is being read by Logo
	f = open('C:\\Users\\Christian\\output.txt','w')
	print(string,file=f)
	f.close
def logoarray(array):
	newarray = ""
	for element in array:
		if not isinstance(element, (list, tuple)):
			element = logostring(str(element))
		else:
			element = logoarray(element)
		newarray = newarray+" "+element
	return "["+newarray+"]"


def logostring(s):

	try:
		s = "\""+s
		s = str(s)
	except Exception as e:
		return
	s=s.replace(" ","\\ ");
	return s;

try:
	argument = float(sys.argv[1]);
except Exception as e:
	print("Error")
	sys.exit()
## sqlite
if argument == 1:
	try:
		db = sys.argv[2];
	except:
		print("Bitte als 2.Argument DB eingeben");
		sys.exit()
	try:
		command = sys.argv[3];
	except:
		print("Bitte als 3.Argument SQL-Query eingeben");
		sys.exit()
	try:
		conn = sqlite3.connect(db)
	except Exception as e:
			print(e)
			sys.exit()
	try:
		c = conn.cursor()
	except Exception as e:
		print(e)
		sys.exit()
	try:
		# Execution of command
		
		#Creating array for rows
		rows = []
		c.execute(command)
		for row in c:
			rows.append(row)
			
			#Appending row to rows
		if row == []:
			#if row is empty
			pass
		else:
			#print to file
			pass
		save(logoarray(rows))
		# Nur noch speichern als Logoliste
		
		conn.commit() # Save changes, might made
		conn.close() # Close connection
	except Exception as e:
		print(e)
if argument == 2:
			# Curl a webpage
			webpage = str(sys.argv[2])
			print(webpage)
			r = requests.get(webpage)
			print(r.content)
			pass
if argument == 3:
		if len(sys.argv)<7:
			print("Bitte mehr Argumente an das Script übergeben")
			sys.exit()
		try:
			server = str(sys.argv[2])
			user = str(sys.argv[3])
			passwort = str(sys.argv[4])
			db = str(sys.argv[5])
			command = str(sys.argv[6])
		except Exception as e:
			print(e)
			pass
		try:
			conn = pymysql.connect(host=server, user=user, passwd=passwort, db=db)
		except Exception as e:
			print(e)
			pass
			
		cur = conn.cursor()
		cur.execute(command)
		rows = []
		for r in cur:
			rows.append(r)
		save(logoarray(rows))
		cur.close()
		conn.close()
