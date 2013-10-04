__author__ = 'mingxiao'

import unittest
import my_webdav as mydav
import os
import requests
import qp_xml
import sys

class WebDAVTest(unittest.TestCase):

    def setUp(self):
        self.xmlstr = """<?xml version="1.0" encoding="utf-8" ?>
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
        self.smallxml = ""

        self.host = 'webdav.o2oxygencloud.net'
        self.user = 'testwebdav'
        self.password = 'password1'
        #self.session = mydav.get_session(self.user, self.password)
        self.session = requests.Session()
        self.session.auth = (self.user, self.password)
        self.dav_dir = os.path.expanduser(os.path.join('~', 'PycharmProjects', 'my_webdav_search'))

    def test_extract(self):
        parser = qp_xml.Parser()
        parser.parse(self.xmlstr)
        qp_xml.dump(sys.stdout,parser.root)
        print parser.find_prefix('D:')
        pass

    def test_good_status(self):
        self.assertTrue(mydav.good_status(201))
        self.assertTrue(mydav.good_status(207))
        self.assertFalse(mydav.good_status(301))

    def test_download(self):
        filename = '00546_lonelybeach_2560x1600.jpg'
        #session = mydav.get_session(self.user, self.password)
        downloadPath = os.path.join(self.dav_dir, filename)
        print self.session

        mydav.download(self.session, filename, self.host, downloadPath)

    def tearDown(self):
        self.session.close()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(WebDAVTest('test_extract'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    #unittest.main()