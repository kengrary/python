import httplib
import sys
import getopt
import base64
import time

total_servers = 0
error_servers = 0
good_servers = 0


def getweb(host,server,port,url,checkstr):
    global total_servers,error_servers,good_servers
    total_servers += 1
    try:
        auth = base64.b16encode("wasdmin:wasadmin")
        httpClient = httplib.HTTPConnection(host,port,timeout=10)
        httpClient.putrequest('GET',url)
        httpClient.putheader("Authorization","Basic " + auth)
        httpClient.endheaders()
        t1=time.time()
        resp = httpClient.getresponse()
        t2=time.time()
        body=resp.read()
        http_code = int(resp.status)
        idx_checkstr = body.find(checkstr)
        if(http_code != 200 and idx_checkstr < 0):
            error_servers += 1
            print "%-16s%-24s%-10s%-20s" % (host,server,port,'\033[1;33;40mFail RC: ' + str(http_code) + '\033[0m')
        else:
            good_servers +=1
            print "%-16s%-24s%-10s%-20s%18.2f" % (host, server, port, '\033[1;32;40mPass\033[0m',(t2-t1))
    except Exception,e:
        error_servers +=1
        print "%-16s%-24s%-10s%-20s" % (host, server, port, '\033[1;31;40m' + str(e) + '\033[0m')
    finally:
        if(httpClient):
            httpClient.close()


def checkweb():
    print "Check WebServer"
    print "%-16s%-24s%-10s%-20s%-16s" % ("HostName","WebServer","Port","Status","ResponseTime")
    f=open(iniFile,'r')
    for line in f:
        if(len(line)>2):
            line_list = line.split('|')
            product = line_list[0]
            host = line_list[1]
            server = line_list[2]
            port = line_list[3]
            url = line_list[4]
            checkstr = line_list[5].strip('\n')
            if(product == 'web'):
                getweb(host,server,port,url,checkstr)
    f.close()


def checkwas():
    print "Check WasServer"
    print "%-16s%-24s%-10s%-20s%-16s" % ("HostName","WasServer","Port","Status","ResponseTime")
    f=open(iniFile,'r')
    for line in f:
        if(len(line)>2):
            line_list = line.split('|')
            product = line_list[0]
            host = line_list[1]
            server = line_list[2]
            port = line_list[3]
            url = line_list[4]
            checkstr = line_list[5].strip('\n')
            if(product == 'was'):
                getweb(host,server,port,url,checkstr)
    f.close()

iniFile = '/home/ibm_admin/ibm/CheckWAS.ini'

try:
    opts,args = getopt.getopt(sys.argv[1:],'wj')
    if(len(opts) == 0):
        checkweb()
        checkwas()

    for opt,value in opts:
        if opt == '-w':
            checkweb()
        elif opt == '-j':
            checkwas()
except:
    print "Error"