__author__ = 'mingxiao'

import easywebdav
import os

host = 'webdav.o2cloud.net'
user = 'testwebdav'
my_password = 'password1'

webdav = easywebdav.connect(host, username = user, password =   my_password,protocol = 'https')

#webdav.ls('/')
path = os.path.join(os.getcwd(),'tmp.jpg')
webdav.download('00546_lonelybeach_2560x1600.jpg',path)