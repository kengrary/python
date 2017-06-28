import urllib2
import json
import socket

logstash_hosts = ['127.0.0.1']
logstash_port = '9600'
jvm_url = '/_node/stats/jvm'
pipeline_url = '/_node/stats/pipeline'


def byte_to_mb(num):
    return int(num) / 1024 / 1024


def avg_time_per_count(count, time_in_ms):
    return int(time_in_ms / count)


def avg_duration_per_count(count, time_in_ms):
    return float(time_in_ms) / float(count)


def plugins_process(process_name, processes):
    fmt = '{0:14}{1:>14}{2:>30}{3:>30}'
    fmt_float = '{0:14}{1:>14}{2:>30}{3:>30.2f}'
    print fmt.format(process_name, 'EventCount', 'EventTotalDuration(ms)', 'EventAvgDuration(ms)')
    print '-' * 108
    for process in processes:
        p = process['events']
        p_avg_duration = avg_duration_per_count(p['in'], p['duration_in_millis'])
        print fmt_float.format(process['name'], p['in'], p['duration_in_millis'],
                               p_avg_duration)
    print ''


for h in logstash_hosts:
    fmt = '{0:14}{1:>14}{2:>20}{3:>20}{4:>20}{5:>20}'
    try:
        url = "http://" + h + ':' + logstash_port + jvm_url
        body = urllib2.urlopen(url=url, timeout=5)
        jvm_stats = json.loads(body.read())
        host = socket.gethostname()  # jvm_stats['host']
        uptime = int(jvm_stats['jvm']['uptime_in_millis']) / 1000 / 60
        mem = jvm_stats['jvm']['mem']
        gc = jvm_stats['jvm']['gc']
        pools = mem['pools']
        heapMax = byte_to_mb(mem['heap_max_in_bytes'])
        heapUsage = byte_to_mb(mem['heap_used_in_bytes'])
        heapUse = str(heapUsage) + '/' + str(heapMax)
        yngUsage = byte_to_mb(pools['young']['used_in_bytes'])
        oldUsage = byte_to_mb(pools['old']['used_in_bytes'])
        poolUse = str(yngUsage) + '/' + str(oldUsage)
        yngGCCount = gc['collectors']['young']['collection_count']
        oldGCCount = gc['collectors']['old']['collection_count']
        gcCount = str(yngGCCount) + '/' + str(oldGCCount)
        yngGCTime = avg_time_per_count(yngGCCount, int(gc['collectors']['young']['collection_time_in_millis']))
        oldGCTime = avg_time_per_count(oldGCCount, int(gc['collectors']['old']['collection_time_in_millis']))
        gcTime = str(yngGCTime) + '/' + str(oldGCTime)
        print ''
        print fmt.format('Host', 'Uptime(min)', 'HeapUse/Max(MB)', 'Yng/OldUse(MB)', 'Yng/OldGCCount',
                         'Yng/OldGCTime(ms)')
        print '-' * 108
        print fmt.format(host, uptime, heapUse, poolUse, gcCount, gcTime)
        print ''
    except Exception, e:
        print str(e)

for h in logstash_hosts:
    fmt = '{0:14}{1:>14}{2:>30}{3:>30}'
    fmt_float = '{0:14}{1:>14}{2:>30}{3:>30.2f}'
    try:
        url = "http://" + h + ':' + logstash_port + pipeline_url
        body = urllib2.urlopen(url=url, timeout=5)
        pipeline_stats = json.loads(body.read())
        host = socket.gethostname()
        events = pipeline_stats['pipeline']['events']
        plugins = pipeline_stats['pipeline']['plugins']
        events_count = events['in']
        events_total_duration = events['duration_in_millis']
        events_avg_duration = avg_duration_per_count(events_count, events_total_duration)
        filters = plugins['filters']
        outputs = plugins['outputs']
        print ''
        print fmt.format('Host', 'EventCount', 'EventTotalDuration(ms)', 'EventAvgDuration(ms)')
        print '-' * 108
        print fmt_float.format(host, events_count, events_total_duration, events_avg_duration)
        print ''
        plugins_process('Filter', filters)
        plugins_process('Output', outputs)
    except Exception, e:
        print str(e)
