__author__ = 'mingxiao'

from tinydav import WebDAVClient

host = 'webdav.o2cloud.net'
user = 'testwebdav'
password = 'password1'
protocol = 'https'
client = WebDAVClient(host, protocol=protocol)
client.setbasicauth(user, password)
client.connect('/')
response = client.mkcol('/my_folder')

