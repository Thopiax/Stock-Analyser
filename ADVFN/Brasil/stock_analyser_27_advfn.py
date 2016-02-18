###############################--------##################################
# 1.0.0: Originial (past file) - 2013
# 1.0.1: quickened config - 1/10/15

###############################--------##################################

#FILES#

import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read('confi.ini')
config_dict=['names','address','codes','FROM','TO','EMAIL','PASSWORD','budget','diff_up','diff_down','log','path','day_delay']

for i in config_dict:
    exec i + "=Config.get('DEFAULT',i)"


budget, diff_up, diff_down, day_delay=float(budget),float(diff_up),float(diff_down),int(day_delay)

budget_available = budget

already_ran=False
weekend = False

def readFile(sep=",",file=log): #Name of the file, Seperator of data, Boolean to see if file is a .config
    
    global valor_list
    global read
    
    valor_list = []
    read = ""
    data_file = True

    try:
        with open(file,'r') as data:
            try:
                read = data.readlines()[-1]
            except IndexError:
                data_file = False
                return data_file

            valor_list = read.split(sep)

    except:
        open(file,'w')

def writeFile(text, f=log, form = 'a',end = ','):

        with open(f,form) as data:
            data.write(text + end)

#WEB#


def loadSite(address=address,ini='quoteElementPiece4',end='quoteElementPiece11',end_num = 50):
    try:
        site = urllib.urlopen(address).read().decode('utf8') #Loads web
    except:
        global valores
        valores = []
    else:
        global valores
        valores = re.findall(r'\b\d+\b', site[site.find(ini):(site.find(end))+(end_num)])

def sendMail(SUBJECT = "",TEXT = ""): ## FUNCTION FACILITATING

        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        
        msg = MIMEMultipart()

        msg['From'] = FROM
        msg['To'] = TO
        msg['Subject'] = SUBJECT

        with open(log,'r') as data:
            text = """%s
            
%s""" % (TEXT,data.read())


        msg.attach(MIMEText(text))

        mailServer = smtplib.SMTP("smtp.1and1.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(EMAIL, PASSWORD)
        mailServer.sendmail(EMAIL, TO, msg.as_string())
        # Should be mailServer.quit(), but that crashes...
        mailServer.close()

def varCalc(first,last):
    var = ((first - last)/last)*100.
    return var
        

#----------------------------------------------------------- Program starts here -------------------------------------------------------------------#

def run():

    global venda_done
    global budget_available

    valor_abertura,valor_anterior,valor_compra,valor_venda = 0,0,0,0

    var = varCalc

    out = "data_out.txt"
    writeFile('',out,'w','')

    #CHECK LOG/DATA FOR CONFLICTS

    readFile()

    budget_available = float(valor_list[-1][:-1])

    try:

        if read[-1:] != ";":

            valor_anterior = float(valor_list[1])
            valor_abertura = float(valor_list[2])
            valor_compra = float(valor_list[3])

    except:
        pass

    if valor_list[0] == str('%02d/%02d/%04d' % (time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year)):
        already_ran = True
        return already_ran

    
#LOAD WEBSITE

    try:
        loadSite()

    except IndexError:
        writeFile('IndexError',out,end ='\n')
        return 

    if valor_anterior == 0:
        valor_anterior = float(valores[-5] +'.' + valores[-4])
        writeFile("\n%02d/%02d/%02d,%.2f" % (time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year,valor_anterior))

    while valor_venda == 0:

        try:
            loadSite()
        except:
            time.sleep(60)
            loadSite()

        valor_atual = float(valores[4] + '.' +valores[5])
        hora_atual = int(str(valores[-3]) + str(valores[-2]))

        if len(valores) < 17:
            time.sleep(59)
            writeFile('-------TOO EARLY------',out,end='\n')

        else:
        
            if valor_compra == 0:
                # GET VALOR ABERTURA
                valor_abertura = float(valores[10] +'.' + valores[11])
                writeFile("%.2f" % valor_abertura)

                # GET COMPRA
                
                if valor_abertura >= valor_anterior:
                    # Mercado en alta.
                    valor_compra = valor_atual
                    writeFile("%.2f" % (float(valor_compra)))
                     
                    sendMail("COMPRA","Valor Anterior: %.2f \n Valor Compra: %.2f \n Total: R$%.2f" % (valor_anterior,valor_compra,budget_available))
                
                else:
                    writeFile(',,,, %.4f' % (budget_available), end = ';')
                    sendMail("ABORTED","Mercado em baixa \n Valor Anterior: %.2f \n Valor Abertura: %.2f \n Valor Final: %2f" % (valor_anterior,valor_abertura,budget_available))
                    return

            else:
                variacao = var(valor_atual,valor_compra)
                
                if (variacao > diff_up) or (variacao < diff_down) or (hora_atual > 1630): 
                    
                    valor_venda = valor_atual
                    earn = (budget_available / valor_compra) * valor_venda
                    
                    writeFile("%s:%s,%.2f,%.4f" % (str(hora_atual)[:2],str(hora_atual)[2:], valor_venda, variacao) + '%,' + "%.4f" % (earn), end=";")
                    sendMail("VENDA","Valor Venda: %.2f \n Variacao: %.4f \n Resultado Final: R$%.2f" % (valor_venda,variacao,earn))
                    
                    budget_available = earn
                    budget = earn

                    already_ran = True
                    
                    return

                else:
                    print(str(hora_atual) + "-->CURRENT VALUE:%s;VARIACAO:%s" % (str(valor_atual), str(variacao)))
                    writeFile(str(hora_atual) + "-->CURRENT VALUE:%s;VARIACAO:%s" % (str(valor_atual), str(variacao)),out,end = "\n")
                    time.sleep(59)        

import time, urllib, re, smtplib, os, sys

print (sys.version)

open_time = ((10+ day_delay)*60)
close_time = ((17+ day_delay)*60)

while True:

    if time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6:
        weekend = True

    current_time = (time.gmtime().tm_hour*60) + time.gmtime().tm_min

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

