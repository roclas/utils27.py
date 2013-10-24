#!/usr/bin/env python

import unittest
import nose
import Properties
import S3Uploader
import os

class testS3Uploader(unittest.TestCase):
    	def setup(self):
        	print ("TestUM:setup() before each test method")

    	def teardown(self):
        	print ("TestUM:teardown() after each test method")

    	@classmethod
    	def setup_class(cls):
            print ("setup_class() before any methods in this class")
            p = Properties.Properties()
	    print p
            p.load(open( os.path.dirname(os.path.realpath(__file__))+ '/../properties.properties'))
            p.list()
            credentials={ 'mybucket':[p["bucketkey"],p["bucketsecret"] ] }
            cls.uploader=S3Uploader.S3Uploader("mybucket", credentials["mybucket"],
			     #"/home/carlos/Desktop/input",
			     "/tmp",
			     "/input_pruebas_carlos_borrar/",
			     "/home/carlos/Desktop/logfile.txt"
            )

    	@classmethod
    	def teardown_class(cls):
        	print ("teardown_class() after any methods in this class")
	
		

	def test_connection_and_listing_dir(self):
       		"""
       		Test that we can connect and list a bucket.
       		"""
		local_file="dates.TXT"
		remote_file="dates.txt"
		#uploader.upload_file(local_file,remote_file)
		#uploader.download_file(local_file,remote_file)
		#uploader.download_dir("/input_pruebas_carlos_borrar/dates/acumulado/dates_month","/tmp")
		#for i in uploader.get_dirs_tree("/input_pruebas_carlos_borrar"): print i
		files_count=0
		for i in self.uploader.ls("/"): files_count+=1
		self.assertEqual((files_count>0),True)
		
       	 	#for i in range(0, 6, 2):
        	#	self.assertEqual(i % 2, 0)

	def test_connection_download_file(self):
       		"""
       		Test that we can download a file. 
       		"""
	


