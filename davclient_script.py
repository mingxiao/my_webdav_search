__author__ = 'mingxiao'

import davclient

host = 'webdav.o2cloud.net'
protocol = 'https'
username = 'testwebdav'
password = 'password1'

url = '{}://{}'.format(protocol,host)

client = davclient.DAVClient(url)
client.set_basic_auth(username, password)

client.mkcol('/black')