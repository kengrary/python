import urllib2
import socket

es_hosts = ['127.0.0.1:9200']
index_url = '/_cat/indices'
data_units = ['kb', 'mb', 'gb']
include_patterns = ['app', 'mars', 'phpslow']
result = {'app': [0, 0, ''], 'mars': [0, 0, ''], 'phpslow': [0, 0, '']}
fmt = '{0:10}{1:20}{2:20.1f}{3:>3}'
fmt_header = '{0:10}{1:>20}{2:>23}'


def gb_to_kb(num):
    return num * 1024 * 1024


def mb_to_kb(num):
    return num * 1024


def kb_to_mb(num):
    return num / 1024


def kb_to_gb(num):
    return num / 1024 / 1024


for es_host in es_hosts:
    try:
        host = socket.gethostname()
        url = "http://" + es_host + index_url
        body = urllib2.urlopen(url=url, timeout=5)
        idx_stats = str(body.read()).split("\n")
        for idx_stat in idx_stats:
            if idx_stat != '':
                idx_items = idx_stat.split()
                for include_pattern in include_patterns:
                    if include_pattern in idx_items[2]:
                        result[include_pattern][0] += int(idx_items[6])
                        for data_unit in data_units:
                            if data_unit in idx_items[8]:
                                result[include_pattern][2] = data_unit
                                doc_size = float(idx_items[8].replace(data_unit, ''))
                                if data_unit == 'gb':
                                    doc_size = gb_to_kb(doc_size)
                                elif data_unit == 'mb':
                                    doc_size = mb_to_kb(doc_size)
                                result[include_pattern][1] += doc_size
                                # print  include_pattern, result[include_pattern][1]
        print ''
        print 'Elasticsearch host:', host
        print '-' * 55
        print fmt_header.format('Index Name', 'Doc Count', 'Store Size')
        print '-' * 55
        total_size = 0
        for pattern in include_patterns:
            doc_total_count = result[pattern][0]
            doc_total_size = result[pattern][1]
            total_size += doc_total_size
            unit = result[pattern][2]
            if unit == 'gb':
                doc_total_size = kb_to_gb(doc_total_size)
            elif unit == "mb":
                if doc_total_size > 1048576:
                    doc_total_size = kb_to_gb(doc_total_size)
                    unit = 'gb'
                else:
                    doc_total_size = kb_to_mb(doc_total_size)
            elif unit == "kb":
                if doc_total_size > 1024:
                    doc_total_size = kb_to_mb(doc_total_size)
                    unit = 'mb'
                else:
                    pass
            print fmt.format(pattern, doc_total_count, doc_total_size, unit)
        print ''
        print '-' * 55
        print '{0} {1:.2f} {2}'.format('Total Size:', kb_to_gb(total_size), 'gb')
    except Exception, e:
        print str(e)
