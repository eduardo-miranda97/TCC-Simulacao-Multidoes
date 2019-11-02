# -*- coding:utf-8 -*-
'''
Created on 15 de set de 2017

@author: Guilherme C.
@author: Eduardo Miranda
'''

#from PIL import Image
#from PIL import ImageDraw
#from tkinter import Button
#from tkinter import Canvas
#import time
from random import randint
from numpy import random
from copy import deepcopy
from Individuo import Individuo
from tkinter import Frame
from Util import Util
from Mapa import Mapa
from Logs import Logs
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import os
import datetime

class Simulacao(Frame):

    def __init__(self, dados):
        '''Constructor'''
        self.dados = []
        self.listaMapas = []
        self.listaIndividuos = dados.LISTA_INDIVIDUOS
        self.listaIndividuosInicial = []
        self.listaMapasIndividuosInicial = []
        self.listaFogo = []
        self.dados = dados
        self.tempo = 0
        self.data = datetime.datetime.today()
        self.diretorio = self.data.strftime('./%Y_%m_%d_%H_%M_%S')
        self.listaQtdIndSairam = []
        self.mediaDistanciaSaida = []

        self.lstDistPorClasse = {}
        self.qtdSairamPorClasse = {}
        for classe in self.dados.CLASSES:
            self.lstDistPorClasse[classe] = []
            self.qtdSairamPorClasse[classe] = []
            self.qtdSairamPorClasse[classe].append(0)

        #self.diretorioImagens = self.diretorio+'/imagens/'
        
        self.MovsPerIter  = 0
        self.CrowdPerIter = 0
        self.carregaMapas()
        self.iniciaSimulacao()

    def carregaMapas(self):
        self.listaMapas = []

        #para cada um dos mapas informados cria-se um novo objeto e adciona a uma lista
        #print("Carregando Mapas")
        for i in range(self.dados.DIRETORIO_MAPAS.__len__()):
            newMapa = Mapa(i, self.dados.DIRETORIO_MAPAS[i], self.dados.DIRETORIO_MAPAS_FOGO[i], self.dados.DIRETORIO_MAPAS_VENTO[i], self.filtraTeleportes(i), self.dados)
            self.listaMapas.append(newMapa)
            if self.dados.FLAG_ATIVACAO_FOGO:
                self.listaFogo.append([])
            #print("Mapa: "+ str(i)+" Carregado com sucesso")
            #newMapa.imprimeMapaEstatico()


    def exportaGraficos(self, diretorio, ind):
        diretorioFinal = diretorio+'/'+str(ind)+'/'
        
        plt.xlabel("Tempo (em Iterações)")
        plt.ylabel("Número de Indivíduos")
        plt.title("Quantidade Acumulada de Indivíduos que Evacuaram o\n Ambiente ao Longo do Tempo (Global)")
        plt.grid(True)
        plt.plot(self.listaQtdIndSairam)
        plt.savefig(diretorioFinal+"cumIndsSairam.png")
        plt.close()

        arqSaida = open(diretorioFinal+str('cumIndsSairam.dat'),'w')
        arqSaida.write('Iter\tQTD ind sairam\n')
        for i in range(len(self.listaQtdIndSairam)):
            arqSaida.write(str(i)+'\t'+str(self.listaQtdIndSairam[i])+'\n')
        arqSaida.close()
        
        #///////////////////////////////////////////////////////////////

        plt.xlabel("Tempo (em Iterações)")
        plt.ylabel("Distância média (Em Células)")
        plt.title("Distância média entre multidão e a saida mais próxima (Global)")
        plt.grid(True)
        plt.plot(self.mediaDistanciaSaida)
        plt.savefig(diretorioFinal+"distMedSaida.png")
        plt.close()

        arqSaida = open(diretorioFinal+str('distMedSaida.dat'),'w')
        arqSaida.write('Iter\tDist media saidas\n')
        for i in range(len(self.mediaDistanciaSaida)):
            arqSaida.write(str(i)+'\t'+str(self.mediaDistanciaSaida[i])+'\n')
        arqSaida.close()

        #///////////////////////////////////////////////////////////////

        disct = dict()
        for i in range(self.tempo):
            disct.update({i:0})


        
        for ind in self.listaIndividuos:
                disct[ind.iteracoesGastas-1] += 1

        '''
        #Comeca o agrupamento para mostragem da curva
        qtdDeDivisoes = int((self.tempo)/5)
        maximo = list(disct.keys())[-1]
        divisor = int(maximo / qtdDeDivisoes) + 1
        lista = []
        y = []
        for i in range(qtdDeDivisoes):
            y.append(i*divisor)
            lista.append(0)

        for key, value in disct.items():
            lista[key // divisor] += value

        while lista[-1] == 0:
            del lista[-1]
            del y[-1]
        '''

        #print(disct.keys())
        #print(disct.items())
        plt.xlabel("Tempo (em iterações)")
        plt.ylabel("Vazão (Indivíduos/Iteração)")
        plt.title("Vazão observada no ambiente ao longo do tempo")
        plt.plot(list(disct.keys()), list(disct.values()))
        plt.savefig(diretorioFinal+"iterGastas.png")
        plt.close()

        arqSaida = open(diretorioFinal+str('iterGastas.dat'),'w')
        arqSaida.write('Iter\tQtd pessoas sairam\n')
        for it,qtd in disct.items():
            arqSaida.write(str(it)+'\t'+str(qtd)+'\n')
        arqSaida.close()   
        
        #///////////////////////////////////////////////////////////////////

        plt.xlabel("Tempo (em Iterações)")
        plt.ylabel("Distância média (Em Células)")
        plt.title("Distância média entre multidão e a saida mais próxima (Por classe)")
        legendas = []
        for classe in self.dados.CLASSES:
            cor = self.transformaRGB(self.dados.CORES[classe])
            plt.plot(self.lstDistPorClasse[classe], label=classe, color=cor)
            legenda = mpatches.Patch(color=cor, label=classe)
            legendas.append(legenda)
        plt.legend(handles=legendas)
        plt.savefig(diretorioFinal+"distanciaPorClasse.png")
        plt.close()

        arqSaida = open(diretorioFinal+str('distanciaPorClasse.dat'),'w')
        string = 'Iter'
        for classe in self.dados.CLASSES:
            string += '\t'+classe
        string += '\n'
        arqSaida.write(string)
        for it in range(self.tempo):
            string = str(it) 
            for classe in self.dados.CLASSES:
                string += '\t'+str(self.lstDistPorClasse[classe][it])
            string += '\n'
            arqSaida.write(string)
        arqSaida.close()

        #////////////////////////////////////////////////////////////////////////////

        plt.xlabel("Tempo (em Iterações)")
        plt.ylabel("Número de Indivíduos")
        plt.title("Quantidade Acumulada de Indivíduos que Evacuaram o\n Ambiente ao Longo do Tempo (Por Classe)")
        legendas = []
        for classe in self.dados.CLASSES:
            cor = self.transformaRGB(self.dados.CORES[classe])
            plt.plot(self.qtdSairamPorClasse[classe], label=classe, color=cor)
            legenda = mpatches.Patch(color=cor, label=classe)
            legendas.append(legenda)
        plt.legend(handles=legendas)
        plt.savefig(diretorioFinal+"qtdSairamPorClasse.png")
        plt.close()

        arqSaida = open(diretorioFinal+str('qtdSairamPorClasse.dat'),'w')
        string = 'Iter'
        for classe in self.dados.CLASSES:
            string += '\t'+classe
        string +='\n'
        arqSaida.write(string)
        for it in range(self.tempo):
            string = str(it) 
            for classe in self.dados.CLASSES:
                string += '\t'+str(self.qtdSairamPorClasse[classe][it])
            string += '\n'
            arqSaida.write(string)
        arqSaida.close()


    def transformaRGB(self,cor):
        cor0=0; cor1=0; cor2=0
        if cor[0] == 0:
            cor0 = 0
        else:
            cor0 = cor[0]/255
        if cor[1] == 0:
            cor1 = 0
        else:
            cor1 = cor[1]/255
        if cor[2] == 0:
            cor2 = 0
        else:
            cor2 = cor[2]/255

        return (cor0,cor1,cor2)

    
    def iniciaSimulacao(self):
        
        self.geraIndividuosAleatoriamente()
        #self.geraFogoInicial()
        for ind in range(self.dados.QTD_REPLICACACOES):
            self.carregaMapas()
            #self.geraIndividuosAleatoriamente()
            if self.dados.FLAG_ATIVACAO_FOGO:
                self.geraFogoInicial()

            self.diretorioImagens = self.diretorio+"/"+str(ind)+'/imagens/'
            os.makedirs(self.diretorioImagens)
            logs = Logs(self.diretorio, ind)
            #print("Replicacao numero "+str(ind))
            #logs.gravaNumReplicacao(ind)
            #logs.gravaCabecalho(self.dados.QTD_PESSOAS)
            self.tempo = 0
            self.atribuiMapaIndividuoInicial()
            #self.geraIndividuosAleatoriamente()

            logs.abreMovsPerIter()
            self.simulacao(logs)
            logs.fechaMovsPerIter()

            KPIs = logs.printaKPIs(self.listaIndividuos, self.dados.FLAG_ATIVACAO_FOGO)

            logs.geraHTML(self.data, self.tempo, self.listaIndividuos.__len__(), self.listaMapas.__len__(), KPIs, self.dados.FLAG_ATIVACAO_FOGO)
            #print("Simulacao Finalizada com sucesso com Tempo = " + str(self.tempo))
            #print(str(ind)+"\t"+str(self.tempo));
            logs.geraResultado(ind, self.tempo)

            self.exportaGraficos(self.diretorio, ind)
        #imprime resultado do mapa dinamico 1 
        #for i in range(self.listaMapas.__len__()):
            #print('Mapa Parede: ' + str(i))
            #self.listaMapas[i].imprimeMapaDinamico1()
            #self.listaMapas[i].imprimeMapaParedes()

            
    def simulacao(self, logs):

        #Primeiro calculo do mapa de calor
        if self.dados.FLAG_ATIVACAO_FOGO:
            for i in range(self.listaMapas.__len__()):
                self.listaMapas[i].calculaMapaCalor(self.listaFogo[i])
                #self.listaMapas[i].calculaMapaEstaticoAndCalor(self.listaFogo[i], Util.CALOR_MAPA)

            self.atualizaVitalidade()

        #Começa a simulação propiamente dita
        #while(not self.verificaIndividuosEvacuados()):
        while(not self.verificaIndividuosEvacuados() and self.tempo < 1200):
            self.desenhaMapa(self.tempo)
            self.tempo = self.tempo + 1
            listaIndividuosTeleporte = []
            if(self.dados.GERAR_LOG == 1):
                print("Tempo: " + str(self.tempo))
            self.ordenaIndividuosPorDistancia()

            self.MovsPerIter  = 0
            self.CrowdPerIter = 0
            qtdIndSaiu = 0

            for classe in self.dados.CLASSES:
                self.qtdSairamPorClasse[classe].append(self.qtdSairamPorClasse[classe][-1])

            for ind in self.listaIndividuos:
                # Incrementa a quantidade de passos para o individuo se mover com base no deslocamento
                ind.qtdPassos += 1
                if(not ind.saiu):
                    ind.iteracoesGastas += 1
                    if ind.qtdPassos == ind.deslocamento:
                        self.CrowdPerIter += 1
                        self.moveIndividuo(ind)
                        if(self.listaMapas[ind.idMapa].isTeleporte(ind.linha, ind.coluna)):
                            if(self.dados.GERAR_LOG == 1):
                                print("Teleporte Individuo "+str(ind.idNum)+" no mapa "+str(ind.idMapa))
                            listaIndividuosTeleporte.append(ind)
                        if(self.listaMapas[ind.idMapa].isSaida(ind.linha, ind.coluna)):
                            if(self.dados.GERAR_LOG == 1):
                                print("Saida Individuo "+str(ind.idNum)+" Saiu")
                            ind.saiu = True
                            qtdIndSaiu += 1
                            self.qtdSairamPorClasse[ind.classeIndividuo][-1] += 1
                        ind.qtdPassos = 0

            # Calculo dos KPIs graficos
            if self.listaQtdIndSairam:
                self.listaQtdIndSairam.append(qtdIndSaiu + self.listaQtdIndSairam[-1])
            else:
                self.listaQtdIndSairam.append(qtdIndSaiu)
                
            self.mediaDistanciaSaida.append(self.calculaMediaDistancia())
            self.calculaMediaDistanciaPorClasse()

            #logs.gravaMovsPerIter(self.tempo, self.MovsPerIter, self.CrowdPerIter)            
            #ao finalizar o movimento possivel de todos os individuos libera os individuos que chegaram a saida
            #gera os logs das posicoes de cada individuo
            self.liberaSaidas()
            self.realizaTeleportes(listaIndividuosTeleporte)
            #logs.gravaIteracao(self.tempo, self.listaIndividuos)
            #depois dos movimentos eh realizado o calibramento dos mapas dinamicos
            #calibrando campos dinamicos, de fogo e de fumaca
            oldMapas1 = []  #dinamico
            oldMapas2 = []  #fogo
            oldMapas3 = []  #fumaca
            for m in self.listaMapas:
                oldMapas1.append(deepcopy(m.mapa_dinamico1))
                if self.dados.FLAG_ATIVACAO_FOGO:
                    oldMapas2.append(deepcopy(m.mapa_fogo))
                    oldMapas3.append(deepcopy(m.mapa_vento))

            #print("Entrei iter = "+str(self.tempo))
            for i in range(self.listaMapas.__len__()):
                self.difusaoDecaimento(oldMapas1[i], self.listaMapas[i].mapa_dinamico1)
                if self.dados.FLAG_ATIVACAO_FOGO:
                    self.espalhaFogo(oldMapas2[i], self.listaMapas[i].mapa_fogo, i)
                    self.listaMapas[i].calculaMapaCalor(self.listaFogo[i])
                    #self.listaMapas[i].calculaMapaEstaticoAndCalor(self.listaFogo[i],Util.CALOR_MAPA)
                    self.listaMapas[i].desenhaMapaCalor(self.tempo-1, self.diretorioImagens)
                    #self.espalhaFumaca(oldMapas3[i], self.listaMapas[i].mapa_vento, oldMapas2[i])

            #print(self.listaMapas[i].mapa_calor)
            if self.dados.FLAG_ATIVACAO_FOGO:
                self.atualizaVitalidade()


    def geraFogoInicial(self):

        if self.dados.FLAG_FOGO_INICIAL == 1:
            for idMapa, linha, coluna in self.dados.LISTA_FOCOS:
                self.listaMapas[idMapa].mapa_fogo[linha][coluna][Util.FS_STATE] = Util.FIRE_BURNING
                self.listaFogo[idMapa].append([linha,coluna])

            return 1

        for _ in range(self.dados.QTD_FOCOS_INCENDIO):

            # Escolhe qual mapa irá iniciar o fogo
            idMapa = randint(0, self.listaMapas.__len__() - 1)

            # Sorteia até que um local válido seja usado
            while True:
                coluna = randint(0, self.listaMapas[idMapa].tam_colunas - 1)
                linha = randint(0, self.listaMapas[idMapa].tam_linhas - 1)
                
                if self.listaMapas[idMapa].mapa_objetos[linha][coluna] == Util.M_VAZIO or self.listaMapas[idMapa].mapa_objetos[linha][coluna] == Util.M_DESENHO:
                    break

            # Escolhido um valor válido, inciderar célula
            self.listaMapas[idMapa].mapa_fogo[linha][coluna][Util.FS_STATE] = Util.FIRE_BURNING
            self.listaFogo[idMapa].append([linha, coluna])
    
    def espalhaFogo(self, oldMapa, newMapa, idMapa):
        for i in range(1, newMapa.__len__()-1):
            for j in range(1, newMapa[0].__len__()-1):

                if self.listaMapas[idMapa].mapa_objetos[i][j] == Util.M_PAREDE or self.listaMapas[idMapa].mapa_objetos[i][j] == Util.M_VOID:
                    continue

                if oldMapa[i][j][Util.FS_STATE] == Util.FIRE_EMPTY:
                    newMapa[i][j][Util.FS_STATE] = Util.FIRE_EMPTY

                elif oldMapa[i][j][Util.FS_STATE] == Util.FIRE_BURNING:
                    newMapa[i][j][Util.F_PERSIST] = newMapa[i][j][Util.F_PERSIST] - 1
                    newMapa[i][j][Util.FS_STATE] = Util.FIRE_BURNING
                    if oldMapa[i][j][Util.F_PERSIST] <= Util.FIRE_EMPTY:
                        newMapa[i][j][Util.FS_STATE] = Util.FIRE_EMPTY
                        self.listaFogo[idMapa].remove([i, j])

                else:
                    if self.funct_f(oldMapa, i, j, idMapa) > 0.5:
                        newMapa[i][j][Util.FS_STATE]  = Util.FIRE_BURNING
                        newMapa[i][j][Util.F_PERSIST] = newMapa[i][j][Util.F_PERSIST] - 1 
                        self.listaFogo[idMapa].append([i, j])
                    else:
                        newMapa[i][j][Util.FS_STATE] = Util.FIRE_UNBURNED

    def funct_f(self, oldMapa, i, j, idMapa):
        vet = []
        dic = {Util.FIRE_BURNING:1,Util.FIRE_EMPTY:0,Util.FIRE_UNBURNED:0}
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i-1,j-1)):
            prob = (oldMapa[i-1][j-1][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i-1][j-1][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i,j-1)):
            prob = (oldMapa[i][j-1][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i][j-1][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i+1,j-1)):
            prob = (oldMapa[i+1][j-1][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i+1][j-1][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i+1,j)):
            prob = (oldMapa[i+1][j][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i+1][j][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i+1,j+1)):
            prob = (oldMapa[i+1][j+1][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i+1][j+1][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i,j+1)):
            prob = (oldMapa[i][j+1][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i][j+1][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i-1,j+1)):
            prob = (oldMapa[i-1][j+1][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i-1][j+1][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)
        if(self.listaMapas[idMapa].verificaPosicaoVizinhaExiste(i-1,j)):
            prob = (oldMapa[i-1][j][Util.F_STATIC] + 1) * random.uniform(0, 0.5)
            fogoVizinho = dic[oldMapa[i-1][j][Util.FS_STATE]]
            vet.append(prob * fogoVizinho)

        nmax = max(vet)

        if nmax > 0.5 and random.uniform(0, nmax) < nmax * Util.FIRE_RATE:
            return 1

        return 0

    
    def espalhaFumaca(self, oldMapa, newMapa, oldMapaFogo):
        for i in range(1, newMapa.__len__()-1): 
            for j in range(1, newMapa[0].__len__()-1):
                if(oldMapa[i][j][Util.FS_STATE] == Util.SMOKE_BLANK):
                    newMapa[i][j][Util.FS_STATE] = Util.SMOKE_BLANK
                else:
                    if(oldMapa[i][j][Util.FS_STATE] == Util.SMOKE_WITHOUT_SMOKE and random.uniform(0, self.funct_s(oldMapa, i, j)) < 0.5):
                        newMapa[i][j][Util.FS_STATE] = Util.SMOKE_WITHOUT_SMOKE
                    else:
                        if((oldMapa[i][j][Util.FS_STATE] == Util.SMOKE_WITHOUT_SMOKE and random.uniform(0, self.funct_s(oldMapa, i, j)) > 0.5) or 
                           (oldMapa[i][j][Util.FS_STATE] == Util.SMOKE_WITH_SMOKE) or 
                           (oldMapaFogo[i][j][Util.FS_STATE] == Util.FIRE_BURNING)):
                                newMapa[i][j][Util.FS_STATE] = Util.SMOKE_WITH_SMOKE
    
    def funct_s(self, oldMapa, i, j):
        nmax = max([oldMapa[i-1][j-1][Util.S_STATIC] + 0 + random.uniform(0, 0.5), 
                    oldMapa[i][j-1][Util.S_STATIC]   + 0 + random.uniform(0, 0.5), 
                    oldMapa[i+1][j-1][Util.S_STATIC] + 0 + random.uniform(0, 0.5), 
                    oldMapa[i+1][j][Util.S_STATIC]   + 0 + random.uniform(0, 0.5),
                    oldMapa[i+1][j+1][Util.S_STATIC] + 0 + random.uniform(0, 0.5), 
                    oldMapa[i][j+1][Util.S_STATIC]   + 0 + random.uniform(0, 0.5), 
                    oldMapa[i-1][j+1][Util.S_STATIC] + 0 + random.uniform(0, 0.5), 
                    oldMapa[i-1][j][Util.S_STATIC]   + 0 + random.uniform(0, 0.5)])    
        if(nmax > 1):
            return 1
        else:
            return nmax             

    def difusaoDecaimento(self, oldMapa, newMapa):
        for i in range(1, newMapa.__len__()-1):
            for j in range(1, newMapa[0].__len__()-1):
                newMapa[i][j] = oldMapa[i][j] + ((Util.DD_ALFA/4)*(oldMapa[i+1][j] + oldMapa[i-1][j] + oldMapa[i][j+1] + oldMapa[i][j-1] + 
                                                                   oldMapa[i-1][j-1] + oldMapa[i-1][j+1] + oldMapa[i+1][j-1] + oldMapa[i+1][j+1]))
                newMapa[i][j] = oldMapa[i][j] - (Util.DD_SIGMA*oldMapa[i][j])
    

    def atualizaVitalidade(self):
        string = ''
        for ind in self.listaIndividuos:
            '''
            print('Individuo n= '+str(ind.idNum)+' - Vitalidade='+str(ind.vitalidade)+' - Cor='+str(ind.cor)
                +' - calor local= '+str(self.listaMapas[ind.idMapa].mapa_calor[ind.linha][ind.coluna])
                +' - lin,col='+str(ind.linha)+','+str(ind.coluna))
            '''
            #print('Vitalidade ='+str(ind.vitalidade)+' - Bool='+str(ind.vitalidade <= 0)+' - Old Cor='+str(ind.cor))
            ind.vitalidade = ind.diminuiVitalidade(self.listaMapas[ind.idMapa].mapa_calor[ind.linha][ind.coluna])
            ind.deslocamento = ind.corrigeDeslocamento()
            string = string + str(ind.deslocamento) + ' - '

            #Individuo fica como que saiu, quando na verdade ele está morto pelo fogo
            if ind.vitalidade <= 0:
                ind.saiu = True
                ind.cor = self.dados.COR_MORTE
                if not (self.listaMapas[ind.idMapa].mapa_objetos_static[ind.linha][ind.coluna] == Util.M_JANELA
                and self.listaMapas[ind.idMapa].mapa_objetos_static[ind.linha][ind.coluna] == Util.M_PORTA):
                    self.listaMapas[ind.idMapa].mapa_objetos_static[ind.linha][ind.coluna] = Util.M_PAREDE

        #print(string)
            #print('NVitalidade ='+str(ind.vitalidade)+' - NBool='+str(ind.vitalidade <= 0)+' - NCor='+str(ind.cor))
            #Roxo = (150,0,255)
            #Implementar a morte do individuo


    def moveIndividuo(self, ind):
        linha    = ind.linha
        coluna   = ind.coluna
        campoMov = [0,0,0,0,0,0,0,0,0]
        campoMov = self.calculaProbabilidadesMovimentoBruto(linha, coluna, ind, campoMov)
        #Normalizacao
        total = self.calculaTotalNormalizacao(campoMov)
        campoMov = self.calculaProbabilidadesMovimentoNormalizado(campoMov, total)
        caminho = self.sorteiaCaminhoDestino(campoMov)
        resp = self.converteDirecao(ind, caminho)
        direcao = resp[0]
        caminho = resp[1]
        #atualiza no mapa o individuo
        if(caminho[1] != linha or caminho[2] != coluna):
            if(self.listaMapas[ind.idMapa].verificaMovimentoValido(caminho[1], caminho[2])):
                self.MovsPerIter = self.MovsPerIter + 1
                #atualiza os dados no mapa de individuos
                self.listaMapas[ind.idMapa].mapa_individuo[caminho[1]][caminho[2]] = Util.M_INDIVIDUO
                self.listaMapas[ind.idMapa].mapa_individuo[linha][coluna]  = Util.M_VAZIO
                self.listaMapas[ind.idMapa].mapa_dinamico1[linha][coluna] += 1
                #atualiza nos dados do individuo sua posicao
                ind.linha  = caminho[1]
                ind.coluna = caminho[2]
                ind.ultimaDirecao = direcao
                ind.movimentosFeitos += 1
        else:
            ind.movimentosWaiting += 1

    def calculaProbabilidadesMovimentoBruto(self, linha, coluna, ind, campoMov):
        if(self.listaMapas[ind.idMapa].qtdSaidasVizinhas(linha, coluna) == 0):  
            #superior esquerdo - ind 0
            campoMov[Util.C_SE] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha-1, coluna-1, Util.C_SE, ind)
            #superior direito - ind 1
            campoMov[Util.C_SD] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha-1, coluna+1, Util.C_SD, ind)
            #inferior direito - ind 2
            campoMov[Util.C_ID] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha+1, coluna+1, Util.C_ID, ind)
            #inferior esquerdo - ind 3
            campoMov[Util.C_IE] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha+1, coluna-1, Util.C_IE, ind)
            #topo - ind 4
            campoMov[Util.C_TO] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha-1, coluna,   Util.C_TO, ind)
            #baixo - ind 5
            campoMov[Util.C_BA] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha+1, coluna,   Util.C_BA, ind)
            #esquerdo - ind 6
            campoMov[Util.C_ES] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha, coluna-1,   Util.C_ES, ind)
            #direito - ind 7
            campoMov[Util.C_DI] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha, coluna+1,   Util.C_DI, ind)
            #meio - ind 8
            campoMov[Util.C_ME] = self.listaMapas[ind.idMapa].calculaValorMovimentoBruto(linha, coluna,     Util.C_ME, ind)
        else:
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha-1, coluna-1)):
                campoMov[Util.C_SE] = 1
            else:
                campoMov[Util.C_SE] = 0
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha-1, coluna+1)):
                campoMov[Util.C_SD] = 1
            else:
                campoMov[Util.C_SD] = 0
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha+1, coluna+1)):
                campoMov[Util.C_ID] = 1
            else:
                campoMov[Util.C_ID] = 0
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha+1, coluna-1)):
                campoMov[Util.C_IE] = 1
            else:
                campoMov[Util.C_IE] = 0
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha-1, coluna)):
                campoMov[Util.C_TO] = 1
            else:
                campoMov[Util.C_TO] = 0
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha+1, coluna)):
                campoMov[Util.C_BA] = 1
            else:
                campoMov[Util.C_BA] = 0
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha, coluna-1)):
                campoMov[Util.C_ES] = 1
            else:
                campoMov[Util.C_ES] = 0
            if(self.listaMapas[ind.idMapa].isSaidaVazia(linha, coluna+1)):
                campoMov[Util.C_DI] = 1
            else:
                campoMov[Util.C_DI] = 0
            campoMov[Util.C_ME] = 0
            
        return campoMov
    
    def calculaTotalNormalizacao(self, campoMov):
        total = campoMov[Util.C_SE] + campoMov[Util.C_SD] + campoMov[Util.C_ID] + campoMov[Util.C_IE] + campoMov[Util.C_TO]
        return total + campoMov[Util.C_BA] + campoMov[Util.C_ES] + campoMov[Util.C_DI] + campoMov[Util.C_ME]
    
    def calculaProbabilidadesMovimentoNormalizado(self, campoMov, total):
        if(total==0):
            campoMov[Util.C_SE] = 0
            campoMov[Util.C_SD] = 0
            campoMov[Util.C_ID] = 0
            campoMov[Util.C_IE] = 0
            campoMov[Util.C_TO] = 0
            campoMov[Util.C_BA] = 0
            campoMov[Util.C_ES] = 0
            campoMov[Util.C_DI] = 0
            campoMov[Util.C_ME] = 0
        else:
            campoMov[Util.C_SE] = campoMov[Util.C_SE]/total
            campoMov[Util.C_SD] = campoMov[Util.C_SE] + campoMov[Util.C_SD]/total
            campoMov[Util.C_ID] = campoMov[Util.C_SD] + campoMov[Util.C_ID]/total
            campoMov[Util.C_IE] = campoMov[Util.C_ID] + campoMov[Util.C_IE]/total
            campoMov[Util.C_TO] = campoMov[Util.C_IE] + campoMov[Util.C_TO]/total
            campoMov[Util.C_BA] = campoMov[Util.C_TO] + campoMov[Util.C_BA]/total
            campoMov[Util.C_ES] = campoMov[Util.C_BA] + campoMov[Util.C_ES]/total
            campoMov[Util.C_DI] = campoMov[Util.C_ES] + campoMov[Util.C_DI]/total
            campoMov[Util.C_ME] = campoMov[Util.C_DI] + campoMov[Util.C_ME]/total
        return campoMov

    def sorteiaCaminhoDestino(self, campoMov):
        ini = 0
        sort = randint(0, 100)/100
        for i in range(campoMov.__len__()):
            if(sort < campoMov[i] and sort > ini):
                return i
            ini = campoMov[i]

    def converteDirecao(self, ind, caminho):
        #Retorna ["direcao","[caminho]"]
        linha    = ind.linha
        coluna   = ind.coluna
        direcao  = 0
        if(caminho == Util.C_SE):
            linha   = linha-1
            coluna  = coluna-1
            direcao = Util.C_SE
        if(caminho == Util.C_SD):
            linha   = linha-1
            coluna  = coluna+1
            direcao = Util.C_SD
        if(caminho == Util.C_ID):
            linha   = linha+1
            coluna  = coluna+1
            direcao = Util.C_ID
        if(caminho == Util.C_IE):
            linha   = linha+1
            coluna  = coluna-1
            direcao = Util.C_IE
        if(caminho == Util.C_TO):
            linha   = linha-1
            coluna  = coluna
            direcao = Util.C_TO
        if(caminho == Util.C_BA):
            linha   = linha+1
            coluna  = coluna
            direcao = Util.C_BA
        if(caminho == Util.C_ES):
            linha   = linha
            coluna  = coluna-1
            direcao = Util.C_ES
        if(caminho == Util.C_DI):
            linha   = linha
            coluna  = coluna+1   
            direcao = Util.C_DI 
        return [direcao, [self.listaMapas[ind.idMapa].mapa_estatico[linha][coluna], linha, coluna]]

    def realizaTeleportes(self, listaInd):
        #para todos os individuos que estao em um teleporte eles sao movimentados para
        #o novo mapa de destino
        for ind in listaInd:
            trans = self.listaMapas[ind.idMapa].getTransicaoTeleporte(ind.linha, ind.coluna)
            idMapaOrigem  = trans[Util.T_ORIGEM_MAPA]
            linhaOrigem   = trans[Util.T_ORIGEM_LINHA]
            colunaOrigem  = trans[Util.T_ORIGEM_COLUNA]
            idMapaDestino = trans[Util.T_DESTINO_MAPA]
            linhaDestino  = trans[Util.T_DESTINO_LINHA]
            colunaDestino = trans[Util.T_DESTINO_COLUNA]
            if(self.listaMapas[idMapaDestino].isPosicaoVazia(linhaDestino, colunaDestino)):
                self.listaMapas[idMapaDestino].mapa_individuo[linhaDestino][colunaDestino] = Util.M_INDIVIDUO
                self.listaMapas[idMapaOrigem].mapa_individuo[linhaOrigem][colunaOrigem] = Util.M_VAZIO
                ind.idMapa = idMapaDestino
                ind.linha  = linhaDestino
                ind.coluna = colunaDestino

    def liberaSaidas(self):
        #para cada saida neste mapa, todos os individuos nestas posicoes sao evacuados
        for mapa in self.listaMapas:
            for saida in mapa.saidas:
                mapa.mapa_individuo[saida[0]][saida[1]] = Util.M_VAZIO

    def desenhaMapa(self, iteracao):
        #para cada mapa, desenha uma imagem do estado atual do mapa
        for mapa in self.listaMapas:
            #Recalcula o mapa estatico a cada 20 iteracoes
            if iteracao == 0:
               mapa.desenhaDistribuicaoMapaBanner(self.diretorioImagens,iteracao)

            else:
                if iteracao % Util.QTD_ITER_CALC_CAMPO_STATICO == 0:
                    #mapa.calculaMapaEstaticoAndCalor([],Util.ESTATICO_MAPA)
                    if self.dados.FLAG_ATIVACAO_FOGO:
                        mapa.calculaMapaEstatico()
                    mapa.desenhaDistribuicaoMapaBanner(self.diretorioImagens,iteracao)

            mapa.desenhaMapa(iteracao, self.diretorioImagens, self.listaIndividuos)
            mapa.desenhaMapaTracing(iteracao, self.diretorioImagens)
            if self.dados.FLAG_ATIVACAO_FOGO:
                mapa.desenhaMapaFogo(iteracao, self.diretorioImagens)
    
    def verificaIndividuosEvacuados(self):
        #verifica se todos os individuos foram evacuados, se nenhum ainda nao foi evacuado retorna true
        #caso algum ainda esteja saindo dos mapas retorna false
        if self.dados.FLAG_ATIVACAO_FOGO:
            for i in range(self.listaIndividuos.__len__()):
                if(not self.listaIndividuos[i].saiu and self.listaIndividuos[i].movimentosFeitos < 500):
                    return False
            return True

        for i in range(self.listaIndividuos.__len__()):
            if(not self.listaIndividuos[i].saiu):
                return False
        return True
        

    def ordenaIndividuosPorDistancia(self):
        #a ordenacao eh util para que os movimentos dos individuos sejam feitas pelas distancias mais proximas
        self.listaIndividuos.sort(key=self.keySortIndividuo, reverse=False)

    def keySortIndividuo(self, ind):
        #os niveis inferiores serao movimentados primeiro, entao o id do mapa +1(pois eh indexado de 0) sera um peso para o andar
        #quanto menor o valor do campo * idMapa maior eh a prioridade do movimento
        return self.listaMapas[ind.idMapa].mapa_estatico[ind.linha][ind.coluna]*(ind.idMapa+1)

    def filtraTeleportes(self, idMapaOrigem):
        #retorna um objeto com os teleportes com origem do mapa solicidado
        lista = []
        for tele in self.dados.TELETRANSPORTES:
            linha = tele.split("-")
            #converte strings para inteiros    
            aux = []
            for valor in linha:
                aux.append(int(valor))
            linha = aux
            
            if(linha[Util.T_ORIGEM_MAPA] == idMapaOrigem):
                lista.append(linha)
        return lista

    def geraIndividuosAleatoriamente(self):
        #ao iniciar uma simulacao gera a posicao individuos em posicoes aleatorioas em mapas aleatorios
        #print("Carregando "+str(self.dados.QTD_PESSOAS)+" Individuos Aleatoriamente")
        
        for i in range(self.dados.QTD_PESSOAS):

            idMapa = randint(0, self.listaMapas.__len__()-1)
            coluna = randint(0, self.listaMapas[idMapa].tam_colunas-1)
            linha  = randint(0, self.listaMapas[idMapa].tam_linhas-1)
            
            while(not self.verificaPosicaoVazia(idMapa, coluna, linha)):
                idMapa = randint(0, self.listaMapas.__len__()-1)
                coluna = randint(0, self.listaMapas[idMapa].tam_colunas-1)
                linha = randint(0, self.listaMapas[idMapa].tam_linhas-1)

            self.listaIndividuos[i].posicionaIndividuoMapa(coluna, linha, idMapa)

            #self.listaMapas[idMapa].mapa_individuo[linha][coluna] = Util.M_INDIVIDUO
            
            #print("Individuo Gerado | Mapa: " + str(idMapa) + " Linha: " + str(linha) + " Coluna: " + str(coluna))
        #self.listaIndividuosInicial.append(deepcopy(self.listaIndividuos))
        #for i in range(self.dados.DIRETORIO_MAPAS.__len__()):
            #self.listaMapasIndividuosInicial.append(deepcopy(self.listaMapas[i].mapa_individuo))
            #print("Mapa: "+ str(i))
            #self.listaMapas[i].imprimeMapaIndividuo()
            #self.listaMapas[i].imprimeMapaParedes()
    
    def atribuiMapaIndividuoInicial(self):
        
        for ind in self.listaIndividuos:
            self.listaMapas[ind.idMapa].mapa_individuo[ind.linha][ind.coluna] = Util.M_INDIVIDUO
    
    def sorteiaNaRoleta(self, roletaProbabilidades):
        ini = 0
        sort = randint(0, 100)/100
        for i in range(roletaProbabilidades.__len__()):
            if(sort <= roletaProbabilidades[i] and sort >= ini):
                return i
            ini = roletaProbabilidades[i]
    
    def defineCor(self, sexo, tipoIndividuo):
        if(sexo == Util.S_MASCULINO):
            if(tipoIndividuo == Util.IND_ADOLECENTE):
                return self.dados.COR_HOMEM_ADOLECENTE
            elif(tipoIndividuo == Util.IND_JOVEM):
                return self.dados.COR_HOMEM_JOVEM
            elif(tipoIndividuo == Util.IND_ADULTO):
                return self.dados.COR_HOMEM_ADULTO
            elif(tipoIndividuo == Util.IND_IDOSO):
                return self.dados.COR_HOMEM_IDOSO
        elif(sexo == Util.S_FEMININO):
            if(tipoIndividuo == Util.IND_ADOLECENTE):
                return self.dados.COR_MULHER_ADOLECENTE
            elif(tipoIndividuo == Util.IND_JOVEM):
                return self.dados.COR_MULHER_JOVEM
            elif(tipoIndividuo == Util.IND_ADULTO):
                return self.dados.COR_MULHER_ADULTO
            elif(tipoIndividuo == Util.IND_IDOSO):
                return self.dados.COR_MULHER_IDOSO
             
    def verificaPosicaoVazia(self, idMapa, coluna, linha):
        #verifica se a posicao nao eh referente a um local que contenha um objeto, 
        #ou se existe alguma pessoa naquele local
        if(self.listaMapas[idMapa].mapa_objetos[linha][coluna] == Util.M_VAZIO or self.listaMapas[idMapa].mapa_objetos[linha][coluna] == Util.M_DESENHO):
            if(self.listaMapas[idMapa].mapa_individuo[linha][coluna] == Util.M_VAZIO):
                return True
        return False

    def calculaMediaDistancia(self):
        soma = 0.0
        qtdInd = 0.0
        for ind in self.listaIndividuos:
            if not (ind.saiu or ind.vitalidade <= 0):
                soma += self.listaMapas[ind.idMapa].mapa_estatico[ind.linha][ind.coluna]
                qtdInd += 1

        if qtdInd == 0:
            return 0

        return soma / qtdInd

    def calculaMediaDistanciaPorClasse(self):
        
        dicioQTD   = dict()
        for classe in self.dados.CLASSES:
            self.lstDistPorClasse[classe].append(0)
            dicioQTD[classe] = 0

        for ind in self.listaIndividuos:
            if (not ind.saiu) and (ind.vitalidade > 0):
                self.lstDistPorClasse[ind.classeIndividuo][self.tempo-1] += self.listaMapas[ind.idMapa].mapa_estatico[ind.linha][ind.coluna]
                dicioQTD[ind.classeIndividuo] += 1

        for classe, soma in self.lstDistPorClasse.items():
            if dicioQTD[classe] == 0:
                self.lstDistPorClasse[classe][self.tempo-1] = 0
            else:
                self.lstDistPorClasse[classe][self.tempo-1] = soma[self.tempo-1] / dicioQTD[classe]

