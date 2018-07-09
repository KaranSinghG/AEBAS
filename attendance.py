import sqlite3
import datetime
import time

def attendance():
    
    # inputs
    emp = int(input("Enter Employee ID : "))
    emps = str(emp)
    eName = input("Enter name : ")
    
    # creating connection between database & program
    conn = sqlite3.connect('Records.db')
    c = conn.cursor()
    
    # select fingerprint
    query4  = "SELECT Fingerprint FROM aadhaar WHERE AadhaarNumber IN (SELECT AadhaarNum FROM empData WHERE EmpID = {0} AND Name = '{1}')".format(emp,eName)
    c.execute(query4)
    F1 = c.fetchall()
    F2 = str(input("Enter Finger Print : "))
    
    # check fingerprint
    if F1[0][0]==F2:
        print('Finger Print matched')
        now = datetime.datetime.now()
        dte=now.strftime("%d %B %Y")
        query = "SELECT COUNT(*) FROM {0}{1} WHERE Date = '{2}'".format(eName,emps,dte)
        c.execute(query)
        count = c.fetchall()
        if count[0][0] == 0:
            query1 = "INSERT INTO {2}{0} (Date,inTime,inStamp) VALUES ('{1}','{3}',{4})".format(emps,dte,eName,now.time(),time.time())
            c.execute(query1)
        else:
            query3 = "SELECT inStamp FROM {0}{1} WHERE Date = '{2}'".format(eName,emps,dte)
            c.execute(query3)
            intime = c.fetchone()
            query2 = "UPDATE {0}{1} SET outTime='{2}',outStamp={3},Hours={4},Minutes={5} WHERE Date = '{6}'".format(eName,emps,now.time(),time.time(),int((time.time()-intime[0])//3600),int(((time.time()-intime[0])//60)%60),dte)
            c.execute(query2)
    else:
        print('Finger Print not found')
    conn.commit()
    c.close()
    conn.close()
