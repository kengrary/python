import requests
import socket
import datetime
import json
import pytz

es_host = '127.0.0.1:9200'
index_url = '/_cat/indices'
backup_url = '/_snapshot/my_backup'
snapshot_all_url = '/_snapshot/my_backup/_all'
snapshot_url = '/_snapshot/my_backup'
include_patterns = ['app', 'mars', 'phpslow']
snapshots = []
backup_days = 10
now_date = datetime.datetime.now()
snap_shot = "snapshot" + str(now_date.date())
tz = pytz.timezone('Asia/Shanghai')
fmt = '{0:<2}{1:22}{2:22}{3}'


def list_all_dict(dict_inst):
    if isinstance(dict_inst, dict):
        for (k, v) in dict_inst.items():
            print k + ': ' + str(v)
            list_all_dict(v)


try:
    host = socket.gethostname()
    url = "http://" + es_host + snapshot_all_url
    response = requests.get(url=url, timeout=5)
    jsonData = json.loads(response.content)
    print fmt.format('#', 'Create time', 'Snapshot', 'Indices')
    print '-' * 100
    i = 1
    for snapshot in jsonData['snapshots']:
        start_time = datetime.datetime.strptime(snapshot['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        st = (start_time.replace(tzinfo=pytz.utc)).astimezone(tz)
        print fmt.format(i, st.strftime('%Y-%m-%d %H:%M:%S'),
                         snapshot['snapshot'], ', '.join(snapshot['indices']))
        i += 1
        snapshots.append(snapshot['snapshot'])
except Exception, e:
    print e.message

# print snapshots
snapshot_count = len(snapshots)
# print snapshot_count

while True:

    print ''
    choice = raw_input('Please enter the index No. or [q]uit >> ')
    if choice == 'quit' or choice == 'q':
        break
    elif choice == '':
        continue
    elif int(choice) > 0 and int(choice) <= snapshot_count:
        print 'Action: [1]Detail [2]Restore [3]Delete [4]Cancel'
        choice2 = raw_input('Please enter the action No. >> ')
        if int(choice2) == 1:
            try:
                url = "http://" + es_host + snapshot_url + '/' + snapshots[int(choice) - 1]
                response = requests.get(url)
                jsonData = json.loads(response.content)
                print json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception, e:
                print e.message
        elif int(choice2) == 2:
            try:
                url = "http://" + es_host + snapshot_url + '/' + snapshots[
                    int(choice) - 1] + '/_restore?wait_for_completion=true'
                confirm_res = raw_input('Are you sure to restore snapshot ' + snapshots[int(choice) - 1] + ' [y/n] >> ')
                if confirm_res == 'y':
                    response = requests.post(url)
                    jsonData = json.loads(response.content)
                    print json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception, e:
                print e.message
        elif int(choice2) == 3:
            try:
                url = "http://" + es_host + snapshot_url + '/' + snapshots[int(choice) - 1]
                confirm_del = raw_input('Are you sure to delete snapshot ' + snapshots[int(choice) - 1] + ' [y/n] >> ')
                if confirm_del == 'y':
                    response = requests.delete(url)
                    jsonData = json.loads(response.content)
                    print json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception, e:
                print e.message
        elif int(choice2) == 4:
            continue
