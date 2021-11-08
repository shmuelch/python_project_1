 

"""
The Questions you should answer:
What are the universities with more than one website 
Out of the last 1000 flights - Display the flights Landed from countries which are larger than 1,000,000 km² 
Out of the last 1000 flights - Show list of all flights coming from countries with more than 5 universities and that the number of flights for this country is less than 100

Hands out:
Git repository with your code and SQL
We will review your code together
"""
 
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:@localhost/project_1')
 
 
 
#What are the universities with more than one website 
sql= "SELECT name,country,web_pages from universities where web_pages > 1 "
 
df = pd.read_sql(sql, con=engine)

print("\n\n Universities with more than one website \n")
print(df)
 

 
#Out of the last 1000 flights - Display the flights Landed from countries which are larger than 1,000,000 km² 

#sql= "  select flights.*,countries.AREA from flights join countries on  (UPPER(flights.CHLOCCT)=UPPER(countries.NAME))  where CHRMINE='LANDED' and countries.AREA > 1000000 and CHFTLN in  (select  CHFTLN   from flights order by UNIX_TIMESTAMP(CHSTOL) desc limit 1000 )" 
# This version of MariaDB doesn't yet support 'LIMIT & IN/ALL/ANY/SOME subquery'


 

sql="select * from flights order by UNIX_TIMESTAMP(CHSTOL) desc limit 1000"
df = pd.read_sql(sql, con=engine)
df.to_sql(name="flights_temp", con=engine, if_exists = 'replace', index=False)
 

sql= "  select flights_temp.*,`countries`.`Area in km²` from flights_temp join countries on  (UPPER(flights_temp.CHLOCCT)=UPPER(countries.Country))    where  CHRMINE='LANDED' and `countries`.`Area in km²` > 1000000 " 
df = pd.read_sql(sql, con=engine) 

print("\n\nLast 1000 flights -  Landed from countries which are larger than 1,000,000 km² \n")

print (df)
  
 
#Out of the last 1000 flights - Show list of all flights coming from countries with more than 5 universities and that the number of flights for this country is less than 100


 

 

sql= "  select * from flights_temp    "
sql+="  where UPPER(flights_temp.CHLOCCT) in (select UPPER(country) from universities GROUP by country HAVING COUNT(country) > 5 ) "
sql+="  and flights_temp.CHLOCCT in (select CHLOCCT from  flights_temp GROUP by CHLOCCT HAVING COUNT(_id) < 100) "
 
df = pd.read_sql(sql, con=engine) 

 

print("\n\nLast 1000 flights -  coming from countries with more than 5 universities and that the number of flights for this country is less than 100 \n")

print (df)