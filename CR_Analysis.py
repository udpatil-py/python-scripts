#!/usr/bin/python
##############################################################
#  Script     : CR_Analysis.py
#  Author     : Uday Kumar Patil  (udpatil.py@gmail.com)
#  Date       : 07/28/2014
#  Description: Script to find the impact list from CR's.
##############################################################

"""
This program finds the impact list of our production servers by comparing the server names

with the CR impacted listed provided by (DB,Hosting,network....like teams) in service now,

and prints the final impacted hostnames....!
"""

with open("Your_project_server_list.txt",'r',encoding='utf-8')as server_list:
	server_names = server_list.readlines()

with open("CR_impact_list.txt",'r',encoding='utf-8')as impact_list:
	impacted_server_names = impact_list.readlines()

print('\n --------------these are the hosts found in impact list:--------------\n')
for host_name in [hostname_1 for hostname_1 in impacted_server_names for hostname_2 in server_names if hostname_1 == hostname_2]):
    print(host_name)

