import requests
import socket
import datetime
import json

es_host = '127.0.0.1:9200'
index_url = '/_cat/indices'
backup_url = '/_snapshot/my_backup'
include_patterns = ['app', 'mars', 'phpslow']
backup_indices = []
backup_days = 10
now_date = datetime.datetime.now()
snap_shot = "snapshot" + str(now_date.date())
dict_indices = {}


def list_all_dict(dict_inst):
    if isinstance(dict_inst, dict):
        for (k, v) in dict_inst.items():
            print k + ': ' + str(v)
            list_all_dict(v)


def list_all_indices():
    try:
        url = "http://" + es_host + index_url
        body = requests.get(url=url, timeout=5)
        idx_stats = str(body.content).split("\n")
        print '{0:30}{1:<10}'.format('Index Name', 'Create Date')
        for idx_stat in idx_stats:
            if idx_stat != '':
                idx_items = idx_stat.split()
                for include_pattern in include_patterns:
                    if include_pattern in idx_items[2]:
                        idx_date = (idx_items[2].split('-'))[2]
                        idx_date_1 = datetime.datetime.strptime(idx_date, "%Y.%m.%d")
                        # print '{0:30}{1:<4}days ago'.format
                        dict_indices[idx_items[2]] = (now_date - idx_date_1).days
        dict_sorted_indices = sorted(dict_indices.iteritems(), key=lambda d: d[0])
        for (k, v) in dict_sorted_indices:
            print '{0:30}{1:<4}days ago'.format(k, v)
    except Exception, e:
        print e.message


def ask_for_days():
    while True:
        temp_days = raw_input(
            'Please enter the days number, indices older than the days will be backup or [c]ancel >> ')
        try:
            if temp_days == 'c':
                exit(1)
            backup_days = int(temp_days)
            break
        except Exception, e:
            continue
    return backup_days


def get_backup_indices(backup_days):
    try:
        url = "http://" + es_host + index_url
        body = requests.get(url=url, timeout=5)
        idx_stats = str(body.content).split("\n")
        for idx_stat in idx_stats:
            if idx_stat != '':
                idx_items = idx_stat.split()
                for include_pattern in include_patterns:
                    if include_pattern in idx_items[2]:
                        idx_date = (idx_items[2].split('-'))[2]
                        idx_date_1 = datetime.datetime.strptime(idx_date, "%Y.%m.%d")
                        if (now_date - idx_date_1).days >= backup_days:
                            backup_indices.append(idx_items[2])
    except Exception, e:
        print e.message
    if len(backup_indices) == 0:
        print "No indices are chosen, exit the program."
        exit(1)
    else:
        for idx in sorted(backup_indices):
            print idx
    return backup_indices


def ask_for_backup():
    while True:
        choice = raw_input('Backup these indices? [y/n] >> ')
        if choice == 'y':
            break
        elif choice == 'n':
            exit(1)
        else:
            continue


def do_backup_indices(backup_indices):
    try:
        url = 'http://' + es_host + backup_url + '/' + snap_shot + '?wait_for_completion=true'
        data = '{ "indices": "' + ','.join(backup_indices) + '"}'
        response = requests.put(url, data)
        jsonData = json.loads(response.content)
        print datetime.datetime.now()
        print json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
        # list_all_dict(jsonData)
    except Exception, e:
        print e.message

    if response.ok and jsonData['snapshot']['state'] == "SUCCESS":
        while True:
            choice = raw_input('Do you want to delete the indices ' + ', '.join(backup_indices) + ' [y/n] >> ')
            if choice == 'y':
                for index in backup_indices:
                    url = 'http://' + es_host + '/' + index
                    response = requests.delete(url)
                    if response.ok:
                        print 'Delete index {0} success.'.format(index)
                    else:
                        print 'Delete index {0} failed.'.format(index)
                break
            elif choice == 'n':
                break


if __name__ == '__main__':
    list_all_indices()
    backup_days = ask_for_days()
    backup_indices = get_backup_indices(backup_days)
    ask_for_backup()
    do_backup_indices(backup_indices)
