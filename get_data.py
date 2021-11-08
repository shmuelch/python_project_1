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
import pandas as pd
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
 
# FLIGHTS

url1 = 'https://data.gov.il/api/3/action/datastore_search?resource_id=e83f763b-b7d7-479e-b172-ae981ddc6de5&limit=10000'  

df = pd.read_json(url1)
all_flights=df.result.records
all_flights=pd.DataFrame(all_flights)
  


engine = create_engine('mysql+pymysql://root:@localhost/project_1')
 
all_flights.to_sql(name="flights", con=engine, if_exists = 'replace', index=False)

 
print("flights data ready")


#UNIVERSITIES
 

url1 = 'https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json'  

df = pd.read_json(url1)
all_universities=df
 
all_universities=pd.DataFrame(all_universities)
#Remove columns from dataframe
all_universities = all_universities.drop('domains', axis=1)
all_universities = all_universities.drop('alpha_two_code', axis=1)
all_universities = all_universities.drop('state-province', axis=1)

#Count websites
  
 
for index, row in all_universities.iterrows():
    all_universities.at[index,'web_pages'] = len(row['web_pages'])
    #all_universities[1]["web_pages"]=len(row['web_pages'])
 

all_universities.to_sql(name="universities", con=engine, if_exists = 'replace', index=False)
 
print("universities  data ready")      
 
#COUNTRIES
 

 
url1 = "https://www.geonames.org/countries/"
dfs = pd.read_html(url1)
 
 
all_countries = dfs[1]
 
 
 
all_countries.to_sql(name="countries", con=engine, if_exists = 'replace', index=False)

print("countries  data ready")
 
 