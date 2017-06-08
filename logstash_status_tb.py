import urllib2
import json
import socket
from pylsy import pylsytable

logstash_hosts = ['127.0.0.1']
logstash_port = '9600'
jvm_url = '/_node/stats/jvm'

def toMB(num):
    return int(num)/1024/1024

def perMS(count, time_in_ms):
    return int(time_in_ms/count)

header = ['host','uptime(min)','HeapUse/Max(MB)', 'YngUse/OldUse(MB)','Yng/OldGCCount'
           ,'Yng/OldGCTime(ms)']
table = pylsytable(header)

for h in logstash_hosts:
    try:
        url = "http://" + h + ':' + logstash_port + jvm_url
        body = urllib2.urlopen(url=url, timeout=5)
        jvm_stats = json.loads(body.read())
        host = socket.gethostname() #jvm_stats['host']
        uptime = int(jvm_stats['jvm']['uptime_in_millis'])/1000/60
        mem = jvm_stats['jvm']['mem']
        gc = jvm_stats['jvm']['gc']
        pools = mem['pools']
        heapMax = toMB(mem['heap_max_in_bytes'])
        heapUsage = toMB(mem['heap_used_in_bytes'])
        heapUse = str(heapUsage) + '/' + str(heapMax)
        yngUsage = toMB(pools['young']['used_in_bytes'])
        oldUsage = toMB(pools['old']['used_in_bytes'])
        poolUse = str(yngUsage) + '/' + str(oldUsage)
        yngGCCount = gc['collectors']['young']['collection_count']
        oldGCCount = gc['collectors']['old']['collection_count']
        gcCount = str(yngGCCount) + '/' + str(oldGCCount)
        yngGCTime = perMS(yngGCCount, int(gc['collectors']['young']['collection_time_in_millis']))
        oldGCTime = perMS(oldGCCount, int(gc['collectors']['old']['collection_time_in_millis']))
        gcTime = str(yngGCTime) + '/' + str(oldGCTime)
        data = [host, uptime, heapUse, poolUse, gcCount, gcTime]
        for h,d in zip(header, data):
            table.add_data(h,d)
        print table
    except Exception, e:
        print str(e)
