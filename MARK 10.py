
# coding: utf-8

# In[1]:


from tkinter import *
import sys
import sqlite3
import datetime
##import time
from time import time, sleep
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as gpio

root = Tk()

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if(f.verifyPassword() == False):
        raise ValueError("The given fingerprint sensor password is wrong!!")
except Exception as e:
    print("Excpetion message1: "+str(e))
    exit(1)

def searchFinger():
    try:
        print('Waiting for finger...')
        while( f.readImage() == False ):
            #pass
            sleep(0.5)
            return
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        accuracyScore = result[1]
        if positionNumber == -1 :
            print('No match found!')
##            lcdcmd(1)
##            lcdprint("No Match Found")
            sleep(2)
            return
        else:
            print('Found template at position #' + str(positionNumber))
            return positionNumber
##            lcdcmd(1)
##            lcdprint("Found at Pos:")
####            lcdprint(str(positionNumber))
            sleep(2)
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def registerWin():
    win1 = Tk()
    win1.title("Register")
    
    def takeVal():
        aNum = int(entry1.get())
        eName = entry2.get()
        dep = entry3.get()
        
        conn = sqlite3.connect("Records.db")
        c = conn.cursor()
    
        c.execute("SELECT COUNT(*) FROM aadhaar")
        rows = c.fetchone()
        total=rows[0]
     
        empID = aNum % 10000
    
        c.execute("SELECT Phone FROM aadhaar WHERE AadhaarNumber = :AadhaarNumber",{'AadhaarNumber':aNum})
        phNum = c.fetchall()  

        c.execute("SELECT Address FROM aadhaar WHERE AadhaarNumber = :AadhaarNumber",{'AadhaarNumber':aNum})
        add = c.fetchall()  
          
        c.execute("SELECT AadhaarNumber FROM aadhaar")
        data = c.fetchall()
    
        count=0
        for i in range(total):
            if data[i][0]==aNum:
                print("Found in the AADHAAR database")
                #eName = input("Enter your name : ")
                #dep = input("Enter your Department : ")
                c.execute("INSERT INTO empData VALUES (?,?,?,?,?,?)",(empID,eName,dep,aNum,phNum[0][0],add[0][0]))
                print("Your Employee ID = {0}".format(empID))
                que = "CREATE TABLE {0}{1} ( Date TEXT NOT NULL, inTime NUMERIC, outTime NUMERIC, inStamp INTEGER, outStamp INTEGER, Hours INTEGER, Minutes INTEGER )".format(eName,empID)
                c.execute(que)
                break
            else :
                count=count+1
                continue
        if count==total:
            print("Not found")
        conn.commit()
        c.close()
        conn.close()
    
    label1 = Label(win1,text = "Aadhaar Number")
    label2 = Label(win1,text = "Name")
    label3 = Label(win1,text = "Department")
    entry1 = Entry(win1)
    entry2 = Entry(win1)
    entry3 = Entry(win1)
    
    label1.grid(row=0,sticky=E)
    label2.grid(row=1,sticky=E)
    label3.grid(row=2,sticky=E)
    entry1.grid(row=0,column=1)
    entry2.grid(row=1,column=1)
    entry3.grid(row=2,column=1)
    
    
    
    buttonOK = Button(win1,text="OK",command=takeVal)
    buttonOK.grid(row=3,columnspan=2)
    
      
    win1.mainloop()
    
    
def attendWin():
    win2 = Tk()
    win2.title("Mark your attendance")

    def subVal():
        emp = int(entry1.get())
        eName = entry2.get()
        fingerprintValue = searchFinger()
        F2 = fingerprintValue
        
        emps = str(emp)
        
        conn = sqlite3.connect('Records.db')
        c = conn.cursor()
        query4  = "SELECT Fingerprint FROM aadhaar WHERE AadhaarNumber IN (SELECT AadhaarNum FROM empData WHERE EmpID = {0} AND Name = '{1}')".format(emp,eName)
        c.execute(query4)
        F1 = c.fetchall()
        
        if F1[0][0]==F2:
            print('Finger Print matched')

            label3 = Label(win2, text = "Attendance Marked and close the window")
            label3.grid(row=2,columnspan=3)
                        
            now = datetime.datetime.now()
            dte=now.strftime("%d %B %Y")
            query = "SELECT COUNT(*) FROM {0}{1} WHERE Date = '{2}'".format(eName,emps,dte)
            c.execute(query)
            count = c.fetchall()
            if count[0][0] == 0:
                query1 = "INSERT INTO {2}{0} (Date,inTime,inStamp) VALUES ('{1}','{3}',{4})".format(emps,dte,eName,now.time(),time())
                c.execute(query1)
            else:
                query3 = "SELECT inStamp FROM {0}{1} WHERE Date = '{2}'".format(eName,emps,dte)
                c.execute(query3)
                intime = c.fetchone()
                query2 = "UPDATE {0}{1} SET outTime='{2}',outStamp={3},Hours={4},Minutes={5} WHERE Date = '{6}'".format(eName,emps,now.time(),time(),int((time()-intime[0])//3600),int(((time()-intime[0])//60)%60),dte)
                c.execute(query2)
        else:
            print('Finger Print not found')
        conn.commit()
        c.close()
        conn.close()
        
    
    label1 = Label(win2,text = "Employee ID")
    label2 = Label(win2,text = "Name")
    
##    label3 = Label(win2,text = "Finger Print")
    entry1 = Entry(win2)
    entry2 = Entry(win2)
##    entry3 = Entry(win2)
    
    label1.grid(row=0,sticky=E)
    label2.grid(row=1,sticky=E)
##    label3.grid(row=2,sticky=E)
    entry1.grid(row=0,column=1)
    entry2.grid(row=1,column=1)
##    entry3.grid(row=2,column=1)
    
       
    buttonOK = Button(win2,text="OK",command=subVal)
    buttonOK.grid(row=3,columnspan=2)
    
    win2.mainloop()
    
    
root.title("Biometric Attendance System")
root.geometry("300x125")

label1 = Label(root, text="                           ")
label2 = Label(root, text="                            ")
button1 = Button(root,text="Register",command=registerWin)
button2 = Button(root,text="Mark Attendance",command=attendWin)

label1.grid(row=0,columnspan=3)
label1.grid(row=1,columnspan=3)
label1.grid(row=2,columnspan=3)
label2.grid(rowspan=3,column=0)
label2.grid(rowspan=3,column=1)
label2.grid(rowspan=3,column=2)
label2.grid(rowspan=3,column=3)
label2.grid(rowspan=3,column=4)
button1.grid(row=4,column=3)
button2.grid(row=5,column=3)

root.mainloop()

