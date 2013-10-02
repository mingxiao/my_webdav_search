__author__ = 'mingxiao'

import requests
import os
import base64
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def get_session(username, password):
    sess = requests.Session()
    sess.auth=  (username, password)
    return sess


def download(session,filename):
    r = session.get("https://webdav.o2cloud.net/%s"%filename,stream=True)
    if r.status_code == 200:
        path = os.path.join(os.getcwd(),'other.jpg')
        with open(path,'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)


def upload(session, filePath, serverFileName = None):
    assert os.path.exists(filePath)
    with open(filePath,'rb') as fp:
        mydata = fp.read()
        response = session.put("https://webdav.o2cloud.net/%s"%serverFileName, data=mydata)
        print response.status_code

def delete(session, filename):
    response = session.delete("https://webdav.o2cloud.net/%s"%filename)
    print response.status_code

def addFolder(session, folderPath):
    #header = {"Authorization": "Basic testwebdav:password1"}
    header = {}
    prepped = requests.Request('MKCOL',"https://webdav.o2cloud.net/%s" % folderPath, headers = header).prepare()
    print prepped.url
    response = session.send(prepped)
    print response.status_code, response

def ls(session,path):
    """
    We use the PROPFIND command
    """
    base64string = base64.encodestring('%s:%s' % ('testwebdav', 'password1'))[:-1]
    myHeader= {"Depth": 1, "authorization":"Basic %s" % base64string}
    prepped = requests.Request('PROPFIND', "https://webdav.o2cloud.net/%s" % path, headers = myHeader).prepare()
    response = session.send(prepped)
    print response.content
    print response.headers ,response.status_code
    root = ET.fromstring(response.content)
    namespaces = {'D': 'DAV'} # add more as needed
    #root.findall('owl:Class', namespaces=namespaces)
    for f in root.findall('{DAV}href'):
        print 'here'
        print f


xmlstr = """<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D="DAV:">
<D:response>
<D:href>/</D:href>
<D:propstat>
<D:prop>
<D:creationdate/><D:getlastmodified></D:getlastmodified>
<D:displayname></D:displayname>
<D:resourcetype>
<D:collection/></D:resourcetype>
<D:getcontenttype></D:getcontenttype>
<D:getcontentlength/><D:getetag>ff8080814170b8d00141758a9500374e</D:getetag>
</D:prop>
<D:status>HTTP/1.1 200</D:status>
</D:propstat>
</D:response>
<D:response>
<D:href>/00546_lonelybeach_2560x1600.jpg</D:href>
<D:propstat>
<D:prop>
<D:creationdate>2013-10-01T19:44:33Z</D:creationdate>
<D:getlastmodified>Tue, 01 Oct 2013 19:44:33 GMT</D:getlastmodified>
<D:displayname>00546_lonelybeach_2560x1600.jpg</D:displayname>
<D:resourcetype/><D:getcontenttype>image/jpeg</D:getcontenttype>
<D:getcontentlength>683356</D:getcontentlength>
<D:getetag>4bd84b6a-5c8f-4934-92c8-fe29a5006423_1972171177</D:getetag>
</D:prop>
<D:status>HTTP/1.1 200</D:status>
</D:propstat>
</D:response>
<D:response>
<D:href>/00559_dawninmadrid_2560x1600.jpg</D:href>
<D:propstat>
<D:prop>
<D:creationdate>2013-10-01T19:44:45Z</D:creationdate>
<D:getlastmodified>Tue, 01 Oct 2013 19:44:45 GMT</D:getlastmodified>
<D:displayname>00559_dawninmadrid_2560x1600.jpg</D:displayname>
<D:resourcetype/><D:getcontenttype>image/jpeg</D:getcontenttype>
<D:getcontentlength>993741</D:getcontentlength>
<D:getetag>81797285-9f89-4fd0-ba2f-295cd89898d3_1972182665</D:getetag>
</D:prop>
<D:status>HTTP/1.1 200</D:status>
</D:propstat>
</D:response>
<D:response>
<D:href>/Folder%20A/</D:href>
<D:propstat>
<D:prop>
<D:creationdate/><D:getlastmodified></D:getlastmodified>
<D:displayname>Folder A</D:displayname>
<D:resourcetype>
<D:collection/></D:resourcetype>
<D:getcontenttype></D:getcontenttype>
<D:getcontentlength/><D:getetag>e9da8013-497e-4b62-be70-4a2184c9e9db</D:getetag>
</D:prop>
<D:status>HTTP/1.1 200</D:status>
</D:propstat>
</D:response>
<D:response>
<D:href>/Folder%20B/</D:href>
<D:propstat>
<D:prop>
<D:creationdate/><D:getlastmodified></D:getlastmodified>
<D:displayname>Folder B</D:displayname>
<D:resourcetype>
<D:collection/></D:resourcetype>
<D:getcontenttype></D:getcontenttype>
<D:getcontentlength/><D:getetag>df572c11-4cb5-4531-a560-ea7968c877d8</D:getetag>
</D:prop>
<D:status>HTTP/1.1 200</D:status>
</D:propstat>
</D:response>
<D:response>
<D:href>/somefile</D:href>
<D:propstat>
<D:prop>
<D:creationdate>2013-10-01T23:40:38Z</D:creationdate>
<D:getlastmodified>Tue, 01 Oct 2013 23:40:38 GMT</D:getlastmodified>
<D:displayname>somefile</D:displayname>
<D:resourcetype/><D:getcontenttype>application/octet-stream</D:getcontenttype>
<D:getcontentlength>7</D:getcontentlength>
<D:getetag>0ad13a4a-3345-4afb-8ebe-43df20dbd3fe_1986336177</D:getetag>
</D:prop>
<D:status>HTTP/1.1 200</D:status>
</D:propstat>
</D:response>
</D:multistatus>
"""
def test_extract(xmlstr):
    root = ET.fromstring(xmlstr)
    #print root[1][0]
    namespaces = {'D': 'DAV'} # add more as needed
    for elem in root.iter("{DAV}href"):
        print elem
    #root.findall('owl:Class', namespaces=namespaces)
    #for f in root.findall('D:href',namespaces = namespaces):
    #    print 'here'
    #    print f
    #pass

test_extract(xmlstr)

user = 'testwebdav'
password = 'password1'
sess = get_session(user,password)


#download
#filename = '00546_lonelybeach_2560x1600.jpg'
#download(sess, filename)

#upload
#upfile = os.path.join(os.getcwd(), 'foo.txt')
#serverFile = 'somefile.txt'
#upload(sess, upfile, serverFile)

#delete
#filename = 'somefile.txt'
#delete(sess,filename)

#add folder
#foldername= 'my_folder'
#addFolder(sess,foldername)

#ls
#folder = ''
#ls(sess,folder)