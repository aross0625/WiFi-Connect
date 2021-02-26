#!/usr/bin/python
import os
import re
import sys
import requests
import threading

def ReadWiFiFile():
    with open('/etc/wpa_supplicant/wpa_supplicant.conf','r') as f:
            configFile = f.readlines()
            f.close()
            return configFile

def InterpretWiFiFile(input):
    WiFiInfo = []
    for i in input:
        if "ssid" in i:
            s1 = i
            result1 = re.search('="(.*)"', s1)
            WiFiInfo.append(result1.group(1))
        elif "psk" in i:
            s2 = i
            result2 = re.search('="(.*)"', s2)
            WiFiInfo.append(result2.group(1))
    return WiFiInfo

def ConnectToWiFi(input):
    if len(input) > 1:
        os.system('sudo iwconfig wlan0 essid ' + input[0] + ' key s:' + input[1])
    else:
        os.system('sudo iwconfig wlan0 essid ' + input[0])

def IsConnectedToInternet():
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return False

def ConnectToLTE():
    os.system("sudo pon");

def VerifyConnectionStatus():
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        threading.Timer(60.0, VerifyConnectionStatus).start()
        print("Connected to the Internet")
    except (requests.ConnectionError, requests.Timeout) as exception:
        ConnectSequence()
        print("No internet connection.")

def ConnectSequence():
    Value1 = ReadWiFiFile()
    Value2 = InterpretWiFiFile(Value1)
    ConnectToWiFi(Value2)
    Value3 = IsConnectedToInternet()
    if Value3 != True:
        ConnectToLTE()
        threading.Timer(60.0, ConnectSequence).start()
    else:
        VerifyConnectionStatus()

def main():
    ConnectSequence()

if __name__ == "__main__":
    main()
