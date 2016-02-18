###############################--------##################################
# 1.0.0: Originial (past file) - 2013
# 1.0.1: quickened config - 1/10/15

###############################--------##################################

#PACKAGES#

import configparser, time, re, smtplib, os, requests, pyCookieCheat

#FILES#

Config = configparser.ConfigParser()
Config.read('confi.ini')
config_dict=['names','address','budget','diff_up','diff_down','log']

for i in config_dict:
    exec(i + "=Config.get('DEFAULT',i)")

budget, diff_up, diff_down=float(budget),float(diff_up),float(diff_down)

# acc_pwd = {i:n for i, n in [x.split("-") for x in acc_pwd.split(",")]}

#STOCK CLASS#

class MainStock(object):
    def __init__(self,name):
        self.name = name
        self.ini = 'quoteElementPiece4' #variable for data searching
        self.f = ("/LOGS/" + self.name + "_log.txt") #path for individual logs

    def initialize(self):

        self.running = False
        self.processing = True

        self.sell_value, self.buy_value = 0,0
        self.values = []

        self.readFile()

    def readFile(self,sep=":"): #Name of the file, Seperator of data
        if os.path.isfile(self.f):
            with open(self.f,'r') as data:
                read = data.readlines()[-1]
                value = read[12:].split(sep)
                if value[0] == "BUY": 
                    self.buy_value = value[1]
                    self.running = True
                elif value[0] == "FINALISATION": 
                    self.writeFile("INITIALISATION:")
        else:
            self.writeFile("INITIALISATION:",w)

    def writeFile(self,text, form = 'a',end = ';'):
        with open(self.f,form) as data: 
            data.write(str('%02d/%02d/%04d' % (time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year)) + "---" + text + end)

    def setParams(self):
        if self.running:
            writeFile("CLOSE:%02f" % self.close)
            writeFile("OPEN:%02f" % self.open)

            if self.close > self.open: 
                instFormat(10)
            else: 
                instFormat(20)

            self.current = self.last_current

    def uptdateParams(self):

        if !self.buy_value:
            if varCalc(self.current,self.last_current) > self.instant_down:
                self.buy_value = self.current
                self.writeFile("BUY:%02f" % self.buy_value)
        else:
            if self.

        self.current = self.last_current
#WEB#

def loadSite(end='quoteElementPiece11',end_num = 50):
    # cj = cookielib.CookieJar() ## add cookies
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # opener.addheaders = [('User-agent','Mozilla/5.0 \
    #                     (compatible; MSIE 6.0; Windows NT 5.1)')]
    # data = urllib.urlencode(acc_pwd)
    # r = opener.open(address,data,10) 

    s = requests.Session()
    cookies = pyCookieCheat.chrome_cookies(address)
    r = s.get(address, cookies=cookies,auth=('rballestiero','OEOM8032nielsypoo'))
    site = r.text

    for stock in stocks:
        print(site[site.find(stock.ini):site.find(end)+end_num])
        valores = re.findall(r'-?\d+.\d+\b', site[site.find(stock.ini):site.find(end)+end_num])
        stock.change, stock.percent_change, stock.current,stock.high,stock.low,stock.open,stock.close = [float(n) for n in valores if n.find(":")<0]
        stock.time = valores[-1]
        stock.values.append(stock.current)
        if stock.time.split(":")[0] != time.localtime().tm_hour:
            stock.running = True

def instFormat(obj,x):
    setattr(obj,"instant_up",x)
    setattr(obj,"instant_down",x*(-1))

def diffCalc(first,last):
    return ((first - last)/last)*100.

names = [n for n in names.split(",")]
stocks = [MainStock(name) for name in names]
processes = [stock.processing for stock in stocks]

#----------------------------------------------------------- Program starts here -------------------------------------------------------------------#

def run():

    loadSite()

    for stock in stocks: 
        stock.initialize()
        stock.setParams()

    while any(processes):



open_time = (10*60)
close_time = (17*60)

# while True:

#     if time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6:
#         weekend = True

#     current_time = ((time.localtime().tm_hour*60) + time.localtime().tm_min)%1440
#     print current_time

#     if (current_time >= open_time) and (current_time <= close_time) and (weekend == False):
run()

    # time.sleep(55)

