addresses = "http://br.advfn.com/bolsa-de-valores/bovespa/vale-VALE5/cotacao"

import urllib, re, time

def loadSite(addresses=addresses,ini='quoteElementPiece4',end='quoteElementPiece11',end_num = 50):
        site = urllib.urlopen(addresses).read().decode('utf8') #Loads web
        global valores
        valores = re.findall(r'\b\d+\b', site[site.find(ini):(site.find(end))+(end_num)])

while True:
	loadSite()
	print(valores)
	hora_atual = int(str(valores[-3]) + str(valores[-2]))
	print(hora_atual)
	time.sleep(60)