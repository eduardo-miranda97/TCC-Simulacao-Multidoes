#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys
import statistics

def cv(lista):
	return round(float(100*float(statistics.stdev(lista))/float(statistics.mean(lista))),2)

nome_arquivo = sys.argv[1]

colunas = []

Arq = open(nome_arquivo, "r")

for linha in Arq:

	#ignora linha inicial
	if(("RUNTIME" in linha)):
		for it in linha.split("\t"):
			colunas.append(it.strip())
		qtd_colunas = len(colunas)
		listas = [] 
		for i in range(qtd_colunas):
			listas.append([])
		continue

	conteudo = linha.split("\t")
	if conteudo[0][0] != '#':
		for i in range(qtd_colunas):
			listas[i].append(float(conteudo[i]))

Arq.close()


for i in range(qtd_colunas):
	plt.figure()
	plt.title("Boxplot: "+colunas[i])
	plt.boxplot(listas[i])
	plt.savefig('plot_'+colunas[i]+'.png')
	plt.close()

for i in range(qtd_colunas):
	string = ''
	Arq = open('estatisticas_'+colunas[i]+'.txt', "w")
	string += 'Min\t'+str(min(listas[i]))+'\n'
	string += 'Max\t'+str(max(listas[i]))+'\n'
	string += 'Mean\t'+str(statistics.mean(listas[i]))+'\n'
	string += 'Median\t'+str(statistics.median(listas[i]))+'\n'
	string += 'Variance\t'+str(statistics.variance(listas[i]))+'\n'
	string += 'Desvio Padrão\t'+str(statistics.stdev(listas[i]))+'\n'
	string += 'Coeficiente de Variação\t'+str(cv(listas[i]))+'\n'
	Arq.write(string)
	Arq.close()

string = ''
string += '-\tMin\tMédia\tMediana\tMax\tVariância\tDP\tCV\t\n'

for i in range(qtd_colunas):
	string += colunas[i] + '\t' + str(round(min(listas[i]),2)) + '\t' + str(round(statistics.mean(listas[i]),2)) + '\t' + str(round(statistics.median(listas[i]),2)) + '\t' + str(round(max(listas[i]),2)) + '\t' + str(round(statistics.variance(listas[i]),2)) + '\t' + str(round(statistics.stdev(listas[i]),2))+ '\t' + str(cv(listas[i])) + '\n'

Arq = open('estatisticas.txt','w')
Arq.write(string)
Arq.close()
