"""

Prerequisites: 
Notebook with python and access to SQL database 
 

Assumptions:
The test is limited to one hour, so like a pro in real life, priorities and ask questions if you need.

The mission 
You are requested to get data from the web (flight, counties, universities info).  Load it to a database of your choice and perform 3 queries on the data you loaded.

Data Sources:
Countries list and details: https://www.geonames.org/countries/
Israel flight information : https://data.gov.il/dataset/flydata/resource/e83f763b-b7d7-479e-b172-ae981ddc6de5
Universities Names and domains data:
https://github.com/Hipo/university-domains-list 
The Task:
Load the data you retrieve to the database preferably by using python code 
Answer the following questions by at least 2 of them should be by using SQL

The Questions you should answer:
What are the universities with more than one website 
Out of the last 1000 flights - Display the flights Landed from countries which are larger than 1,000,000 km² 
Out of the last 1000 flights - Show list of all flights coming from countries with more than 5 universities and that the number of flights for this country is less than 100

Hands out:
Git repository with your code and SQL
We will review your code together
"""



import urllib.request
import json

from connect_db import *

# FLIGHTS

# empty table flights
mycursor = mydb.cursor()
mycursor.execute("TRUNCATE TABLE flights")

 

url1 = 'https://data.gov.il/api/3/action/datastore_search?resource_id=e83f763b-b7d7-479e-b172-ae981ddc6de5&limit=10000'  

with urllib.request.urlopen(url1) as url:
    s = url.read()

y = json.loads(s)


 
 

all_flights="["
comma=""
for z in y["result"]["records"]:
    if z["CHLOCCT"] !="" and z["CHRMINE"]!="":
       all_flights+=comma+ "('" + str(z["_id"]) +  "', '" + z["CHOPER"]  +  "', '" + z["CHFLTN"]  +  "', '" + z["CHSTOL"]   + "', '" + z["CHLOCCT"]  + "', '" + z["CHRMINE"]+ "')"
       comma=","    
      
all_flights+="]" 

 
all_flights=eval(all_flights) # convert string to list of tuples
 
 



sql = "INSERT INTO flights (_id,CHOPER,CHFLTN,CHSTOL,CHLOCCT, CHRMINE) VALUES (%s, %s, %s, %s, %s, %s)"
 

mycursor.executemany(sql, all_flights)

mydb.commit()

print("flights data ready")


#UNIVERSITIES

# empty table universities


mycursor.execute("TRUNCATE TABLE universities")



url1 = 'https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json'  

with urllib.request.urlopen(url1) as url:
    s = url.read()
    
y = json.loads(s)

  

all_universities="["
comma=""
 
for z in y:
    if z["country"] !="" and z["name"]!="":

       u_name=z["name"].replace('“', '')
       u_name=u_name.replace('”', '')
       u_name=u_name.replace("'", '')
       country=z["country"].replace("'", '')
       all_universities+=comma+ "('" + country + "', '" +  u_name  + "', "+ str(len(z["web_pages"]))+")"
       comma="," 
       
      
all_universities+="]"   

 
 
 
all_universities=eval(all_universities) # convert string to list of tuples
 



sql = "INSERT INTO universities (COUNTRY,NAME,WEB_PAGES) VALUES (%s, %s, %s)"
 

mycursor.executemany(sql, all_universities)

mydb.commit()
 
print("universities  data ready")      
 
#COUNTRIES
 

# empty table countries


mycursor.execute("TRUNCATE TABLE countries") 

url1 = "https://www.geonames.org/countries/"

with urllib.request.urlopen(url1) as url:
    s = url.read()

s =s.decode('UTF-8')

s=s.split('Continent</th></tr>')
s=s[1]

s=s.split('</table>')
s=s[0]

s=s.split('<tr')
first=1
all_countries="["
comma=""
for z in s:
    if first==1:
        first=0
        continue
    z=z.split('<td')
    
    country=z[5]
    country=country.split('.html">')
    country=country[1]
    country=country.split('</a>')
    country=country[0]
    area=z[7]
    area=area.split('">')
    area=area[1]
    area=area.split('</td>')
    area=area[0]
    
    area=area.replace(",","")


        
    if country!="":
        all_countries+=comma+ "('" + country + "', " + area + ")"
        comma=","    
    
    
all_countries+="]" 


all_countries=eval(all_countries) # convert string to list of tuples





sql = "INSERT INTO countries (NAME,AREA) VALUES ( %s, %s)"


mycursor.executemany(sql, all_countries)

mydb.commit()

print("countries data ready")
    
   
mydb.close()    
   