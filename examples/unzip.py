#!/usr/local/bin/python
import sys, zipfile, os, os.path

def unzip_file_into_dir(file, dir):
    if not os.path.exists(dir):
    	os.makedirs(dir)
    zfobj = zipfile.ZipFile(file)
    for name in zfobj.namelist():
        if name.endswith('/'):
		dir2=os.path.join(dir, name)
    		if not os.path.exists(dir2):
            		os.makedirs(dir2)
        else:
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

def main():
    unzip_file_into_dir(open(sys.argv[1]), sys.argv[2])

if __name__ == '__main__': main()
