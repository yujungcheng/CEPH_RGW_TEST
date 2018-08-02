#!/usr/bin/python

import time
from connect import *
from dd_file import *
from math import sqrt

#----------------------------------------------------------------------------

Test_FileName           = "ddfile" 
#Test_FilePath           = "/dev/shm/" 
Test_FilePath           = "/tmp/" 
#Test_FileSize           = [16, 32, 64, 128, 256, 512, 1024, 2048] 
Test_FileSize           = [128] 
Test_Iterate            = 1 # test loop
Test_Delay_Interval     = 3 # time in second

Swift_User      = "testuser:swift"
Swift_SecretKey = "l1Uw9fLntGrf1vxYCEv3fIkQZ1PYFRyM4J3zrmrx"
Swift_AuthUrl   = "http://192.168.124.120:8080/auth"
Swift_ContainerName = "swift-test-container"

#----------------------------------------------------------------------------

def swift_upload(conn, container_name, filepath, filename):
    start_time = time.time()
    with open(filepath+filename, 'r') as fp:
        conn.put_object(container_name,
                        filename,
                        contents = fp.read(),
                        content_type=''
    spent_time = time.time() - start_time
    return '%.3f' % spent_time

def swift_download(conn, container_name, filepath, filename):
    start_time = time.time()
    
    spent_time = time.time() - start_time
    return '%.3f' % spent_time

def swift_delete():

def swift_list():

#----------------------------------------------------------------------------

if __name__ == '__main__':
    conn = get_swift_conn(user    = Swift_User,
                          key     = Swift_SecretKey,
                          authurl = Swift_AuthUrl)
   
    bucket = None
    for container in conn.get_account()[1]:
        if container['name'] == Swift_ContainerName:
            bucket = container
            break
    if bucket == None:
        conn.put_container(Swift_ContainerName)

    for size in Test_FileSize:
                
    
#    for bucket in conn.get_account()[1]:
#        print "*"+bucket['name']

    for data in conn.get_container(Swift_ContainerName)[1]:
        print '{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified'])

    conn.close()
