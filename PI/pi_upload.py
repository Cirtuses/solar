# coding:utf-8
import os
import re
import time
import shutil
import datetime
import subprocess
import psutil
import urllib
import threading
import paramiko

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
import logging
from pi_upload_config import *

time = time.strftime('%Y%m%d', time.localtime(time.time()))
download_path = os.path.join(download_path, time)
print(download_path)

import time


class PIload:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.client = None
        self.init_logger()
        

    def init_logger(self):
        self.logger = logging.getLogger('efuseload')
        self.logger.setLevel('INFO')
        console = logging.StreamHandler()
        console.setLevel("INFO")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        handler = logging.FileHandler("/home/pi/Desktop/log/{}.txt".format(time.strftime('%Y%m%d', time.localtime(time.time()))))
        handler.setLevel('INFO')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def create_sftp_client(self):
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.username, password=self.password)
            self.client = paramiko.SFTPClient.from_transport(self.transport)
            self.logger.info("create_sftp_client PASS")
        except Exception as e:
            self.logger.error(e)
            raise Exception(e)

    def stop_sftp_client(self):
        try:
            self.transport.close()
        except Exception as e:
            self.logger.error(e)
            raise Exception(e)

    def remove_file(self,file_path):
        files = os.listdir(file_path)
        for file in files:
            remove_file_path = os.join(file_path, file)
            os.remove(remove_file_path)

    def execute_efuse(self):  # execute 
        for i in range(1):
            try:
                self.upload() #local_upload_path
                break
            except Exception as  ex :
                if i >= 0 :
                    raise Exception(ex)
                else:
                    self.logger.info("Update ftp fail times:{}".format(i+1))
                pass
        self.trans_file()
        self.logger.info("Update efuse PASS")

    def kill(self,proc_pid):
        parent_proc = psutil.Process(proc_pid)
        for child_proc in parent_proc.children(recursive=True):
            child_proc.kill()
        parent_proc.kill()


    def generate_url(self,command = 'generate_url.sh'):
        """ execute commands and judge result of returns
            Args:
            command: generate rul 
            retest_allowed: false or true
        """
        url = ''
        bflag = False

        try:
            wpath = os.path.split(os.path.abspath(__file__))[0]
            cmd = "{}/{} ".format(wpath,command)
            proc = subprocess.Popen(args=[cmd],
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                bufsize=1)
        
            while proc.poll() is None:
                for line in iter(proc.stdout.readline, b''):
                    line = line.decode('UTF-8')
                    self.logger.info("generate_url:{}".format(line))
                    if line.find("https://artifactory-cn.nevint.com:443/artifactory/firmware-all-local/adc/fuse/") >= 0:
                        bflag = True
                        self.kill(proc.pid)
                        url_message = line.split('"')  
                        url = url_message[3]         
                        self.logger.info("url message is: {}".format(line))
                        break     
            self.logger.info("generate url is {}".format(url))

        except subprocess.CalledProcessError as e:
            self.logger.error(e)
            raise Exception(e)

        if bflag:
            self.logger.info("{} success".format(cmd))
            return url
        else:
            self.logger.info("{} fail".format(cmd))
            raise Exception("generate_url fail")
            return ' '

    def upload(self):
        # 获取Transport实例
        try:
            is_existence = False
            self.logger.info(host)
            self.logger.info(port)
            self.logger.info("sftp connect pass")
            ## 或使用
            # # 配置私人密钥文件位置
             # private = paramiko.RSAKey.from_private_key_file('/Users/root/.ssh/id_rsa')
            # # 连接SSH服务端，使用pkey指定私钥
            # tran.connect(username="root", pkey=private)
    
            # 获取SFTP实例
            self.logger.info("sftp from_transport pass")
            
            #while not is_existence:
            #    is_existence = True if "request" in self.client.listdir(communicate_path) else False
            #    if not is_existence:
            #        self.logger.info("upload pause")
            
            self.logger.info("start upload")

            is_existence = True if "running" in self.client.listdir(base_remote_path) else False
            self.logger.info(self.client.listdir(base_remote_path))
            self.logger.info(is_existence)

            if not is_existence:
                self.client.mkdir(remote_path)

            files = os.listdir(download_path)
            for file in files:
                local_path = os.path.join(download_path, file)
                remote_upload_path = os.path.join(remote_path, file)
                self.logger.info(local_path)
                self.logger.info(remote_upload_path)
                self.client.put(local_path, remote_upload_path)
                self.logger.info("sftp put pass")

        except Exception as e:
            self.stop_sftp_client()
            self.logger.error(e)
            raise Exception(e)


    def renameftpdone(self):
        try:
            is_existence = False
            newfilepath = ""
            newfilepath = base_remote_path +"done_"+ datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            is_existence = True if "running" in self.client.listdir(base_remote_path) else False
            self.logger.info(self.client.listdir(base_remote_path))

            if is_existence:
                self.logger.info(newfilepath)
                self.client.rename(remote_path,newfilepath)
        except Exception as e:
            self.logger.error(e)
            raise Exception(e)
        self.logger.info("Renameftpdone PASS")


    def callbackfunc(self,blocknum, blocksize, totalsize):
        '''''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        print("%.2f%%" % percent)


    def trans_file(self):
        filename_list = os.listdir(download_path)
        for file in filename_list:
            used_name = os.path.join(download_path, file)
            new_name = os.path.join(local_save_path, file)
            self.logger.info("{} ==> {}".format(used_name, new_name))
            shutil.move(used_name, new_name)
    

def main():
    start_time = time.time()
    fuse_obj = PIload(host, port, sftp_username, sftp_password)
    fuse_obj.create_sftp_client()

    j = 1
    for i in range(efusenumber):
        fuse_obj.execute_efuse()
        if j == perfusenumber or i == efusenumber -1 :
            fuse_obj.renameftpdone()
            j = 0
        j = j + 1
    
    end_time = time.time()
    print("cost time is {}".format(end_time - start_time))
    fuse_obj.delete_files()
    fuse_obj.stop_sftp_client()
    #end_time = time.time()
    #print("cost time is {}".format(end_time - start_time))


if __name__ == '__main__':
    main()
