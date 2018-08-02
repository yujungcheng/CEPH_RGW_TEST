#!/usr/bin/python

import subprocess
import os.path

class DD_File:
    def __init__(self, name, path, size, ddif="/dev/urandom", ddbs="1M"):
        self.name = name
        self.path = path
        self.size = str(size)
        self.ddif = ddif
        self.ddbs = ddbs
        self.create()

    def create(self):
        if self.lookup() == False:
            dd_if    = " if=" + self.ddif
            dd_of    = " of=" + self.path + self.name
            dd_bs    = " bs=" + self.ddbs
            dd_count = " count=" + self.size
            dd_cmd   = "dd " + dd_if + dd_of + dd_bs + dd_count
            return self.execute(dd_cmd)
        return False
        
    def delete(self):
        if self.lookup() != False:
            rm_cmd = "rm -rf " + self.path + self.name
            return self.execute(rm_cmd)
        return False

    def lookup(self):
        if os.path.exists(self.path+self.name):
            return self.path+self.name
        return False

    def delete_file_cache(self):
        cmd = "echo 1 > /proc/sys/vm/drop/drop_caches; sync; sleep 1"
        return self.execute(cmd)

    def execute(self, *cmd,**kwargs):
        command = ' '
        command = command.join(cmd)
        cmdPopen = subprocess.Popen(command,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        out = cmdPopen.stdout.read().rstrip()
        err = cmdPopen.stderr.read().rstrip()
        #print("out %s, err %s" %(out, err))
        return out,err
