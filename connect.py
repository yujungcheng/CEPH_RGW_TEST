#!/usr/bin/python

import boto
import boto.s3.connection
import swiftclient

def get_s3_conn(access_key, secret_key, rgw_host, rgw_port=7480, secure=False):
    conn = boto.connect_s3(
           aws_access_key_id     = access_key,
           aws_secret_access_key = secret_key,
           host                  = rgw_host,
           port                  = rgw_port,
           is_secure             = secure,
           calling_format        = boto.s3.connection.OrdinaryCallingFormat(),
           )
    return conn

def get_swift_conn(user, key, authurl):
    conn = swiftclient.Connection(
           user    = user,
           key     = key,
           authurl = authurl,
           )
    return conn
