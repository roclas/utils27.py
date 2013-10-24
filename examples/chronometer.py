import time,sys,math,os,thread

def openfile(file):
	os.system("eog "+file)

start=time.time()
c=0
while(True):
    c+=1
    sys.stdin.readline()
    nt=time.time()-start
    h=int(math.floor(nt/3600))
    m=int((nt-h*3600)/60.0)
    s=int(nt-h*3600-m*60)
    ms=nt-s
    file="%02d.png" % c
    print "%02d:%02d:%02d-%03d %s"%(h,m,s,ms*1000.0,file)
    thread.start_new_thread(openfile,(file,))
    
