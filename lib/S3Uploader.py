#!/usr/bin/env python

import sys
import os
import logging
import boto
import Properties
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Uploader:
	"""Class to upload files to S3"""
		
	def percent_cb(self,complete, total):
		logging.info( '.' )
    		sys.stdout.write('.')
    		sys.stdout.flush()

	def upload_file(self,local_file,remote_file):
		if not (self.connection): self.connect()
		if(not (local_file.startswith("/"))):local_file=self.local_dir+"/"+local_file;
		if(not (remote_file.startswith("/"))):remote_file=self.remote_dir+"/"+remote_file;
		self.k.key=remote_file
		logging.info( 'Uploading %s to S3 bucket %s, %s -> %s' % (self.k.key, self.bucketname,local_file,remote_file) )
                self.k.set_contents_from_filename(local_file, cb=self.percent_cb, num_cb=10)

	def download_file(self,local_file,remote_file):
		if not (self.connection): self.connect()
		if(not (local_file.startswith("/"))): local_file=self.local_dir+"/"+local_file
		if(not (remote_file.startswith("/"))):remote_file=self.remote_dir+"/"+remote_file
		logging.info( 'Downloading %s from S3 bucket %s, %s <- %s' % (self.k.key, self.bucketname,local_file,remote_file) )
		try:
		 for f in self.ls("/"+remote_file.strip("/")):f.get_contents_to_filename(local_file)#there will only be one file
		except:
		 logging.info( 'cannot download %s from S3 bucket %s, %s <- %s' % (self.k.key, self.bucketname,local_file,remote_file) )
			

	def download_dir(self,local_dir,remote_dir,recursive=True):
		if not (self.connection): self.connect()
		if(not (local_dir.startswith("/"))): local_dir=self.local_dir+"/"+local_dir;
		if(not (remote_dir.startswith("/"))): remote_dir=self.remote_dir+"/"+remote_dir;
		for i in self.ls("/"+remote_dir.strip("/")):
			try:
				logging.info( 'Downloading %s from S3 bucket %s' % (i.key, self.bucketname) )
				i.get_contents_to_filename(local_dir+"/"+i.key.split("/")[-1])
			except:
				logging.info( 'Cannot download file %s from S3 bucket %s, %s <- %s' % (i.key, self.bucketname,local_dir,remote_dir) )
			
	def lsprefix(self,remote_dir,pref):
		if not (self.connection): self.connect()
		if(remote_dir.startswith("/")): remote_files=self.bucket.list(remote_dir.strip("/"),prefix=pref)
		else:remote_files=self.bucket.list("/"+(self.remote_dir+"/"+remote_dir).strip("/"),prefix=pref)
		return remote_files


	def ls(self,remote_dir):
		if not (self.connection): self.connect()
		if(remote_dir.startswith("/")): remote_files=self.bucket.list(remote_dir.strip("/"))
		else:remote_files=self.bucket.list("/"+(self.remote_dir+"/"+remote_dir).strip("/"))
		return remote_files

	def get_dirs_tree(self,remote_dir):
		tree={}
		for i in self.ls(remote_dir):
			for j in reduce(lambda x,y:x+[x[len(x)-1]+"/"+y], i.key.split("/"), [""])[1:-1]:
				tree[j]=True
		return sorted(tree.keys())

	def connect(self):
		self.connection = S3Connection(self.credentials[0],self.credentials[1])
		rs = self.connection.get_all_buckets()
		bucket=""
		for b in rs:
        		if (b.name==self.bucketname):
				self.bucket=b
				logging.info("my bucket is %s\n" % (self.bucketname))

		self.k = Key(self.bucket)
		
	def __init__(self,bucketname,credentials,localdir,remotedir,logfile):
		logging.basicConfig(filename=logfile,level=logging.DEBUG)
		self.credentials=credentials
		self.bucketname=bucketname
		self.errors=[]
		self.local_dir=localdir
		self.remote_dir=remotedir 
		self.connection=False
		self.bucket=False
		
		
if __name__ == '__main__': 
	p = Properties.Properties()
	p.load(open( os.path.dirname(os.path.realpath(__file__))+ '/properties.properties'))
	p.list()
	credentials={ 'mybucket':[p['bucketkey'],p['bucketsecret'] ] }
	uploader=S3Uploader("mybucket", credentials["mybucket"], "/home/carlos/Desktop/input/data", "/borrar/aeiou", "/home/carlos/Desktop/logS3UploaderBorrar.txt")
	local_file="a.TXT"
	remote_file="b.txt"
	uploader.ls("/")
	#uploader.upload_file(local_file,remote_file)
	#uploader.download_file(local_file,remote_file)
	
