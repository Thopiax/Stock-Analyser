#FILES#
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read('config_stocks.cfg')
config_dict=['names','addresses','historic_addresses','codes','FROM','TO','EMAIL','PASSWORD','budget','diff_up','diff_down','log','path','day_delay']

for i in config_dict:
    exec i + "=Config.get('DEFAULT',i)"

budget, diff_up, diff_down, day_delay=float(budget),float(diff_up),float(diff_down),int(day_delay)
budget_available = budget
TO, names, addresses, historic_addresses, codes = TO.split(","), names.split(","), addresses.split(","), historic_addresses.split(","), codes.split(",")

already_ran=False
weekend = False

class stock(object):
    def __init__(self,name,address,historic_address,code):

        self.name = name
        self.address = address
        self.historic_address = historic_address
        self.code = code
        self.string = ""

        self.valor_abertura,self.valor_anterior,self.valor_compra,self.valor_venda = 0,0,0,0

        self.compra_done, self.venda_done = False, False

    def loadSite(self,ini='<tbody>',end='</tbody>',end_num = 0,historic=False):
        site = urllib.urlopen(self.address).read().decode('utf8') #Loads web
        if historic == False:
            self.valores= re.findall(r'\b\d+\b', site[site.find(ini):(site.find(end))+(end_num)])
        else:
            self.valores_historic= re.findall(r'\b\d+\b', site[site.find(ini):(site.find(end))+(end_num)])

    def sendMail(self,SUBJECT = "",TEXT = ""): ## FUNCTION FACILITATING
        
        server = smtplib.SMTP('smtp.1and1.com', 587)
        #Next, log in to the server
        server.login(EMAIL, PASSWORD)
        
        #Send the mail
        msg = """\
            From: %s
            To: %s
            Subject: %s
            
            %s 
            \n
            %s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT) # The /n separates the message from the headers
        
        server.sendmail(EMAIL, TO , msg)
        server.quit()

stocks = []

for name in names:
    stocks.append(stock(name,addresses[names.index(name)],historic_addresses[names.index(name)],codes[names.index(name)]))


def writeFile(text, form = 'a',end = ','):

    with open(log,form) as data:
        data.write(text + end)

#WEB#


#----------------------------------------------------------- Program starts here -------------------------------------------------------------------#

def run():

    date = time.localtime()
    days=1

    done_list = []
    venda_done = False

    for stock in stocks:
        stock.valor_abertura,stock.valor_anterior,stock.valor_compra,stock.valor_venda = 0,0,0,0
        stock.compra_done, stock.venda_done = False, False

# SET ANTERIOr

    
    today = '%d/%02d/%04d' % ((date.tm_mday)-days, date.tm_mon, date.tm_year)

    for stock in stocks:
        stock.loadSite(today,today,1000,True)

        if bool(stock.valores_historic) == False:
            days = days+1
            today = '%d/%02d/%04d' % ((date.tm_mday)-days, date.tm_mon, date.tm_year)
            stock.loadSite(today,today,1000,True)


        stock.valor_anterior = float(stock.valores_historic[3] + '.' + stock.valores_historic[4])
        stock.string_anterior = "\n%02d/%02d/%02d,%s,%.2f" % (date.tm_mday,date.tm_mon,date.tm_year,stock.name,stock.valor_anterior)

    while venda_done == False:

        done_list = []

        for stock in stocks:

            done_list.append(stock.venda_done)

            if stock.venda_done == False:

                stock.loadSite()
                stock.valor_atual = float(stock.valores[6] + '.' +stock.valores[7])

                hora_atual = int(str(date.tm_hour+day_delay)+str(date.tm_min))
                
                if stock.compra_done == False:
                    # GET VALOR ABERTURA
                
                    stock.valor_abertura = float(stock.valores[12] +'.' + stock.valores[13])
                    stock.string = stock.string + ("%.2f" % stock.valor_abertura)

                    # GET COMPRA
                    
                    if stock.valor_abertura > stock.valor_anterior:
                        # Mercado en alta.
                        stock.valor_compra = stock.valor_atual
                        stock.string_compra = ("%.2f" % (float(stock.valor_compra)))
                        
                        #stock.sendMail(("COMPRA - "+ stock.name),("Valor Anterior: %.2f \n Valor Compra: %.2f \n Total: R$%.2f" % (stock.valor_anterior,stock.valor_compra,budget)))
                        stock.compra_done = True
                    
                    else:
                        stock.string = stock.string_anterior + (',,,, %.4f' % (budget))
                        #stock.sendMail("ABORTED - "+ stock.name,"Mercado em baixa \n Valor Anterior: %.2f \n Valor Abertura: %.2f \n Valor Final: %2f" % (stock.valor_anterior,stock.valor_abertura,budget))

                        stock.compra_done = True

                        writeFile(stock.string,end=";")

                else:
                    stock.variacao = ((stock.valor_atual - stock.valor_compra) / stock.valor_compra)* 100.

                    if (stock.variacao > diff_up) or (stock.variacao < diff_down) or (hora_atual > 1650): 
                        
                        stock.valor_venda = stock.valor_atual
                        earn = (budget_available / stock.valor_compra) * stock.valor_venda
                        
                        stock.string_venda = ("%02d:%02d,%.2f,%.4f" % (round(hora_atual/60),hora_atual%60, stock.valor_venda, stock.variacao) + '%,' + "%.4f" % (earn))
                        writeFile(stock.string_anterior + stock.string_compra+stock.string_venda,end=";")

                        #stock.sendMail("VENDA - " + stock.name,"Valor Venda: %.2f \n Variacao: %.4f \n Resultado Final: R$%.2f" % (stock.valor_venda,variacao,earn))
                        budget = earn

                        stock.venda_done = True

            if all(done_list):
                venda_done = True
                return  
                print("wait...")
                time.sleep(59)

import time, urllib, re, smtplib, os, sys

open_time = ((10+ day_delay)*60)
close_time = ((17+ day_delay)*60)

while True:

    if time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6:
        weekend = True
        print(weekend)

    current_time = (time.gmtime().tm_hour*60) + time.gmtime().tm_min
    d_time = (1440 - current_time) + open_time

    if (current_time >= open_time) and (current_time <= close_time) and (already_ran == False) and (weekend == False):
        run()

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
