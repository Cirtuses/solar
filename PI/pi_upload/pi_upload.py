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

# config
host = '192.168.3.69'
port = 22
sftp_username ='pi'
sftp_password ='yahboom'

Time = datetime.datetime.now()
Time = time.strftime('%Y%m%d') # 与拍照约定使用当天的问题件 例如20210701

local_image_path = os.path.join('/home/pi/Desktop',  Time)   # 用与上传

if os.path.exists(local_image_path) == False:
    print("image is null")

remote_path = '/data' #远程的上传路径
remote_path = os.path.join('/data', Time)

local_log_path = '/home/pi/Desktop/log'

class PIload:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sftp= None
        self.client = None
        self.init_logger()
        
    def init_logger(self):
        self.logger = logging.getLogger('pi upload')
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
            self.ssh_obj = paramiko.SSHClient()
            self.ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # self.ssh_obj.connect(hostname=self.host, port=self.port, username=self.username, password=self.password,allow_agent=False, look_for_keys=False)
            self.ssh_obj.connect(hostname=self.host, port=self.port, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)            
            self.sftp= paramiko.Transport((self.host, self.port))
            self.sftp.connect(username=self.username, password=self.password)
            self.client = paramiko.SFTPClient.from_transport(self.sftp)
            self.logger.info("create_sftp_client PASS")
        except Exception as e:
            self.logger.error(e)
            raise Exception(e)

    def stop_sftp_client(self):
        try:
            self.sftp.close()
        except Exception as e:
            self.logger.error(e)
            raise Exception(e)

    def remove_file(self, file_path):
        files = os.listdir(file_path)
        for file in files:
            remove_file_path = os.join(file_path, file)
            os.remove(remove_file_path)

    def kill(self, proc_pid):
        parent_proc = psutil.Process(proc_pid)
        for child_proc in parent_proc.children(recursive=True):
            child_proc.kill()
        parent_proc.kill()

    def upload(self):
        try:
            self.logger.info(host)
            self.logger.info(port)
            self.logger.info("sftp connect pass")
            self.logger.info("start upload")
            
            try:
                self.sftp.stat(remote_path)
            except Exception as e:
                # TO DO
                self.ssh_obj.exec_command("mkdir -p {}".fromat(remote_path)) # 创建远程文件夹

            files = os.listdir(local_image_path)
            for file in files:
                local_image = os.path.join(local_image_path, file)
                remote_image = os.path.join(remote_path, file)
                self.logger.info("the image {} is uploading".format(local_image))
                self.logger.info(remote_image)
                self.client.put(local_image, remote_image) #执行上传
                self.logger.info("sftp put pass")

        except Exception as e:
            self.stop_sftp_client() # stop 上传
            self.logger.error(e)
            raise Exception(e)
    

def main():
    start_time = time.time()
    
    pi_obj = PIload(host, port, sftp_username, sftp_password)
    pi_obj.create_sftp_client()

    for i in range(1):
        try:
            pi_obj.upload() #local_upload_path
            break
        except Exception as  ex :
            if i >= 0 :
                raise Exception(ex)
            else:
                pi_obj.logger.info("Update sftp fail times:{}".format(i+1))
            pass

    
    end_time = time.time()
    print("cost time is {}".format(end_time - start_time))
    pi_obj.stop_sftp_client()


if __name__ == '__main__':
    main()
