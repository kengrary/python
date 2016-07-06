import os
import sys


def process(access_log):
    top_n = 10
    total_req_count = 0
    total_res_time = 0
    ip_addr_dict = {}
    rc_dict = {}
    rc_500_dict = {}
    slow_req_time_list = [""] * top_n
    slow_res_time_list = [""] * top_n
    slow_url_list = [""] * top_n

    fp = open(access_log, 'rb', 5000)
    try:
        for line in fp.readline():
            line_list = line.split()
            ip_addr = line_list[0]
            req_time = line_list[3].replace('[', '')
            url = line_list[6]
            rc = line_list[8]
            res_time = float(line_list[10]) / (1000 * 1000)

            total_req_count += 1
            total_res_time += res_time

            for i in range(top_n):
                if res_time > slow_res_time_list[i]:
                    slow_req_time_list[i] = req_time
                    slow_res_time_list[i] = res_time
                    slow_url_list[i] = url
                    break
            if ip_addr_dict.has_key(ip_addr):
                ip_addr_dict[ip_addr] += 1
            else:
                ip_addr_dict[ip_addr] = 1

            if rc_dict.has_key(rc):
                rc_dict[rc] += 1
            else:
                rc_dict[rc] = 1

            if rc == 500:
                if rc_500_dict.has_key(url):
                    rc_500_dict[url] += 1
                else:
                    rc_500_dict[url] = 1

        if total_req_count > 0:
            avg_res_time = total_res_time / total_req_count

            print "Result of process access log file : %s" % access_log
            print ""
            print "Average response time : %.3f" % avg_res_time
            print ""
            print "Total request count : %d" % total_req_count
            print ""
            print "Client IP stats : "
            for f, v in ip_addr_dict.items():
                print "%s %d" % (f, v)
            print ""
            print "HTTP code stats : "
            for f, v in rc_dict.items():
                print "%s %d" % (f, v)
            print ""
            print "HTTP code 500 urls : "
            for f, v in rc_500_dict.items():
                print "%s %d" % (f, v)
            print ""
            print "Top %d slow process url : " % (top_n)
            for i in range(top_n):
                print "%.3f %s %s" % (float(slow_res_time_list[i]), slow_req_time_list[i], slow_url_list[i])
        else:
            print "Total request count is 0."
        fp.close()
    except Exception, e:
        print e

access_log_file=""
if len(sys.argv) == 2:
    access_log_file = sys.argv[1]
else:
    print "Usage: %s filename." % (sys.argv[0])
    exit(1)

if os.path.isfile(access_log_file):
    process(access_log_file)
elif os.path.isdir(access_log_file):
    print "\"%s\" is a directory, please give a file." % access_log_file
else:
    print "File \"%s\" is not exists." % access_log_file
    exit(1)
