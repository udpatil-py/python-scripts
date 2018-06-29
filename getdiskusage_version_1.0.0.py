#!/usr/local/bin/python3
###########################################################################
#  Script     : getdiskusage_version_1.0.0.py                             #
#  Version    : Python 3.5.4                                              #
#  Author     : Uday Kumar Patil  (udpatil.py@gmail.com)                  #
#  Date       : 06/16/2018                                                #
#  Description: Script to find files recursively on given path.           #
###########################################################################

#----------------------------------------------------------------------------------------------------#
import os
import logging
import sys
import glob
import re
import json
import time
import subprocess

#----------------------------------------------------------------------------------------------------#
#Assumptions and extra comments about the program
#I assume that as per condition, SSH is not allowed without VP approval
#hence there should be a sudo access,to mount the remote filesystem on local server
#or we should be allowed to mount the path of interest with generic usernames and passwords if aggreed
#----------------------------------------------------------------------------------------------------#
#initializing global variables
path = sys.argv[1]
dirs = []
rfilex = []
path_check = re.compile(r"[^.\-\w\/\:\@]")
LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename="getdiskusage.log",filemode="a",level=logging.DEBUG,format=LOG_FORMAT)
logger = logging.getLogger()
#----------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------#            
def main(path):
   """main program starts here,check path format and proceed"""
   logger.info("checking path format")
   while path_check.search(path):
       print("Invalid path syntax...!")
       logger.error("Invalid path syntax...!",path)
       logger.info("waiting for user to enter correct path")
       path = input("Please enter absolute path name to proceed...!\nExample:'username@server:/opt/target/monitor/app/' \n")

   logger.info("given path has all expected characters and checking further now")
   
   status, newpath = server_check_and_mount(path)
   
   if status:
       logger.info("path is valid and mounted successfully on local server")
       
       for testfun in [search_files_1,search_files_2,search_files_3,search_files_4]:
           time1 = time.time()
           if testfun != search_files_2:
               data = testfun(newpath)
               time2 = time.time()
           else:
               testfun(newpath)
               if dirs != []:
                   for cd in dirs:
                       list_files(cd)
               else:
                   list_files(newpath)
               time2 = time.time()
               data = rfilex
           if data is not False and data != []:
               json_data = json.dumps({"files":data})
               #print("\n\n",json_data)
               logger.info("number of files found using %s function is %s:"%(testfun,str(len(data))))
               logger.info("%s function took %0.3f ms"%(testfun,(time2-time1)*1000.0))
               logger.info(20*"="+"Just displaying only few top and bottom files of json data"+20*"=")
               logger.info("\n,\n"+json_data[0:1000]+5*"\n."+json_data[-1000:])
               logger.info(100*"*")
               logger.info(40*"*"+"Next Function Starts"+40*"*")
               logger.info(100*"*")
           else:
               logger.info(24*"="+"No files found"+24*"=")
               print('\n'+24*"-"+"Please check getdiskusage.log for more information"+24*"-")
       
       logger.info("Waiting to unmount the filesystem as required task is completed") 
       time.sleep(5)
       command = "sudo fusermount -u "+newpath
       status = os.system(command)
       if status == 0:
           logger.info("successfully unmounted the remote filesystem from local machine")
           print("successfully unmounted the remote filesystem from local machine")
       else:
           logger.error("unable to umount the path"+newpath)
           print("unable to umount path",newpath)

#----------------------------------------------------------------------------------------------------#
def server_check_and_mount(path):
    
    try:
        if "@" in path and ":" in path:
            username,serverip,mountpath = re.split("@|:",path)
            command = "sudo sshfs -o allow_other,IdentityFile=/home/python/.ssh/id_rsa {0}@{1}:{2} /home/python/Desktop/newmount".format(username,serverip,mountpath)
            logger.info("username:"+username)
            print("UserName:",username)
        elif "@" not in path and ":" in path:
            serverip,mountpath = re.split(":",path)
            command = "sudo sshfs -o allow_other,IdentityFile=/home/python/.ssh/id_rsa {0}:{1} /home/python/Desktop/newmount".format(serverip,mountpath)
        else:
            logger.info("incorrect path format received,desired format is : username@server@/path")
            print("Please enter path in desired format example: username@server:/path")
            sys.exit()
        logger.info("ServerName/ip:"+serverip)
        logger.info("Remote Server mountpath:"+mountpath)
        print("ServerName/ip:",serverip)
        print("Remote Server mountpath:",mountpath)

        status = os.system("ping -c 1 "+serverip)

        if status != 0:
            logger.error("Server not reachable")
            sys.exit("ERROR : Server not reachable")
        elif status == 0:
            mountpoints = subprocess.check_output('mount')
	
            if len(list(set(mountpath))) == 1:
                logger.error("Invalid input path"+mountpath)
                sys.exit("Invalid input path")

            if mountpath == "/" or  mountpath == "/root" or mountpath == "/root/":
                logger.warning("mount is restricted on root directories, exiting the program")
                sys.exit("mount is restricted on root directories")
            elif mountpath in str(mountpoints):
                logger.info(10*"-"+"path is already in mount,please check below mount locations"+10*"-"+"\n"+mountpoints)
                print(10*"-"+"path is already in mount,please check below mount locations"+10*"-"+"\n\n"+mountpoints)
                sys.exit()
            else:
                status = os.system(command)
                if status == 0:
                    newpath = "/home/python/Desktop/newmount"
                    logger.info("newmount path is received now:"+newpath)
                    return (True,newpath)
                else:
                    logger.error("Unable to mount")
                    print("Unable to mount")
        else:
            logger.error("Invalid Server Name")
            sys.exit("Invalid Server Name")
    except Exception as e:
        logger.error("Exception occurred in {0} function \n {1}".format(server_check_and_mount.__name__,e))
        print("Exception occured ",e)

#----------------------------------------------------------------------------------------------------#

    
#----------------------------------------------------------------------------------------------------#
def search_files_1(path):
    """search file recursively for given path"""
    logger.info("Started to search file recursively using glob function")
    filex = []
    try:
        for file in glob.glob(path+"/**/*",recursive=True):
            file_name = os.path.join(path,file)
            if os.path.isfile(file_name):
                size = os.path.getsize(file)
                temp = {file:size}
                filex.append(temp)
        return filex
    except Exception as e:
        logger.error("Exception occurred in {0} function \n {1}".format(search_files_1.__name__,e))
        print("Exception occurred in {0} function \n {1}".format(search_files_1.__name__,e))
        return filex
#----------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------#
"""search file recursively and return search result without using os.walk"""
def search_files_2(path):
    "find all directory names with full path"
    try:
        files = os.listdir(path)
        for file in files:
            x = os.path.join(path,file)
            if os.path.isdir(x):
                dirs.append(x)
                search_files_2(x)
    except Exception as e:
        logger.error("Exception occurred in {0} function \n {1}".format(search_files_2.__name__,e))
        print("Exception occurred in {0} function \n {1}".format(search_files_2.__name__,e))
 
def list_files(cd):
    "list file names and size of the given directory"
    try:
        files = os.listdir(cd)
        for file in files:
            file_name = os.path.join(cd,file)
            if os.path.isfile(file_name):
                size = os.path.getsize(file_name)
                rfilex.append({file_name:size})
    except Exception as e:
        logger.error("Exception occurred in {0} function \n {1}".format(list_files.__name__,e))
        print("Exception occurred in {0} function \n {1}".format(list_files.__name__,e))
        
#----------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------#
def search_files_3(path):
    """search files using os.walk"""
    filex = []
    logger.info("started finding files using os.walk")
    try:
        for dirpath,dirname,filelist in os.walk(path):
            for file in filelist:
                file_name = os.path.join(dirpath,file)
                if os.path.isfile(file_name):
                    size = os.path.getsize(file_name)
                    filex.append({file_name:size})
        return filex
    except Exception as e:
        logger.error("Exception occurred in {0} function \n {1}".format(search_files_3.__name__,e))
        print("Exception occurred in {0} function \n {1}".format(search_files_3.__name__,e))
        return filex
#----------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------#
def search_files_4(path):
    """search files above given threshold size recursively,
    and stop search if timeout and return search result"""
    
    logger.info("finding logs which are more than 100MB in size with in 30 seconds of given timeout")
    filex = []
    "below threshold set to find files more than 100 MB"
    threshold_size = 100000000 #100MB, 100 followed by 6 0's
    
    "30 seconds time out threshold to stop search"
    timeout_threshold = 30 #default 30 sec maximum search time given
    try:
        timeout = time.time()+timeout_threshold
        while timeout > time.time():
            logger.info("started file search with file size limit of 100MB and timeout of 30 seconds at:Remote Server mountpath:\t"+path)
            time.asctime()
#            print("\nstarted file search with file size limit of 100MB and timeout of 30 seconds at:",time.asctime())
            for n in range(1):
                for file in glob.glob(path+"/**/*",recursive=True):
                    size = os.path.getsize(file)
                    if size > threshold_size:
                        temp = {file:size}
                        filex.append(temp)
            break
        
        if timeout < time.time():
            logger.warning("file search stopped due to timeout,default timeout is 30 sec:"+time.asctime())
#            print("file search stopped due to timeout,default timeout is 30 sec:",time.asctime())
        else:
            logger.info("file search completed by:"+time.asctime())
#            print("file search completed by:",time.asctime())
        
        if filex == []:
            logger.info("no files found more than 100MB in size")
            return filex
        else:
            return filex
    
    except Exception as e:
        logger.error("Exception occurred in {0} function \n {1}".format(search_files_4.__name__,e))
        print("Exception occurred in {0} function \n {1}".format(search_files_4.__name__,e))
        return filex
#----------------------------------------------------------------------------------------------------#


#-------------------------------------------START----------------------------------------------------#
if __name__ == "__main__":
    logger.info(24*"="+"Program Started"+24*"=")
    print(24*"="+"Program Started"+24*"=")
    main(path)
    logger.info(20*"="+"Program Ended successfully"+20*"=")
    print(20*"="+"Program Ended successfully"+20*"=")
#--------------------------------------------END-----------------------------------------------------#
