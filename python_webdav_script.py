__author__ = 'mingxiao'

import python_webdav.client
import python_webdav.connection

#f = urllib2.urlopen('https://webdav.o2cloud.net/')

#login
client_object = python_webdav.client.Client('https://webdav.o2cloud.net/')
client_object.set_connection(username='testwebdav', password='password1')

#download - WORKS
client_object.download_file('00546_lonelybeach_2560x1600.jpg', dest_path='.')

#upload
#client_object.upload_file("python_webdav_script.py",'/tmp.py')
#list - WORKS
#client_object.ls()