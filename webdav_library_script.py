__author__ = 'mingxiao'

import davlib
import webdav.WebdavClient as client
import os
import time


protocol = 'https'
host = 'webdav.o2cloud.net'

#login
webDAVURL = 'https://webdav.o2cloud.net'
webdavconn = client.CollectionStorer(webDAVURL, validateResourceNames=True)
webdavconn.connection.addBasicAuthorization('testwebdav', 'password1')

#create tmp_folder in root
#webdavconn.addCollection('tmp_folder')
#webdavconn.addCollection('tmp_folder')
webdavconn.connection.close()
webdavconn.connectio
time.sleep(10)

#upload ~/Downloads/classes.html into tmp_folder
path = os.path.join('~', 'Downloads', 'classes.html')
path = os.path.expanduser(path)
#uploadFile takes a file id
fid = open(path, 'rb')
#we need to change the path of the location of where we want the file to upload
webdavconn.path = '/tmp_folder/classes.html'
webdavconn.uploadFile(fid)

#move /tmp_folder/classes.html to /classes.html
webdavconn.path = '/tmp_folder/classes.html'
webdavconn.move('https://webdav.o2cloud.net/classes.html')

#update https://webdav.o2cloud.net/classes.html with ~/Downloads/bar.txt
webdavconn.path = '/classes.html'
path = os.path.join('~', 'Downloads', 'bar.txt')
path = os.path.expanduser(path)
fid = open(path, 'rb')
webdavconn.uploadFile(fid)

#download /classes.txt to ~/Downloads/downloaded.txt
path = os.path.join('~', 'Downloads', 'downloaded.txt')
path = os.path.expanduser(path)
webdavconn.downloadFile(path)

#delete file /classes.html
webdavconn.path = '/classes.html'
webdavconn.delete()
#webdavconn.deleteContent()
#webdavconn.deleteResource()

#delete tolder tmp_folder
webdavconn.path = '/tmp_folder'
webdavconn.delete()

#list collection contents
#webdavconn.path = '/'
#print webdavconn.url
#for resource, property in webdavconn.getCollectionContents():
#    print resource.path
#    print property