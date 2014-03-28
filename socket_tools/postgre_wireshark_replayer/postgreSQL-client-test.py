import pyodbc,sys
port="5432"
if(len(sys.argv)>1):port=sys.argv[1] 
connstr ='DRIVER={PostgreSQL ANSI};Server=127.0.0.1;Port='+port+';Database=test1;Uid=postgres;Pwd=postgres;'

print "about to make connection"
cnxn = pyodbc.connect(connstr)
print "connection made"

cursor = cnxn.cursor()
cursor.execute("SELECT * FROM usuarios;")
#cursor.execute("select oid, typbasetype from pg_type where typname = 'lo';")
print "query made"
for row in cursor.fetchall(): print row
print "conection about to close"
cnxn.close()
print "conection closed"
