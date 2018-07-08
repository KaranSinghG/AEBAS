import sqlite3
def register():
	
	# connecting to database
	conn = sqlite3.connect("Records.db")
	
	# creating a cursor
	c = conn.cursor()
    
	# counting number of rows in aadhaar table
	c.execute("SELECT COUNT(*) FROM aadhaar")
	rows = c.fetchone()
	total=rows[0]
    
	# input aadhaar number
	aNum = int(input("Enter your AADHAAR NUMBER : "))
   
	# giving a Employee ID 
	empID = aNum % 10000
    
	# fetching phone number from database
	c.execute("SELECT Phone FROM aadhaar WHERE AadhaarNumber = :AadhaarNumber",{'AadhaarNumber':aNum})
	phNum = c.fetchall()  

	#fetching address from database
	c.execute("SELECT Address FROM aadhaar WHERE AadhaarNumber = :AadhaarNumber",{'AadhaarNumber':aNum})
	add = c.fetchall()  
          
	# fetching aadhaar from database
	c.execute("SELECT AadhaarNumber FROM aadhaar")
	data = c.fetchall()
    
	# checking if such aadhaa number exists or not
	# if exists then insert an entry in employee database
	count=0
	for i in range(total):
    	if data[i][0]==aNum:
        	print("Found in the AADHAAR database")
        	eName = input("Enter your name : ")
        	dep = input("Enter your Department : ")
        	c.execute("INSERT INTO empData VALUES (?,?,?,?,?,?)",(empID,eName,dep,aNum,phNum[0][0],add[0][0]))
        	print("Your Employee ID = {0}".format(empID))
			break
    	else :
        	count=count+1
        	continue
	if count==total:
    	print("Not found")
	conn.commit()
	c.close()
	conn.close()
