__author__ = 'mingxiao'

import davlib
import webdav

davlib.DAV
url = 'https://testwebdav@webdav.o2cloud.net:443/'
info = {"protocol":"https"}
my_dav = davlib.DAV(host = 'webdav.o2cloud.net', protocol='https')
my_dav.setauth('testwebdav','password1')
my_dav.connect()
response =  my_dav.propfind('/',depth =1)
print response.status
