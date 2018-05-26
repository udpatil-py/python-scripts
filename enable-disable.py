#!/usr/bin/python
##############################################################
#  Script     : PRD_monitor_enable_disable.py
#  Author     : Uday Kumar Patil  (udpatil.py@gmail.com)
#  Date       : 07/28/2017
#  Description: Script for monitoring Enable/Disable Status in Shifts.
##############################################################

import os
import time
import datetime
import smtplib
from email.mime.text import MIMEText
import sys
import filecmp


#============================================================================================#
def main():

        'main program starts from here'
        
        result = find_UI_changes()
        if result is 1:
                create_empty_file(jmsg['sendmail'])
                get_changed_details()
                send_email()

#============================================================================================#
def find_UI_changes():

        'find UI changes,check file sizes to avoid memory issues'
        
        if (os.stat(jmsg['firstfile']).st_size) > 1024:return 0
        if (os.stat(jmsg['secondfile']).st_size) > 1024:return 0
        if filecmp.cmp(jmsg['firstfile'],(jmsg['secondfile']), shallow = False):
                print ("Last execution time is: ",jmsg['time'])
                print ("No changes found ,both files are same hence exiting the code")
                return 0
        else:
                print ("Execution time is: ",jmsg['time'])
                print ("Finding changes now.........!")
                return 1

#======================================================================================================#
def create_empty_file(filename):
        open(filename, 'w').close()
        return None

#======================================================================================================#
def get_changed_details():

        'find the changes and write to sendmail file to send email'

        with open(jmsg['firstfile'], 'r')as file1:
                file1 = file1.readlines()
                with open((jmsg['secondfile']), 'r')as file2:
                        file2 = file2.readlines()
                        file1 = [i.replace('\n','') for i in file1]
                        file2 = [i.replace('\n','') for i in file2]
                        header = (" "*9+"-"*71)
                        title = (" "*8+"|   Lifecycle   |  Domain Name  |      Node_Name:Port_Number\t\t|")
    
        print (header)
        print (title)
        print (header)
        fw = open(jmsg['sendmail'], 'a+')
        for line in file1:
                if line in file2:
                        continue
                else:
                        line = "|" +line + "|"
                        line = line.replace('|','\t|\t')
                        print (line)
                        print (header)
                        fw.write(line)
        print (header)
        print (title)
        print (header)
        for line in file2:
                if line in file1:
                        continue
                else:
                        line = "|" +line + "|"
                        line = line.replace('|','\t|\t')
                        print (line)
                        print (header)
                        fw.write(line)
                
        print (header)
        print (title)
        print (header)
        for line in file1:
                line = "|" +line + "|"
                line = line.replace('|','\t|\t')
                print (line)
                print (header)     
                fw.write(line)

        print (fw.read())
        fw.close()





#======================================================================================================#
def get_changed_details_1():

        'find the changes and write to sendmail file to send email'
        file1 = open(jmsg['firstfile'], 'r').readlines()
        file2 = open((jmsg['path']+ "/"+ jmsg['secondfile']), 'r').readlines()
        file1 = [i.replace('\n','|\n') for i in file1]
        file2 = [i.replace('\n','|\n') for i in file2]
        fw = open((jmsg['path']+ "/"+ jmsg['sendmail']),'a+')
        fw.write("\n\n\n\n"+jmsg['newline']+ jmsg['decorator']+ jmsg['disabled']+ jmsg['decorator']+"\n")

        for n in file1:
                if n in file2:
                        continue
                else:
                        n = n.replace("PRD","\n|PRD")
                        n = n.replace("|","\t|\t")
                        fw.write(n)

        fw.write("\n\n" +jmsg['newline']+ jmsg['decorator']+ jmsg['enabled']+ jmsg['decorator']+"\n")

        for n in file2:
                if n in file1:
                        continue
                else:
                        n = n.replace("PRD","|PRD")
                        n = n.replace("|","\t|\t")
                        fw.write(n)

        fw.write("\n\n\n\n"+jmsg['newline']+ jmsg['decorator']+ jmsg['fyi']+ jmsg['decorator']+"\n")

        for n in file1:
                n = n.replace("PRD","|PRD")
                n = n.replace("|","\t|\t")

                fw.write(n)
        fw.close()
        print (open(jmsg['sendmail']), 'r').read()

#======================================================================================================#

def send_email():

        'send enabled/disabled node/domain list over email'
        
        with open((jmsg['sendmail']), 'r')as data:
                msg = MIMEText(jmsg['hi'] +''.join(data) +jmsg['thankyou'])
                msg['Subject'] = jmsg['subject']
                msg['From'] =  "noreply@gmail.com"
                msg['To'] =     jmsg['email_to']
                try:
                        s = smtplib.SMTP('localhost')
                        s.sendmail(msg['From'], msg['To'], msg.as_string())
                        s.quit()
                        print ("Email sent successfully")
                except Exception as e:
                        print ("\t ERROR: Status email could not be sent.")

#======================================================================================================#

def junk_messages():
        jmsg = {
                'time'          :       time.asctime( time.localtime(time.time()) ),
                'firstfile'      :       'input.txt',
                'decorator'     :       '-'*18,
                'newline'       :       '\n\t',
                'enabled'       :       ' Below listed JVMs are Enabled in ',
                'disabled'      :       ' Below listed JVMs are Disabled in ',
                'end'           :       ' End ',
                'fyi'           :       ' Pending list : Yet to be ENABLED ',
                'secondfile'    :       'prod_backup.txt',
                'path'          :       r'C:\Users\patilkum\Desktop Scripts\my pthon scripts',
                'sendmail'      :       'PRD_sendmail.txt',
                'file1'         :       'file1.txt',
                'file2'         :       'file2.txt',
                'subject'       :       'Notice : Changes found in PROD monitoring UI',
                'email_to'      :       'udpatil.py@gmail.com',
                'hi'            :       'Hi All,\n\nThis is to notify that below listed node/domain are Enabled or Disabled in SHIFT:',
                'thankyou'      :       """\n\nThanks & Regards,\nPlatform Operations.
                                    \n\n\bNOTE:  This is an auto generated email, Please do not reply...!""",
                }
        return jmsg
#======================================================================================================#
if __name__ == "__main__":
        jmsg = junk_messages()
        main()
