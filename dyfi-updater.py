#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib2
import base64
import re
import time

Hostnames = ["hostname1.dy.fi", "hostname2.dy.fi"]
Username = ""
Password = "" 

def init():
    return getCurrentIP()

def getCurrentIP():
    http = httplib2.Http()
    try:
        response, content = http.request("http://checkip.dy.fi/")

        if response.status == 200:
            ip = re.findall(r'[0-9]{1,3}(?:\.[0-9]+){3}', content)
            return ip

    except (httplib2.ServerNotFoundError, IOError) as error:
        print ("Checking IP failed!")
        print (repr (error))
        time.sleep(10)
        getCurrentIP()

def updateIp(ip):
    global Hostnames
    global Username
    global Password

    print("Updating IP to: " + str(ip))

    baseUrl = "https://www.dy.fi/nic/update?hostname="
    auth = base64.encodestring( Username + ':' + Password )

    http = httplib2.Http()
    for hostname in Hostnames:
        url = baseUrl + hostname
        print ("Update URL: " + url)
        try:
            response = http.request(url, 'GET', headers = { 'Authorization' : 'Basic ' + auth })
            print (response)
        
        except (httplib2.ServerNotFoundError, IOError) as error:
            print ("Updating failed!")
            print (repr (error))
            time.sleep(5)
            updateIp(ip)

    print ("\n")
    # TODO: Check response status and retry if update/connection was failed.
    #       Alternatively return true/false status to main and do somenthing there...
    '''
        'abuse'     => 'The service feels YOU are ABUSING it!',
        'badauth'   => 'Authentication failed',
        'nohost'    => 'No hostname given for update, or hostname not yours',
        'notfqdn'   => 'The given hostname is not a valid FQDN',
        'badip'     => 'The client IP address is not valid or permitted',
        'dnserr'    => 'Update failed due to a problem at dy.fi',
        'good'      => 'The update was processed successfully',
        'nochg'     => 'The successful update did not cause a DNS data change'
    '''


def main():
    currentIp = getCurrentIP()
    lastUpdated = time.time()

    print ("Starting time: " + time.ctime(int(lastUpdated)))
    print ("Current IP: " + str(currentIp))

    print ("Update ip once before continuing")
    updateIp(currentIp)

    while True:
        newIp = getCurrentIP()

        if time.time() - lastUpdated > 90450:
            print ("Force Updating IP!")
            print ("Time is: " + time.ctime(int(lastUpdated)))
            updateIp(newIp)
            lastUpdated = time.time()

        if newIp == currentIp:
            time.sleep(64)      
        else:
            updateIp(newIp)
            lastUpdated = time.time()
            currentIp = newIp


if  __name__ =='__main__':
    main()