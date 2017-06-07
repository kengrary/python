import urllib2
import json
import socket

logstash_hosts = ['127.0.0.1']
logstash_port = '9600'
jvm_url = '/_node/stats/jvm'

def toMB(num):
    return int(num)/1024/1024

def perMS(count, time_in_ms):
    return int(time_in_ms/count)

for h in logstash_hosts:
    try:
        url = "http://" + h + ':' + logstash_port + jvm_url
        body = urllib2.urlopen(url=url, timeout=5)
        jvm_stats = json.loads(body.read())
        host = socket.gethostname() #jvm_stats['host']
        uptime = int(jvm_stats['jvm']['uptime_in_millis'])/1000
        mem = jvm_stats['jvm']['mem']
        gc = jvm_stats['jvm']['gc']
        pools = mem['pools']
        heapMax = toMB(mem['heap_max_in_bytes'])
        heapUsage = toMB(mem['heap_used_in_bytes'])
        yngUsage = toMB(pools['young']['used_in_bytes'])
        oldUsage = toMB(pools['old']['used_in_bytes'])
        yngGCCount = int(gc['collectors']['young']['collection_count'])
        oldGCCount = int(gc['collectors']['old']['collection_count'])
        yngGCTime = perMS(yngGCCount, int(gc['collectors']['young']['collection_time_in_millis']))
        oldGCTime = perMS(oldGCCount, int(gc['collectors']['old']['collection_time_in_millis']))
        print '%-14s%-14s%-14s%-14s%-14s%-14s%-14s%-14s%-14s%-14s' %('host','uptime(S)','HeapUsage(MB)', 'HeapMax(MB)', 
                                                                     'YngUsage(MB)','YngGCCount','YngGCTime(MS)','OldUsage(MB)','OldGCCount','OldGCTime(MS)')
        print '%-14s%-14d%-14d%-14d%-14d%-14d%-14d%-14d%-14d%-14d' %(host, uptime, heapUsage, heapMax, 
                                                                     yngUsage, yngGCCount, yngGCTime, oldUsage, oldGCCount, oldGCTime)
    except Exception, e:
        print str(e)
