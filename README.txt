Hello,

+----------------+
| Project Title: |											|
+----------------+
List out all the files on the mountpoint and their disk usage in bytes in json format.

This program is written in python 3.5.4 on linux machine RHEL 6 and tested on few cases to my best.

Assuming there will be some generic user id and password is provided to developers to perform
certain tasks with limited access.

In this case I have assumed that the developer is allowed to enter the password,however the script just connect the
remote server on specific given mount path and performs required task and umount it immidiately once results are
written to the getdiskusage.log file.

The script is written based on 4 scenarios,considering sshfs
each scenario shows its performace and can be found in the logs.
1. using glob function recursively
2. using normal os module with simple option recursively
3. using os.walk
4. using glob function recursively, but given a threshold and timeout scenarios which may be helpful when we touch huge prod filesystems
so,the program will stop fetcthin the file information once the timeout crosses to avoid any extra load on the production landing servers
and it is always welcomes any recommendation or changes if required in real time, like size limit and timeout limits.


+--------------------------------------+
| Configuration details/Prerequisites: |											|
+--------------------------------------+
My system Arch:
Linux localhost.localdomain 2.6.32-71.el6.i686 #1 SMP Wed Sep 1 01:26:34 EDT 2010 i686 i686 i386 GNU/Linux

Install python 3.5.4
https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tar.xz

install and configure two linux servers,one to run the code another as a remote servers to access its filesystem
install sshfs on both 
wget https://rpmfind.net/linux/epel/6/i386/Packages/f/fuse-sshfs-2.4-1.el6.i686.rpm
rpm -ivh fuse-sshfs-2.4-1.el6.i686.rpm

configure sudo
visudo
%wheel ALL=(ALL)       NOPASSWD: ALL #uncomment
usermod -aG wheel python

copy the code getdiskusage_version_1.0.0.py 


Input Test cases,few are given below:
python3 getdiskusage_version_1.0.0.py rhel6@192.168.84.135:/
python3 getdiskusage_version_1.0.0.py rhel6@192.168.84.135:/root
python3 getdiskusage_version_1.0.0.py rhel6@192.168.84.135:/root/
python3 getdiskusage_version_1.0.0.py rhel6@192.168.84.135://////
python3 getdiskusage_version_1.0.0.py test@servername:/opt/target/monitor/app
python3 getdiskusage_version_1.0.0.py 192.168.84.135:/home/rhel6/
python3 getdiskusage_version_1.0.0.py rhel6@192.168.84.135:/home/rhel6/Desktop/target/
python3 getdiskusage_version_1.0.0.py rhel6@192.168.84.135:/home/rhel6/Desktop/target/monitor
python3 getdiskusage_version_1.0.0.py rhel6@192.168.84.135:/home/rhel6/Desktop/target/monitor/logs

configure ssh:
ssh-keygen
ssh-copy-id -i ~/.ssh/id_rsa.pub rhel6@192.168.84.135
test it:
ssh rhel6@192.168.84.135 
Note: in sshfs IdentityFile path should be absolute path of the private key

sample_command = 'sudo sshfs -o allow_other,IdentityFile=/home/python/.ssh/id_rsa python@192.168.84.135:/home/python/Desktop/python_scripts /home/rhel6/Desktop/remote1'

sudo fusermount -u /home/python/Desktop/newmount

#create some junk files with random system files on remote server,that is server two
import os
import time
import random

flist = ['/proc/cpuinfo','/proc/meminfo','/proc/crypto','/proc/uptime','/proc/swaps','/proc/zoneinfo']
for x in range(1000):
    fn = str(time.time())+".log"
    f = random.choice(flist)
    os.system("cat "+f+" > "+fn)


+---------+
| AUTHOR: |											|
+---------+
UDAY KUMAR PATIL
udpatil.py@gmail.com
https://github.com/udpatil-py/python-scripts
