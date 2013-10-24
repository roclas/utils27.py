#!/usr/local/bin/python
import os

def ensure_dir(tree,prefix):
	for i in tree.keys():
		newprefix=prefix+"/"+i
    		if not os.path.exists(newprefix):
			os.makedirs(newprefix)
		if(type(tree[i]) is dict):
			ensure_dir(tree[i],newprefix)

"""
dir_tree={
	"web":{
		"a":None,
		"b":{"one":None,"twoo":None},
		"c":None,
		"d":None
	}
}
	
ensure_dir(dir_tree,".");
"""
