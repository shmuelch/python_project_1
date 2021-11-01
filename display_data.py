 

"""
The Questions you should answer:
What are the universities with more than one website 
Out of the last 1000 flights - Display the flights Landed from countries which are larger than 1,000,000 km² 
Out of the last 1000 flights - Show list of all flights coming from countries with more than 5 universities and that the number of flights for this country is less than 100

Hands out:
Git repository with your code and SQL
We will review your code together
"""
 
from connect_db import *

#What are the universities with more than one website 
sql= "SELECT NAME,COUNTRY,WEB_PAGES from universities where WEB_PAGES > 1 "
 


mycursor = mydb.cursor()

mycursor.execute(sql)

myresult = mycursor.fetchall()

 

print("\n\nUniversities with more than one website \n") 
print ("{:<50} {:<25} {:<10}".format('University','Country','Websites'))

for x in myresult:
    university, country, websites = x
    print ("{:<50} {:<25} {:<10}".format( university, country, websites))


 
#Out of the last 1000 flights - Display the flights Landed from countries which are larger than 1,000,000 km² 

#sql= "  select flights.*,countries.AREA from flights join countries on  (UPPER(flights.CHLOCCT)=UPPER(countries.NAME))  where CHRMINE='LANDED' and countries.AREA > 1000000 and CHFTLN in  (select  CHFTLN   from flights order by UNIX_TIMESTAMP(CHSTOL) desc limit 1000 )" 
# This version of MariaDB doesn't yet support 'LIMIT & IN/ALL/ANY/SOME subquery'


mycursor.execute("TRUNCATE TABLE flights_temp")

sql="insert into flights_temp (select * from flights order by UNIX_TIMESTAMP(CHSTOL) desc limit 1000 )"

mycursor.execute(sql)
mydb.commit()

 

sql= "  select flights_temp.*,countries.AREA from flights_temp join countries on  (UPPER(flights_temp.CHLOCCT)=UPPER(countries.NAME))    where  CHRMINE='LANDED' and AREA > 1000000 " 
mycursor.execute(sql)

myresult = mycursor.fetchall()

print("\n\nLast 1000 flights -  Landed from countries which are larger than 1,000,000 km² \n")

print ("{:<10}{:<40}{:<20}{:<40}{:<10}{:<10}".format('Id','Flight number',"Date",'Country','Status','Area'))

for x in myresult:
    id,number1,number2, date,country,status,area  = x
    print ("{:<10}{:<20}{:<20}{:<20}{:<40}{:<10}{:<10}".format(id, number1,number2, date,country,status,area))

 
#Out of the last 1000 flights - Show list of all flights coming from countries with more than 5 universities and that the number of flights for this country is less than 100


mycursor.execute("TRUNCATE TABLE flights_temp")

sql="insert into flights_temp (select * from flights order by UNIX_TIMESTAMP(CHSTOL) desc limit 1000 )"

mycursor.execute(sql)
mydb.commit()

 

sql= "  select * from flights_temp    "
sql+="  where UPPER(flights_temp.CHLOCCT) in (select UPPER(COUNTRY) from universities GROUP by COUNTRY HAVING COUNT(COUNTRY) > 5 ) "
sql+="  and flights_temp.CHLOCCT in (select CHLOCCT from  flights_temp GROUP by CHLOCCT HAVING COUNT(_id) < 100) "
 
mycursor.execute(sql)

myresult = mycursor.fetchall()

print("\n\nLast 1000 flights -  coming from countries with more than 5 universities and that the number of flights for this country is less than 100 \n")

print ("{:<10}{:<40}{:<20}{:<40}{:<10} ".format('Id','Flight number',"Date",'Country','Status'))

for x in myresult:
    id,number1,number2, date,country,status  = x
    print ("{:<10}{:<20}{:<20}{:<20}{:<40}{:<10}".format(id, number1,number2, date,country,status))


mydb.close()    