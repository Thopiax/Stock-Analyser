#FILES#
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read('confi.ini')
config_dict=['codes','FROM','TO','EMAIL','PASSWORD','budget','diff_up','diff_down','alert','inst_diff_up','log','path']

for i in config_dict:
    exec i + "=Config.get('DEFAULT',i)"

budget, diff_up, diff_down, alert,  inst_diff_up=float(budget),float(diff_up),float(diff_down),float(alert),float(inst_diff_up)
inst_diff_down = -1*inst_diff_up
codes = codes.split(",")

already_ran=False
weekend = False

def writeFile(text, f=log, form = 'a',end = ','):

        with open(f,form) as data:
            data.write(text + end)

#WEB#

def sendMail(SUBJECT = "",TEXT = ""): ## FUNCTION FACILITATING

    pass
#     from email.MIMEMultipart import MIMEMultipart
#     from email.MIMEText import MIMEText

#     msg = MIMEMultipart()

#     msg['From'] = FROM
#     msg['To'] = TO
#     msg['Subject'] = SUBJECT

#     with open(log,'r') as data:
#         text = """%s
    
# %s""" % (TEXT,data.read())


#     msg.attach(MIMEText(text))

#     mailServer = smtplib.SMTP("smtp.1and1.com", 587)
#     mailServer.ehlo()
#     mailServer.starttls()
#     mailServer.ehlo()
#     mailServer.login(EMAIL, PASSWORD)
#     mailServer.sendmail(EMAIL, TO, msg.as_string())
#     # Should be mailServer.quit(), but that crashes...
#     mailServer.close()

def varCalc(first,last):

    if last == 0:
        return False
    else:
        var = ((first - last)/last)*100.
        return var

def setTime():
    return int("%02d%02d" %(time.localtime().tm_hour, time.localtime().tm_min))

#--------------------------------------------------------------/--------------------------------------------#
#--------------------------------------------------------------/--------------------------------------------#
import time, urllib, re, smtplib, os, sys
#--------------------------------------------------------------/--------------------------------------------#
#--------------------------------------------------------------/--------------------------------------------#

class Stock(object):

    def __init__(self,code,budget=5000.0):
        self.valor_venda, self.valor_compra, self.valor_anterior = 0,0,0
        self.compra = False
        self.venda = False
        self.success = False

        self.code = code

        self.site = "http://finance.yahoo.com/q?s=%s" % (self.code)

        self.budget = budget
        self.loadSite()

    def checkTime(self,hora):

        if (self.hora_atual > (hora+10)) or (self.hora_atual < hora-10):
            writeFile("%s:NO REAL TIME -- ANALYSIS ABORTED" % (self.code), f=out, end = "\n")
            return False
        else: return True

    def reset(self):
        try:
            if self.valor_venda != 0:
                self.valor_venda, self.valor_compra, self.valor_anterior = 0,0,0
                self.compra = False
                self.venda = False 
                self.success = False
        except: pass

    def loadSite(self,ini='<span id="yfs_l84_',end='Bid:',end_num = 0):
        try:
            ssite = urllib.urlopen(self.site).read().decode('utf8') #Loads web
            self.valores = []

        except: 
            return False

        else:

            for i in re.findall(">[0-9]+[.:][0-9]+", ssite[ssite.find(ini):(ssite.find(end))+(end_num)]):
                self.valores.append(i.strip(">"))

            if len(self.valores) > 0:

                self.valor_atual = float(self.valores[0])

                if len(self.valores) < 4: self.valores.append(self.valores[0])
                if len(filter(lambda x: ':' in x,self.valores)) > 1: return "done"

                elif self.valores[1].find(":") > 0:

                    print str(self.valores[1][:self.valores[1].find(":")]) + str(self.valores[1][self.valores[1].find(":")+1:])

                    self.hora_atual = int(str(self.valores[1][:self.valores[1].find(":")]) + str(self.valores[1][self.valores[1].find(":")+1:]))
                    if self.hora_atual < 400:
                        self.hora_atual+=1200

                    return True

            else: return False 

    def checkValue(self, var):

        self.inst_up,self.inst_down = inst_diff_up, inst_diff_down

        if hasattr(self,"variacao_anterior"):

            self.var_inst = var(self.variacao, self.variacao_anterior)

            if self.variacao > 0:

                if self.variacao > diff_up:
                    self.inst_up = 1
                else:
                    self.inst_up = inst_diff_up

            else:

                if self.variacao < alert:
                    self.inst_down = -1

                else:
                    self.inst_down = inst_diff_down

            if (self.var_inst < self.inst_up and self.variacao > 0) or self.var_inst < self.inst_down or self.variacao < diff_down or self.hora_atual > 1555:
                return True

        self.variacao_anterior = self.variacao

        return False 
  
        

    def setAnterior(self):

        if self.valor_anterior == 0:
            self.valor_anterior = float(self.valores[2])
            writeFile("%s:ANTERIOR:%.2f" % (self.code,self.valor_anterior), f=out, end = "\n")
    
    def buyStock(self):

        if self.compra == False:
                # GET VALOR ABERTURA

                self.valor_abertura = float(self.valores[3])
                writeFile("%s:ABERTURA:%.2f" % (self.code,self.valor_abertura), f=out, end = "\n")
                self.compra = True

                # GET COMPRA
                
                if self.valor_abertura >= self.valor_anterior:
                    # Mercado en alta.
                    self.valor_compra = self.valor_atual
                    writeFile("%s:COMPRA:%.2f" % (self.code,self.valor_compra), f=out, end = "\n")
                    sendMail("COMPRA","Valor Anterior: %.2f \n Valor Compra: %.2f \n Total: $%.2f" % (self.valor_anterior,self.valor_compra,self.budget))
                    self.success = True

                else:
                    writeFile("%s:ABORT" % (self.code), f=out, end = "\n")
                    writeFile('\n%s:%02d/%02d/%02d,%2.f,,, %.4f' % (self.code, time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year,self.valor_anterior,self.budget), end = ';')
                    sendMail("ABORTED","Mercado em baixa \n Valor Anterior: %.2f \n Valor Abertura: %.2f \n Valor Final: %2f" % (self.valor_anterior,self.valor_abertura,self.budget))
                    self.success = False 
                

    def sellStock(self,var):

        if self.success == True:
            self.variacao = var(self.valor_atual,self.valor_compra)
        
            if self.venda == False:

                print("selling")

                if self.checkValue(var):
                    self.valor_venda = self.valor_atual
                    self.earn = (self.budget / self.valor_compra) * self.valor_venda
                    
                    writeFile("\n%s:%02d/%02d/%02d:%.2f,%.2f,%.2f,%s:%s,%.2f,%.4f%%,%.4f" % (self.code, time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year,self.valor_anterior,float(self.valor_abertura),float(self.valor_compra),str(self.hora_atual)[:2],str(self.hora_atual)[2:], self.valor_venda, self.variacao,self.earn), end=";")
                    sendMail("VENDA","Valor Venda: % .2f \n Variacao: %.4f \n Resultado Final: $%.2f" % (self.valor_venda,self.variacao,self.earn))
                    
                    self.budget = self.earn                
                    self.venda = True 

#----------------------------------------------------------- Program starts here -------------------------------------------------------------------#

var = varCalc

stocklist = []
out = "data_out.txt"

for code in codes:
    stocklist.append(Stock(code,budget))

def run():

    writeFile("%02d/%02d/%02d:" % (time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year), f=out, form="w",end="\n")

    hora = setTime()

    for s in stocklist:
        s.reset()
        s.success = True

    while setTime() < 1600:

        hora = setTime()

        for s in stocklist:

            if s.success == True and s.loadSite() == True:

                if s.checkTime(hora) == False:
                    stocklist.remove(s)

                print("%s:loaded" % (s.code))

                s.setAnterior()
                s.buyStock()
                s.sellStock(var)
                if hasattr(s,'variacao'):
                    writeFile("%i-->%s:CURRENT VALUE:%s;VARIACAO:%s" % (s.hora_atual, s.code, str(s.valor_atual), str(s.variacao)),out,end = "\n")
                    if s.variacao > 0.2 and s.venda == True :
                        s.reset()
                
    
        time.sleep(55)


open_time = 9*60
close_time = 16*60

while True:

    if time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6:
        weekend = True

    current_time = (time.localtime().tm_hour*60) + time.localtime().tm_min

    if current_time < 60:
        current_time = 1440 - current_time

    d_time = (1440 - current_time) + open_time

    if (current_time >= open_time) and (current_time <= close_time) and (already_ran == False) and (weekend == False):
        run()
        already_ran = True

    else:

        if current_time < open_time:
            d_time = open_time - current_time

        if time.localtime().tm_wday == 5:
            d_time = (2880 - current_time) + open_time

        if d_time < open_time:
                already_ran = False
                weekend = False

        print("Wait %02d:%02d" % (round(d_time/60),d_time%60))
        time.sleep(59)

