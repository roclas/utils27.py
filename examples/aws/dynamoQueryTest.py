#from boto.dynamodb2.fields import HashKey
import boto
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item

conn=boto.dynamodb2.connect_to_region('eu-west-1')

#conn.list_tables()
results1=conn.scan("AllRelationshipByMonth",limit=5)
results2=conn.scan("AllRelationshipByMonth",limit=5)
#results 1 and results 2 are the same
results3=conn.scan("AllRelationshipByMonth",limit=5,exclusive_start_key=results1['LastEvaluatedKey'])

