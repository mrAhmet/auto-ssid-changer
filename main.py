import sys
import requests
import getpass
from datetime import datetime
import time

class infoChanger:

    def __init__(self):
        # -s: ssid, -p: password, -ru:router username ,-rp: router password -r: request file
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-s": 
                self.ssid = sys.argv[i+1]

            elif sys.argv[i] == "-p":
                self.password = sys.argv[i+1]

            elif sys.argv[i] == "-ru":
                self.routerUser = sys.argv[i+1]
            
            elif sys.argv[i] == "-rp":
                self.routerPass = sys.argv[i+1]

            elif sys.argv[i] == "-r":
                self.reqFile = sys.argv[i+1]
            

    def getCookie(self):
        self.loginUrl = "http://192.168.2.1/cgi-bin/login"
        self.login_header = {'Host':'192.168.2.1' , 'Accept':'application/xml, text/xml, */*; q=0.01' , 'Accept-Language':'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3' , 'Accept-Encoding':'gzip, deflate' , 'Content-Type':'application/x-www-form-urlencoded' , 'Content-Length':'54' , 'Origin':'http://192.168.2.1' , 'Connection':'close' , 'Referer':'http://192.168.2.1/wireless/settings/loginmain.html' , 'Upgrade-Insecure-Requests':'1' }
        self.login_data = "redirect=&self=&user={}&password={}&gonder=TAMAM".format(self.routerUser,self.routerPass)
        login = requests.post(self.loginUrl, data= self.login_data, headers= self.login_header)
        self.cookie = login.headers['airtiesSessionId'].split(';')[0]
        
    def readReqFile(self):
        req = open(self.reqFile,'r')
        self.xmlReq = req.read().format(self.ssid,self.password)
        
    def sendReq(self):
        self.chng_url = "http://192.168.2.1/cgi-bin/webapp"
        self.change_header = {'Host':'192.168.2.1' , 'Accept':'application/xml, text/xml, */*; q=0.01' , 'Accept-Language':'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3' , 'Accept-Encoding':'gzip, deflate' , 'Content-Type':'application/x-www-form-urlencoded' , 'X-Requested-With':'XMLHttpRequest' , 'Content-Length':'2532' , 'Origin':'http://192.168.2.1' , 'Connection':'close' , 'Referer':'http://192.168.2.1/wireless/settings/settings_new.html' , 'Cookie':'{}'.format(self.cookie)}
        req_chng = requests.post(self.chng_url, data = self.xmlReq, headers = self.change_header)
        print(req_chng)

    def timer(self):
        date = datetime.now()
        if (date.hour == 22):
            return True
        else:
            time.sleep(1800)
            return False
        
    def reqStart(self):
        while True:
            if self.timer():
                self.getCookie()
                self.readReqFile()
                self.sendReq()
                time.sleep(3600)
        
if __name__ == "__main__":
    x = infoChanger()
    x.reqStart()

