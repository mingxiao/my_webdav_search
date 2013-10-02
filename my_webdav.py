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


def download(session,filename, host, downloadPath, protocol='https'):
    r = session.get("{}://{}/{}".format(protocol,host,filename),stream=True)
    if r.status_code == 200:
        print 'downloading...'
        #path = os.path.join(os.getcwd(),'other.jpg')
        with open(downloadPath,'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
        print 'Downloaded {} to {}'.format(filename, downloadPath)
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
    if good_status(response.status_code):
        print 'Deleted {}'.format(filename)
    else:
        print 'Failed to delete {}'.format(filename)

def addFolder(session, folderPath, host, user, password, protocol = 'https'):
    base64string = base64.encodestring('{}:{}'.format(user, password))[:-1]
    myHeader = {"Depth": 1, "authorization":"Basic %s" % base64string}
    prepped = requests.Request('MKCOL', "{}://{}/{}".format(protocol, host,folderPath), headers=myHeader).prepare()
    response = session.send(prepped)
    if good_status(response.status_code):
        print 'Successfully created folder {}'.format(folderPath)
    else:
        print 'Failed to create folder {}'.format(folderPath)

def ls(session, path, host, protocol = 'https'):
    """
    We use the PROPFIND command
    """
    base64string = base64.encodestring('%s:%s' % ('testwebdav', 'password1'))[:-1]  # remove ending newline
    myHeader = {"Depth": 1, "authorization":"Basic %s" % base64string}
    prepped = requests.Request('PROPFIND', "{}://{}/{}".format(protocol, host, path), headers = myHeader).prepare()
    response = session.send(prepped)
    if good_status(response.status_code):
        print response.content
    else:
        print 'Failed to list {}'.format(path)

def move(session, src, dest, host, protocol = 'https'):
    prepped_src = os.path.join('{}://{}/'.format(protocol,host),src)
    prepped_dest = os.path.join('{}://{}/'.format(protocol,host),dest)
    myHeader = {"Destination":prepped_dest, "Host":host}
    prepped = requests.Request('MOVE', prepped_src, headers = myHeader).prepare()
    response = session.send(prepped)
    if good_status(response.status_code):
        print 'Successfully moved {} to {}'.format(src, dest)
    else:
        print 'Failed to move {} to {}'.format(src, dest)


def good_status(status_code):
    """
    Return true if the status code is acceptable
    """
    return str(status_code).startswith('2')


def extract(xmlstr, np, tag):
    root = ET.fromstring(xmlstr)
    for f in root.findall(tag, namespaces=np):
        print 'here'
        print f


if __name__ == '__main__':
    user = 'testwebdav'
    password = 'password1'
    host = 'webdav.o2cloud.net'
    sess = get_session(user, password)

    #download - file
    #filename = '00546_lonelybeach_2560x1600.jpg'
    #downPath = os.path.join(os.getcwd(),filename)
    #download(sess, filename, host, downPath)

    #upload
    #upfile = os.path.join(os.getcwd(), 'foo.txt')
    #serverFile = 'somefile.txt'
    #upload(sess, upfile, serverFile, host)

    #delete - file
    #filename = 'somefile'
    #delete(sess, filename, host)

    #add folder
    #foldername= 'my_folder'
    #addFolder(sess, foldername, host, user, password)

    #delete - folder
    #folder_name = 'my_folder'
    #delete(sess,folder_name, host)

    #ls
    #folder = ''
    #ls(sess,folder, host)

    #move
    src = '/somefile.txt'
    dest = '/my_folder'
    move(sess, src, dest, host)