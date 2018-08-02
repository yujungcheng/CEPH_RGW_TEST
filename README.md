# CEPH_RGW_TEST


WorkFlow

1. connect to radosgw
2. set test bucket
3. generate local test file for upload/download
4. upload testfile
5. download testfile 
6. delete local test file
7. delete test file in ceph

```
root@ycheng:~/ceph-rgw-test# ./s3_test.py

Test File Uploading/Downloading, Test Iteration: 1
  *File size      = [16, 32] in MB
  *File path      = /tmp/
  *File name      = ddfile
  *S3 Rgw Host    = 172.20.3.63
  *S3 Rgw Port    = 7480
  *S3 Bucket Name = s3-test-bucket
  *S3 AccessKey   = 6333TG5E6YC9RYVSPIUA
  *S3 SecretKey   = gcCoGTWMR9PYOkfdUhdhbJDHlBqGmu5Z9wxQ3h6D
==================================================
Preparing Test File (16M)
Uploading..... 16M Test File
  1:	Time         : 0.479 seconds
  ------------------------------------------------
  Mean Value         : 0.479
  Median Value       : 0.479
  Standard Deviation : 0.000

Downloading... 16M Test File
  1:	Time         : 0.407 seconds
  ------------------------------------------------
  Mean Value         : 0.407
  Median Value       : 0.407
  Standard Deviation : 0.000

Preparing Test File (32M)
Uploading..... 32M Test File
  1:	Time         : 1.166 seconds
  ------------------------------------------------
  Mean Value         : 1.166
  Median Value       : 1.166
  Standard Deviation : 0.000

Downloading... 32M Test File
  1:	Time         : 0.480 seconds
  ------------------------------------------------
  Mean Value         : 0.480
  Median Value       : 0.480
  Standard Deviation : 0.000

root@ycheng:~/ceph-rgw-test# 
```
