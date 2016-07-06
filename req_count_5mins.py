import datetime
import sys
import time

if 2 == len(sys.argv):
    access_log = sys.argv[1]
else:
    exit(1)

count = 0
now_time = datetime.datetime.now()
mins = 5

fp = open(access_log, 'rb', 5000)
try:
    for line in fp.readlines():
        req_time_tmp = time.strptime(line.split()[3].replace('[', ''), "%d/%b/%Y:%H:%M:%S")
        req_time = datetime.datetime(*req_time_tmp[:6])
        if (now_time - req_time) <= datetime.timedelta(minutes=mins):
            count += 1
    fp.close()
    print count
except Exception,e:
    print str(e)
