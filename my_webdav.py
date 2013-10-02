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
        print 'Downloaded {} to {}'.format(filename, path)
    else:
        print 'Failed to download {}'.format(filename)


def upload(session, filePath, serverFileName = None):
    assert os.path.exists(filePath)
    with open(filePath,'rb') as fp:
        mydata = fp.read()
        response = session.put("https://webdav.o2cloud.net/%s"%serverFileName, data=mydata)
        if str(response.status_code).startswith('2'):
            print 'Uploaded {} to {}'.format(filePath, serverFileName)
        else:
            print 'Failed to upload {}'.format(filePath)

def delete(session, filename):
    response = session.delete("https://webdav.o2cloud.net/%s"%filename)
    if str(response.status_code).startswith('2'):
        print 'Deleted {}'.format(filename)
    else:
        print 'Failed to delete {}'.format(filename)

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


def good_status(status_code):
    """
    Return true if the status code is acceptable
    """
    return str(status_code).startswith('2')


def extract(xmlstr, np, tag):
    root = ET.fromstring(xmlstr)
    for f in root.findall(tag, namespaces= np):
        print 'here'
        print f


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