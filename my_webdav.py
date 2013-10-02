__author__ = 'mingxiao'

import requests
import os
import base64
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def get_session(username, password):
    sess = requests.Session()
    sess.auth = (username, password)
    return sess


def download(session,filename, host, protocol='https'):
    r = session.get("{}://{}/{}".format(protocol,host,filename),stream=True)
    if r.status_code == 200:
        print 'downloading...'
        path = os.path.join(os.getcwd(),'other.jpg')
        with open(path,'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
        print 'Downloaded {} to {}'.format(filename, path)
    else:
        print 'Failed to download {}'.format(filename)


def upload(session, filePath, serverPath, host, protocol = 'https'):
    assert os.path.exists(filePath)
    with open(filePath,'rb') as fp:
        mydata = fp.read()
        response = session.put("{}://{}/{}".format(protocol,host,serverPath), data=mydata)
        if str(response.status_code).startswith('2'):
            print 'Uploaded {} to {}'.format(filePath, serverPath)
        else:
            print 'Failed to upload {}'.format(filePath)

def delete(session, filename,host,protocol='https'):
    response = session.delete("{}://{}/{}".format(protocol,host,filename))
    if str(response.status_code).startswith('2'):
        print 'Deleted {}'.format(filename)
    else:
        print 'Failed to delete {}'.format(filename)

def addFolder(session, folderPath, host, user, password, protocol = 'https'):
    #header = {"Authorization": "Basic testwebdav:password1"}
    base64string = base64.encodestring('{}:{}'.format(user, password))[:-1]
    myHeader = {"Depth": 1, "authorization":"Basic %s" % base64string}
    prepped = requests.Request('MKCOL', "{}://{}/{}".format(protocol, host,folderPath), headers=myHeader).prepare()
    print prepped.url
    response = session.send(prepped)
    print response.status_code, response.content

def ls(session, path):
    """
    We use the PROPFIND command
    """
    base64string = base64.encodestring('%s:%s' % ('testwebdav', 'password1'))[:-1]  # remove ending newline
    myHeader = {"Depth": 1, "authorization":"Basic %s" % base64string}
    prepped = requests.Request('PROPFIND', "https://webdav.o2cloud.net/%s" % path, headers = myHeader).prepare()
    response = session.send(prepped)
    if good_status(response.status_code):
        print response.content
    else:
        print 'Failed to list {}'.format(path)


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
host = 'webdav.o2cloud.net'
sess = get_session(user, password)


#download
#filename = '00546_lonelybeach_2560x1600.jpg'
#download(sess, filename, host)

#upload
#upfile = os.path.join(os.getcwd(), 'foo.txt')
#serverFile = 'somefile.txt'
#upload(sess, upfile, serverFile, host)

#delete
#filename = 'somefile.txt'
#delete(sess,filename)

#add folder
#foldername= 'my_folder'
#addFolder(sess, foldername, host, user, password)

#ls
#folder = ''
#ls(sess,folder)