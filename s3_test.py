#!/usr/bin/python

import time
from connect import *
from dd_file import *
from math import sqrt

#----------------------------------------------------------------------------

Test_FileName           = "ddfile" # local file name
Test_FilePath           = "/tmp/" # local file path
Test_FileSize           = [16, 32] # size in MB
Test_Iterate            = 1 # test loop
Test_Delay_Interval     = 3 # time in second

S3_RgwHost              = "172.20.3.63"
S3_RgwPort              = 7480
S3_AccessKey            = "6333TG5E6YC9RYVSPIUA"
S3_SecretKey            = "gcCoGTWMR9PYOkfdUhdhbJDHlBqGmu5Z9wxQ3h6D"
S3_BucketName           = "s3-test-bucket"

#----------------------------------------------------------------------------

def s3_upload(key, localfile):
    start_time = time.time()
    key.set_contents_from_filename(localfile)
    spent_time = time.time() - start_time
    return '%.3f' % spent_time

def s3_upload2(key, localfile, size):
    with open(localfile, 'rb') as fp:
      start_time = time.time()
      key.set_contents_from_file(fp, size=size)
      spent_time = time.time() - start_time
    return '%.3f' % spent_time
    

def s3_download(key, localfile):
    start_time = time.time()
    key.get_contents_to_filename(localfile)
    spent_time = time.time() - start_time
    return '%.3f' % spent_time

def s3_delete(key, bucket):
    bucket.delete_key(key)
    for bucket_key in bucket.list():
        if bucket_key.name == key:
            return False
    return True

def s3_list(bucket):
    key_list=[]
    for key in bucket.list():
        print "{name} {size} {modified}".format(
                                         name     = key.name,
                                         size     = key.size,
                                         modified = key.last_modified,)
        key_meta={'name':key.name,'size':key.size,'modified':key.last_modified}
        key_list.append(key_meta)
    return key_list

def statistics_calc(value_list):
    list_sum = 0
    list_len = len(value_list)
    for value in value_list:
        list_sum += float(value)
    mean_value = list_sum/list_len

    sorted_list = sorted(value_list)
    index = (list_len - 1) // 2
    if (list_len % 2):
        median_value = sorted_list[index]
    else:
        median_value = (sorted_list[index]+sorted_list[index+1]) / 2

    variance = sum([(float(e) - mean_value)**2 for e in value_list])
    sd_value = sqrt(variance)

    print("  "+"-"*48)
    print "  Mean Value         : " + str('%.3f' % mean_value)
    print "  Median Value       : " + str('%.3f' % median_value)
    print "  Standard Deviation : " + str('%.3f' % sd_value)
    print ""
    return {'mean':mean_value, 'median':median_value, 'sd':sd_value}

def print_test_info():
    print("\nTest File Uploading/Downloading, Test Iteration: %s"%Test_Iterate)
    print("  *File size      = %s in MB" % Test_FileSize)
    print("  *File path      = %s" % Test_FilePath)
    print("  *File name      = %s" % Test_FileName)
    print("  *S3 Rgw Host    = %s" % S3_RgwHost)
    print("  *S3 Rgw Port    = %s" % S3_RgwPort)
    print("  *S3 Bucket Name = %s" % S3_BucketName)
    print("  *S3 AccessKey   = %s" % S3_AccessKey)
    print("  *S3 SecretKey   = %s" % S3_SecretKey)
    print("="*50)

#----------------------------------------------------------------------------

if __name__ == '__main__':
    ########################################
    ## create s3 connection to radosgw
    ########################################
    conn = get_s3_conn(access_key = S3_AccessKey,
                       secret_key = S3_SecretKey,
                       rgw_host   = S3_RgwHost,
                       rgw_port   = S3_RgwPort)

    ########################################
    ## set bucket
    ########################################
    if conn.__contains__(S3_BucketName):
        bucket = conn.get_bucket(S3_BucketName)
    else:
        bucket = conn.create_bucket(S3_BucketName)

    print_test_info()

    ########################################
    # start Test
    ########################################
    for size in Test_FileSize:
        #---------------------------------------
        # create data file and s3 key for testing
        #---------------------------------------
        print("Preparing Test File (%sM)" % size)
        ddfile = DD_File(Test_FileName, Test_FilePath, size)

        #---------------------------------------
        # upload file to radosgw
        #---------------------------------------
        print("Uploading..... %sM Test File" % size)
        spent_time_records = []
        for i in range(1, Test_Iterate+1, 1):
            key = bucket.new_key(Test_FileName+"_"+str(size))
            spent_time = s3_upload(key, ddfile.lookup())
            spent_time_records.append(float(spent_time))
            print("  %s:\tTime         : %s seconds" %(i, spent_time))
            if i < Test_Iterate:
                bucket.delete_key(Test_FileName+"_"+str(size))
            time.sleep(Test_Delay_Interval)
        statistics_calc(spent_time_records)

        #---------------------------------------
        # download file from radosgw
        #---------------------------------------
        print("Downloading... %sM Test File" % size)
        spent_time_records = []
        for i in range(1, Test_Iterate+1, 1):
            localfile = ddfile.lookup()
            ddfile.delete()
            ddfile.delete_file_cache()
            spent_time = s3_download(key, localfile)
            spent_time_records.append(float(spent_time))
            print("  %s:\tTime         : %s seconds" %(i, spent_time))
            time.sleep(Test_Delay_Interval)
        statistics_calc(spent_time_records)
        bucket.delete_key(Test_FileName+"_"+str(size))
        ddfile.delete()
    
    #s3_list(bucket)
