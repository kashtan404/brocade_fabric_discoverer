#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import sys
import getpass
import re
import argparse

parser = argparse.ArgumentParser(description='brocade_fabric_discoverer')
parser.add_argument('-host', '--hostname', help='BNA host', required=True)
parser.add_argument('-user', '--user', help='BNA user', required=True)
parser.add_argument('-pswd','--password', help='BNA password', required=True)
args = parser.parse_args()

usr = args.user
pwd = args.password
hst = args.hostname
errormask = re.compile('errorMsg=(.*)]')
addnextflag = 'y'

class netadvisor(object):

    def __init__(self, usr, pwd, hst):
        self.__usr = usr
        self.__pwd = pwd
        self.__hst = hst

    def start(self):
        print('Default NetworkAdvisor IP: ' + self.__hst)
        usertype = raw_input('Change NetworkAdvisor? "y" for change or leave blank to continue. ')
        if usertype == 'y':
            self.__hst = raw_input('NetworkAdvisor IP: ')
            self.__usr = raw_input('NetworkAdvisor USR: ')
            self.__pwd = getpass.getpass('NetworkAdvisor PASS:')
        self.getauth()

    def getauth(self):
        self.__url = 'http://' + self.__hst + '/rest/login'
        self.__headers = {'WSUsername': self.__usr, 'WSPassword': self.__pwd,
                          "Accept": "application/vnd.brocade.networkadvisor+json;version=v1"}
        try:
            self.__resp = requests.post(self.__url, headers=self.__headers, timeout=5)
        except:
            print('Cannot connect to ' + self.__url)
            sys.exit(2)
        else:
            if self.__resp.status_code != 200:
                print('Responce: ' + str(self.__resp.status_code) + ' ' + self.__resp.reason)
                sys.exit(2)
            self.__token = self.__resp.headers["WStoken"]
            print('Authed!')
        return self.__token

    def logout(self):
        self.__url = 'http://' + self.__hst + '/rest/logout'
        self.__headers = {"WStoken": self.__token}
        requests.post(self.__url, headers=self.__headers, timeout=5)
        print('Bye!')
        sys.exit(0)

    def getfabrics(self):
        self.__url = 'http://' + self.__hst + '/rest/resourcegroups/All/fcfabrics'
        self.__headers = {"WStoken": self.__token, "Accept": "application/vnd.brocade.networkadvisor+json;version=v1"}
        self.__resp = json.loads(requests.get(self.__url, headers=self.__headers).content.decode("utf-8"))
        return self.__resp

    def getfabricinfo(self, fabrickey):
        self.__url = 'http://' + self.__hst + '/rest/resourcegroups/All/fcfabrics/' + fabrickey + '/fcswitches'
        self.__headers = {"WStoken": authtoken, "Accept": "application/vnd.brocade.networkadvisor+json;version=v1"}
        self.__resp = json.loads(requests.get(self.__url, headers=self.__headers).content.decode("utf-8"))
        return self.__resp

    def discoverfabric(self):
        self.__fabname = raw_input('Type fabric name: ')
        self.__switch_ip = raw_input('Type switch ip: ')
        self.__switch_user = raw_input('Type username: ')
        self.__switch_pass = getpass.getpass()
        self.__data = {"switchIpAddress": self.__switch_ip, "userName": self.__switch_user,
                       "password": self.__switch_pass, "fabricName": self.__fabname}
        self.__url = 'http://' + self.__hst + '/rest/resourcegroups/All/discoverfabric'
        self.__headers = {"WStoken": self.__token, "Accept": "application/vnd.brocade.networkadvisor+json;version=v1",
                   "Content-type": "application/vnd.brocade.networkadvisor+json;version=v1"}
        self.__resp = requests.post(self.__url, headers=self.__headers, data=json.dumps(self.__data)).content.decode("utf-8")
        if not '{"virtualFabricIds":[]}' in self.__resp:
            self.__errormsg = re.search(r'.*errorMsg=(.*)\].*', self.__resp)
            print('Error: ' + self.__errormsg.group(1))
        else:
            print('done!')
        return self.__resp

    def deletefabric(self, fabrickey):
        self.__url = 'http://' + self.__hst + '/rest/resourcegroups/All/fcfabrics/' + fabrickey + '/deletefabric'
        self.__headers = {"WStoken": self.__token}
        self.__resp = requests.post(self.__url, headers=self.__headers).content.decode("utf-8")
        return self.__resp

if __name__ == '__main__':
    conn = netadvisor(usr, pwd, hst)
    conn.start()
    while addnextflag == 'y':
        conn.discoverfabric()
        addnextflag = raw_input('Add next? y/n ')
    conn.logout()
