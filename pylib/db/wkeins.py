#Import
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import urllib.request,urllib.parse
import os
import sqlite3
import re
import socket
import sys
from threading import Thread
allpages = []
sys.setrecursionlimit(500000)
def getsite(url,depth):
        try:
	  
                highestdepth = 7
               	
                if "wikimedia" in url:
                        return
                if depth == highestdepth:
                        return
                if "wikipedia" in url and depth == highestdepth-1:
                        return
                if "#" in url:
                        url = url.split("#")[0]
                if url in allpages:
                        return
                if "wikipedia" in url and not "de.wikipedia" in url:
                        return
                allpages.append(url)
                if not url.startswith("http"):
                       
                        try:
                                socket.inet_aton(url)
                                print("nohttp")
                                url = "http://" + url
                        except socket.error:
                                return
                        except Exception as e:
                                print(e)
                                return
                r = requests.get(url)
                data = r.text
                soup = BeautifulSoup(data)     
                if "Erstellen" in soup.title.string:
                        return;
               
                if "Weltkrieg" not in soup.get_text():
                        return
                if "Datei" in soup.title.string:
                        return
                if "bearbeiten" in soup.title.string:
                        return
                if "Suchergebnisse" in soup.title.string:
                        return
                if "Begriffserklärung" in soup.title.string:
                        return
                print("NR:"+str(len(allpages))+" " +url+ " " + str(depth))
        except KeyboardInterrupt :
                exit()
        except requests.exceptions.RequestException as e:
                print(e)
        except Exception as e:
                print("Couldn't fetch url "+url)
                return
        #Ab hier Speicherung
        #Rekursion
        
        try:
                savedata(soup,url,depth,soup.title.string)
                print(len(getalllinks(data,url)))
       
                links = getalllinks(data,url)
               
                for link in links:
                        if not "yahoo" in link and not link == url:
                                getsite(link,depth+1)
        except KeyboardInterrupt:
                exit()
        except Exception as e:
                return
	
        del soup
        del links
        del data
        del r
        del depth
	
	   
def getalllinks(comtent,url):
        try:
                soup = BeautifulSoup(comtent)
                links = []
                for link in soup.find_all('a'):
                        try:
                                link= link.split("#")[0]
                        except:
                                pass;
                       
                        if link == url:
                                break;
                        links.append(urljoin(url,link.get('href')))
                return links
        except Exception as e:
                print(e)
        del comtent
        del url
        del soup
#sqllite ab hier
def savedata(soup,url,depth,title):

        print("Saving")
        newps = []
        [s.extract() for s in soup(['iframe', 'script','img','style'])]
        #Create List of <p>
        ps = soup.find_all('p')
       
       
        newps = ps
       
        #Liste mit Absaetzen erzeugt.
        text = ""
        for element in newps:
               
                text += str(element)
        #String erzeugt
       
        if "Weltkrieg" not in text:
                return
               
               
        if text == "":
                return 
        #Einfügen in DB#
        if len(re.findall("Weltkrieg",text))<3:
                return
        soup = BeautifulSoup(text)
        onlytext = soup.get_text()
        db = sqlite3.connect(dbname)
        cursor = db.cursor()
       
        cursor.execute('INSERT INTO spider VALUES(?,?,?,?)',(url,depth,text,title))
       
        print("Datensatz in DB aufgenommen")
       
        db.commit()
        db.close()
        
        del soup
        del url
        del depth
        del title
#GetSQLlitedb name
def getdbname():
        Fehler = True
        dbname = ""
        while Fehler:
                try:
                        dbname = input("Name der SQL-LiteDb: ")
                        Fehler = False
                except:
                        pass
        return dbname
def createdb(dbname):
        try:
                os.remove(dbname)
        except:
                pass
        db = sqlite3.connect(dbname)
        cursor = db.cursor()
        cursor.execute("CREATE TABLE spider(url TEXT,depth INTEGER,text TEXT,title Text)")
        db.commit()
        db.close()
        #Datenbank erstellt

#Hauptprogramm
dbname = getdbname()
createdb(dbname)
try:
	
        #url ="http://www.lukol.com/s.php?q=1.Weltkrieg#gsc.tab=0&gsc.q=1.Weltkrieg&gsc.page=1"
        #r = requests.get(url)
        #data = r.text
        #soup = BeautifulSoup(data)
        #print(soup.prettify())
        #thread = []
        i = 1   
        #for link in soup.find_all('a'):
        for link in ["http://de.wikipedia.org/wiki/Erster_Weltkrieg","http://de.wikipedia.org/wiki/Chronologie_des_Ersten_Weltkrieges","http://www.dhm.de/lemo/html/wk1/","http://www.welt.de/themen/erster-weltkrieg/","http://www.dieterwunderlich.de/weltkrieg_i_03.htm","http://www.bild.de/politik/inland/erster-weltkrieg/und-jeden-tag-den-tod-vor-augen-37084120.bild.html","http://www.blz.bayern.de/blz/web/erster_weltkrieg/","http://www.erster-weltkrieg.clio-online.de/default.aspx%3Ftabid%3D40208737","http://www.zeit.de/schlagworte/themen/erster-weltkrieg/index","http://de.wikipedia.org/wiki/Erster_Weltkrieg_au%25C3%259Ferhalb_Europas","http://www.bpb.de/geschichte/deutsche-geschichte/ersterweltkrieg/","http://www.stahlgewitter.com/","http://www.der-erste-weltkrieg.com/kriegsjahr-1914.shtml","http://www.1-weltkrieg.info/1-weltkrieg-ende.htm","http://www.100-jahre-erster-weltkrieg.eu/","http://de.wikipedia.org/wiki/Schweiz_im_Ersten_Weltkrieg","http://de.wikipedia.org/wiki/Zerst%25C3%25B6rung_L%25C3%25B6wens_im_Ersten_Weltkrieg","http://www.zeit.de/2013/38/interview-erster-weltkrieg-christopher-clark-adam-krzeminski"]:
                #getsite(urljoin(url,link.get('href')),3)
                #t= Thread(target = getsite,args=(urljoin(url,link.get('href')),1))
                print(link)
                t = Thread(target = getsite,args=(link,1))
                print("Started")
                #_thread.start_new_thread(getsite,(urljoin(url,link.get('href')),3))
                t.start()
                i = i+1
except KeyboardInterrupt:
        close()
except Exception as e:
        print(e)

