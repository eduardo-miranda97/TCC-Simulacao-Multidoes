# -*- coding:utf-8 -*-
'''
Created on 16 de set de 2017

@author: Guilherme C.
@author: Eduardo Miranda
'''

from Util import Util
from PIL import Image
from PIL import ImageDraw
from colour import Color
from copy import deepcopy

import re
import math
import numpy

class Mapa(object):
        
    def __init__(self, num_id, diretorio_mapa, diretorio_mapa_fogo, diretorio_mapa_vento, teleportes, dados):
        '''Constructor'''
        self.id                   = num_id
        self.diretorio_mapa       = diretorio_mapa
        self.diretorio_mapa_fogo  = diretorio_mapa_fogo
        self.diretorio_mapa_vento = diretorio_mapa_vento
        self.teleportes           = teleportes
        self.mapa_objetos         = []
        self.mapa_objetos_static  = []
        self.mapa_estatico        = []
        self.mapa_individuo       = []
        self.mapa_dinamico1       = []
        self.mapa_parede          = []
        self.mapa_fogo            = []
        self.mapa_vento           = []
        self.mapa_calor           = []
        self.saidas               = []
        self.tam_linhas           = 0
        self.tam_colunas          = 0
        self.dados                = dados
        
        self.carregaMapaObjetos()          #carrega do arquivo do mapa todo o conteudo
        self.mapa_objetos_static = deepcopy(self.mapa_objetos)
        self.calculaMapaEstatico()
        #self.calculaMapaEstaticoAndCalor([],Util.ESTATICO_MAPA) #calcula o campo estatico do mapa
        self.carregaMapaIndividuosVazios() #instancia matriz de individuos vazia
        self.carregaMapaDinamico()         #carrega campos dinamicos no mapa
        self.carregaMapaParedes()          #carrega mapa com distancia das paredes
        if self.dados.FLAG_ATIVACAO_FOGO:
            self.carregaMapaFogo()             #carrega mapa de fogo
            self.carregaMapaVento()            #carrega mapa de vento
    
    def carregaMapaObjetos(self):
        #abre o arquivo e carrega o mapa para uma matriz
        arquivo = open(self.diretorio_mapa, 'r')
        
        for linha in arquivo:
            self.mapa_objetos.append(list(linha.strip('\n')))
        
        arquivo.close()
        self.converteMapa() #converte o arquivo para uma matriz de inteiros
        
        self.tam_linhas = self.mapa_objetos.__len__()
        self.tam_colunas = self.mapa_objetos[0].__len__()
    
    def carregaMapaIndividuosVazios(self):
        #instancia a matriz que ira armazenar os individuos
        for i in range(self.tam_linhas):
            linha = []
            for j in range(self.tam_colunas):
                linha.append(Util.M_VAZIO)
                i=i+0;j=j+0   #apenas para remover warning
            self.mapa_individuo.append(linha)
    
    def carregaMapaDinamico(self):
        #carrega o campo dinamico do mapa com valor 0,0 
        #sendo o primeiro indice eh: se a celula esta ativa, o segundo: o valor da fumaca
        for _ in range(self.tam_linhas):
            linha = []
            for _ in range(self.tam_colunas):
                linha.append(0)
            self.mapa_dinamico1.append(linha)
    
    def carregaMapaParedes(self):
        #carrega um mapa calculando a distancia para cada direcao, afim de encontrar a menor 
        #distancia para uma parede
        for i in range(self.tam_linhas):
            linha = []
            for j in range(self.tam_colunas):
                e = self.calculaDistanciaParede(i,j, 0, -1)
                d = self.calculaDistanciaParede(i,j, 0, +1)
                t = self.calculaDistanciaParede(i,j, -1, 0)
                b = self.calculaDistanciaParede(i,j, +1, 0)
                linha.append(numpy.min([e,d,t,b]))
            self.mapa_parede.append(linha)
    
    def carregaMapaFogo(self):
        #abre o arquivo e carrega o mapa fogo para uma matriz
        arquivo = open(self.diretorio_mapa_fogo, 'r')
        
        for linha in arquivo:
            self.mapa_fogo.append(list(linha.strip('\n')))
            
        arquivo.close()
        self.converteMapaFogo() #converte o arquivo para uma matriz de inteiros
    
    def carregaMapaVento(self):
        #abre o arquivo e carrega o mapa fogo para uma matriz
        arquivo = open(self.diretorio_mapa_vento, 'r')
        
        for linha in arquivo:
            self.mapa_vento.append(list(linha.strip('\n')))
            
        arquivo.close()
        self.converteMapaVento() #converte o arquivo para uma matriz de inteiros
    
    def converteMapa(self):
        #converte a matriz de string para uma matriz de inteiros
        newMapa = []
        
        for linha in self.mapa_objetos:
            newLinha = []
            
            for coluna in linha:
                newLinha.append(int(coluna))
            newMapa.append(newLinha)
            
        self.mapa_objetos = newMapa
        
    def converteMapaFogo(self):
        #converte a matriz de string para uma matriz de inteiros
        newMapa = []
        for i in range(self.tam_linhas):
            newLinha = []
            for j in range(self.tam_colunas):
                newLinha.append([1, Util.FIRE_TIMES, int(self.mapa_fogo[i][j])/10])
            newMapa.append(newLinha)
            
        self.mapa_fogo = newMapa
        
    def converteMapaVento(self):
        #converte a matriz de string para uma matriz de inteiros
        newMapa = []
        for i in range(self.tam_linhas):
            newLinha = []
            for j in range(self.tam_colunas):
                newLinha.append([1, int(self.mapa_vento[i][j])/10])
            newMapa.append(newLinha)
            
        self.mapa_vento = newMapa

    def calculaMapaEstaticoPortas(self):
        #calcula o campo estatico do mapa
        
        self.mapa_estatico = []
        mapa_objetos = self.mapa_objetos_static
        self.saidas = []

        for i in range(self.tam_linhas):
            linha = []
            for j in range(self.tam_colunas):
                if(mapa_objetos[i][j] == Util.M_PORTA):
                    #Caso de estar sendo calculado mapa estatico
                    self.addSaida(i, j)
                    linha.append(Util.M_VALOR_ESTATICO_SAIDA)       #saida tem valor no campo 1

                elif(mapa_objetos[i][j] == Util.M_JANELA):
                    linha.append(Util.M_VALOR_ESTATICO_SAIDA)

                elif(mapa_objetos[i][j] == Util.M_TELEPORTE):
                    #Caso de estar sendo calculado mapa estatico
                    linha.append(Util.M_VALOR_ESTATICO_TELEPORTE)   #saida tem valor no campo 2

                elif(mapa_objetos[i][j] == Util.M_PAREDE or mapa_objetos[i][j] == Util.M_VOID):
                    linha.append(1000)
                
                elif(mapa_objetos[i][j] == Util.M_VAZIO or mapa_objetos[i][j] == Util.M_DESENHO):
                    linha.append(Util.M_VAZIO)

            self.mapa_estatico.append(linha)

        lista = self.saidas

        #para cada ponto e calculado um campo estatico ou de calor para verificar qual o menor
        for ponto in lista:
            p = deepcopy(ponto)
            #Adicionando em cada ponto a profundidade atual para calculo recursivo
            p.append(1)
            self.calculaCampoEstaticoPelasSaidas(p, Util.ESTATICO_MAPA, Util.LIMITE_RECURSAO_PORTA)

        for i in range(self.teleportes.__len__()):
            self.teleportes[i].append(1)
            self.calculaCampoEstaticoPelosTeleportes(self.teleportes[i], Util.ESTATICO_MAPA, Util.LIMITE_RECURSAO_PORTA)
            
        #self.desenhaDistribuicaoMapaBanner();
    
    def calculaMapaEstaticoJanelas(self):
        #calcula o campo estatico do mapa
        mapa_objetos = self.mapa_objetos_static
        lista_menor = []

        for i in range(self.tam_linhas):

            for j in range(self.tam_colunas):
                if(mapa_objetos[i][j] == Util.M_JANELA):
                    #Caso de estar sendo calculado mapa estatico
                    self.addSaida(i, j)
                    lista_menor.append([i,j])

        #para cada ponto e calculado um campo estatico ou de calor para verificar qual o menor
        for ponto in lista_menor:
            p = deepcopy(ponto)
            #Adicionando em cada ponto a profundidade atual para calculo recursivo
            p.append(1)
            self.calculaCampoEstaticoPelasSaidas(p, Util.ESTATICO_MAPA, Util.LIMITE_RECURSAO_JANELA, Util.MULTIPLICADOR_INCREMENTO_JANELA)

        for i in range(self.teleportes.__len__()):
            self.teleportes[i].append(1)
            self.calculaCampoEstaticoPelosTeleportes(self.teleportes[i], Util.ESTATICO_MAPA, Util.LIMITE_RECURSAO_JANELA)

    def calculaMapaEstatico(self):
        self.calculaMapaEstaticoPortas()
        self.calculaMapaEstaticoJanelas()

    def calculaMapaCalor(self, lista):

        self.mapa_calor = []
        mapa_objetos = self.mapa_objetos
        
        for i in range(self.tam_linhas):
            linha = []
            for j in range(self.tam_colunas):
                if(mapa_objetos[i][j] == Util.M_PORTA or mapa_objetos[i][j] == Util.M_JANELA):
                    #Caso de estar sendo calculado mapa de calor
                    linha.append(Util.M_VAZIO)                              
                    
                elif(mapa_objetos[i][j] == Util.M_TELEPORTE):
                    #Caso de estar sendo calculado mapa de calor
                    linha.append(Util.M_VAZIO)                              
                    
                elif(mapa_objetos[i][j] == Util.M_PAREDE or mapa_objetos[i][j] == Util.M_VOID):
                    linha.append(1000)
                
                elif mapa_objetos[i][j] == Util.M_VAZIO or mapa_objetos[i][j] == Util.M_DESENHO:
                    linha.append(Util.M_VAZIO)

            self.mapa_calor.append(linha)
            
        #para cada ponto e calculado um campo estatico ou de calor para verificar qual o menor
        for ponto in lista:
            p = deepcopy(ponto)
            #Adicionando em cada ponto a profundidade atual para calculo recursivo
            p.append(1)
            self.calculaCampoEstaticoPelasSaidas(p, Util.CALOR_MAPA, Util.LIMITE_RECURSAO_CALOR)

        for i in range(self.teleportes.__len__()):
            self.teleportes[i].append(1)
            self.calculaCampoEstaticoPelosTeleportes(self.teleportes[i], Util.CALOR_MAPA, Util.LIMITE_RECURSAO_CALOR)
        #self.desenhaDistribuicaoMapaBanner();
                
    def calculaDistanciaParede(self, linha,coluna, direY, direX):
        cont = 0
        while(self.mapa_objetos[linha][coluna] != Util.M_PAREDE and self.mapa_objetos[linha][coluna] != Util.M_PORTA and
         int(self.mapa_objetos[linha][coluna]) != Util.M_JANELA and self.mapa_objetos[linha][coluna] != Util.M_VOID):
            linha  = linha + direY
            coluna = coluna + direX
            cont   = cont + 1
        return cont
    
    def addSaida(self, linha, coluna):
        #adiciona saida a um par ordenado para a lista de saidas
        saida = []
        saida.append(linha)
        saida.append(coluna)
        self.saidas.append(saida)
        
    def qtdSaidasVizinhas(self, linha, coluna):
        qtdSaidas = 0
        if(self.isSaida(linha-1, coluna-1)):
            qtdSaidas += 1
        if(self.isSaida(linha-1, coluna+1)):
            qtdSaidas += 1
        if(self.isSaida(linha+1, coluna+1)):
            qtdSaidas += 1
        if(self.isSaida(linha+1, coluna-1)):
            qtdSaidas += 1
        if(self.isSaida(linha-1, coluna)):
            qtdSaidas += 1
        if(self.isSaida(linha+1, coluna)):
            qtdSaidas += 1
        if(self.isSaida(linha, coluna-1)):
            qtdSaidas += 1
        if(self.isSaida(linha, coluna+1)):
            qtdSaidas += 1
        
        return qtdSaidas
    
    def isSaida(self, linha, coluna):
        if(self.mapa_objetos[linha][coluna] == Util.M_PORTA or self.mapa_objetos[linha][coluna] == Util.M_JANELA):
            return True
        else:
            return False
    
    def isSaidaVazia(self, linha, coluna):
        if(self.isSaida(linha, coluna) and self.isPosicaoVazia(linha, coluna)):
            return True
        else:
            return False

    def isTeleporte(self, linha, coluna):
        if(self.mapa_objetos[linha][coluna] == Util.M_TELEPORTE):
            return True
        else:
            return False
    
    def isPosicaoCaminhavel(self, linha, coluna):
        if(self.mapa_objetos[linha][coluna] == Util.M_VAZIO or self.mapa_objetos[linha][coluna] == Util.M_DESENHO):
            return True
        else:
            return False
    
    def isPosicaoVazia(self, linha, coluna):
        if(self.mapa_individuo[linha][coluna] == Util.M_VAZIO):
            return True
        else:
            return False
    
    def getTransicaoTeleporte(self, linha, coluna):
        for trans in self.teleportes:
            if(trans[Util.T_ORIGEM_LINHA] == linha and trans[Util.T_ORIGEM_COLUNA] == coluna):
                return trans
        return False
    
    def calculaCampoEstaticoPelasSaidas(self, saida, tipoDeMapa, limiteRecursão, multiplicadorIncremento = 1):
        #eh realizada uma interacao de niveis no mapa, sempre eh calculado o valor dos campos vizinhos 
        #e depois apartir dos vizinhos os vizinhos dos vizinhos ate que todos tenham sido vizitados
        listaVisitada = []
        listaPendencia = []
        listaPendencia2 = []
        listaPendencia.append(saida)
        listaPendencia2.append([saida[0], saida[1]])

        if tipoDeMapa == Util.ESTATICO_MAPA:
            mapaAtual = self.mapa_estatico
        elif tipoDeMapa == Util.CALOR_MAPA:
            mapaAtual = self.mapa_calor

        mapaAtual[saida[0]][saida[1]] = Util.M_VALOR_ESTATICO_SAIDA

        while(listaPendencia.__len__() != 0):
            campo = listaPendencia[0]
            listaVisitada.append([campo[0], campo[1]])
            listaPendencia.remove(campo)
            listaPendencia2.remove([campo[0],campo[1]])
            #superior esquerdo
            self.calculaPosicaoEstatica(campo[0], campo[1], -1, -1, 1.5 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #superior direito
            self.calculaPosicaoEstatica(campo[0], campo[1], -1,  1, 1.5 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #inferior direito
            self.calculaPosicaoEstatica(campo[0], campo[1],  1,  1, 1.5 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #inferior esquerdo
            self.calculaPosicaoEstatica(campo[0], campo[1],  1, -1, 1.5 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #topo
            self.calculaPosicaoEstatica(campo[0], campo[1], -1,  0,   1 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #baixo
            self.calculaPosicaoEstatica(campo[0], campo[1],  1,  0,   1 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #esquerdo
            self.calculaPosicaoEstatica(campo[0], campo[1],  0, -1,   1 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #direito
            self.calculaPosicaoEstatica(campo[0], campo[1],  0,  1,   1 * multiplicadorIncremento, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
    
    def calculaCampoEstaticoPelosTeleportes(self, teleporte, tipoDeMapa):
        #eh realizada uma interacao de niveis no mapa, sempre eh calculado o valor dos campos vizinhos 
        #e depois apartir dos vizinhos os vizinhos dos vizinhos ate que todos tenham sido vizitados
        listaVisitada = []
        listaPendencia2 = []
        listaPendencia = []
        listaPendencia2.append([saida[0], saida[1]])
        listaPendencia.append([teleporte[Util.T_ORIGEM_LINHA], teleporte[Util.T_ORIGEM_COLUNA]])

        if tipoDeMapa == Util.ESTATICO_MAPA:
            mapaAtual = self.mapa_estatico
        elif tipoDeMapa == Util.CALOR_MAPA:
            mapaAtual = self.mapa_calor

        mapaAtual[teleporte[Util.T_ORIGEM_LINHA]][teleporte[Util.T_ORIGEM_COLUNA]] = Util.M_VALOR_ESTATICO_TELEPORTE
        while(listaPendencia.__len__() != 0):
            campo = listaPendencia[0]
            listaVisitada.append([campo[0], campo[1]])
            listaPendencia.remove(campo)
            listaPendencia2.remove([campo[0],campo[1]])
            #superior esquerdo
            self.calculaPosicaoEstatica(campo[0], campo[1], -1, -1, 1.5, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #superior direito
            self.calculaPosicaoEstatica(campo[0], campo[1], -1, 1, 1.5, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #inferior direito
            self.calculaPosicaoEstatica(campo[0], campo[1], 1, 1, 1.5, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #inferior esquerdo
            self.calculaPosicaoEstatica(campo[0], campo[1], 1, -1, 1.5, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #topo
            self.calculaPosicaoEstatica(campo[0], campo[1], -1, 0, 1, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #baixo
            self.calculaPosicaoEstatica(campo[0], campo[1], 1, 0, 1, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #esquerdo
            self.calculaPosicaoEstatica(campo[0], campo[1], 0, -1, 1, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
            #direito
            self.calculaPosicaoEstatica(campo[0], campo[1], 0, 1, 1, listaVisitada, listaPendencia ,tipoDeMapa, campo[2], limiteRecursão, listaPendencia2)
    
    def calculaPosicaoEstatica(self, i, j, variacaoI, variacaoJ, incremento, listaVisitada, listaPendencia, tipoDeMapa, prof_atual, limiteRecursão, listaPendencia2):
        newI = i + variacaoI                               #calcula vizinho
        newJ = j + variacaoJ                               #calcula vizinho

        if tipoDeMapa == Util.ESTATICO_MAPA:
            mapaAtual = self.mapa_estatico
            mapa_objetos = self.mapa_objetos_static
        elif tipoDeMapa == Util.CALOR_MAPA:
            mapaAtual = self.mapa_calor
            mapa_objetos = self.mapa_objetos

        if(self.verificaPosicaoVizinhaExiste(newI, newJ)): #verifica se o vizinho nao esta fora das dimencoes da matriz
            if(mapa_objetos[newI][newJ] == Util.M_VAZIO or mapa_objetos[newI][newJ] == Util.M_DESENHO): #se a posicao eh do tipo vazio originalmente deve receber um valor
                if(mapaAtual[newI][newJ] == 0):    #se ainda nao foi atribuido algum valor ao campo
                    mapaAtual[newI][newJ] = mapaAtual[i][j] + incremento
                else:                                      #se ja foi atribuido, verifica se o novo eh menor
                    if(mapaAtual[newI][newJ] > mapaAtual[i][j] + incremento):
                        mapaAtual[newI][newJ] = mapaAtual[i][j] + incremento
                if( ([newI,newJ] not in listaVisitada and [newI,newJ] not in listaPendencia2) and prof_atual < limiteRecursão ):
                    listaPendencia2.append([newI,newJ])
                    prof_atual+=1
                    listaPendencia.append([newI,newJ,prof_atual])
    
    def verificaPosicaoVizinhaExiste(self, linha, coluna):
        #verifica se a posicao eh valida dentro dos limites da matriz
        if(linha < 0 or linha >= self.tam_linhas):
            return False
        if(coluna < 0 or coluna >= self.tam_colunas):
            return False
        return True
    
    def verificaMovimentoValido(self, linha, coluna):
        if(self.isPosicaoCaminhavel(linha, coluna)
           or self.isSaida(linha, coluna)
           or self.isTeleporte(linha, coluna)):
            if(self.isPosicaoVazia(linha, coluna)):
                return True
        return False
    
    def imprimeMapaEstatico(self):
        string = ""
        for i in range(self.tam_linhas):
            string = ""
            for j in range(self.tam_colunas):
                string= string + str(self.mapa_estatico[i][j])+"\t"
            print(string)
    
    def imprimeMapaIndividuo(self):
        string = ""
        for i in range(self.tam_linhas):
            string = ""
            for j in range(self.tam_colunas):
                string= string + str(self.mapa_individuo[i][j])+"\t"
            print(string)
    
    def imprimeMapaDinamico1(self):
        string = ""
        for i in range(self.tam_linhas):
            string = ""
            for j in range(self.tam_colunas):
                string= string + str(int(self.mapa_dinamico1[i][j]))+"\t"
            print(string)
    
    def imprimeMapaParedes(self):
        string = ""
        for i in range(self.tam_linhas):
            string = ""
            for j in range(self.tam_colunas):
                string= string + str(int(self.mapa_parede[i][j]))+"\t"
            print(string)
    
    def desenhaMapa(self, iteracao, diretorio, listaIndividuos):
        white = (255, 255, 255)
        black = (0, 0, 0)
        gray  = (192, 192, 192)
        #blue  = (0, 0, 255)
        red   = (255, 0, 0)
        green = (0,128,0)
        orange = (255,165,0)
        
        image1 = Image.new("RGB", (self.dados.TAM_BLOCO*self.tam_colunas, self.dados.TAM_BLOCO*self.tam_linhas), white)
        draw = ImageDraw.Draw(image1)

        for ind in listaIndividuos:
            #print(str(ind.linha)+","+str(ind.coluna))
            if(ind.idMapa == self.id):
                if(not self.isSaida(ind.linha, ind.coluna)):
                    draw.ellipse((ind.coluna*self.dados.TAM_BLOCO, ind.linha*self.dados.TAM_BLOCO, (ind.coluna+1)*self.dados.TAM_BLOCO, (ind.linha+1)*self.dados.TAM_BLOCO), ind.cor, black)
                #draw.rectangle((ind.coluna*self.dados.TAM_BLOCO, ind.linha*self.dados.TAM_BLOCO, (ind.coluna+1)*self.dados.TAM_BLOCO, (ind.linha+1)*self.dados.TAM_BLOCO), ind.cor, black)
        for i in range(self.tam_linhas):
            for j in range(self.tam_colunas):
                if(self.mapa_objetos[i][j] == Util.M_PAREDE):
                    #posicao inicial horizontal | posicao inicial vertical | posicao final horizontal | posicao final vertical
                    draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), black, black)
                elif(self.mapa_objetos[i][j] == Util.M_VOID):
                    draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), gray, black)
                elif(self.mapa_objetos[i][j] == Util.M_VAZIO):
                    if(self.isPosicaoVazia(i,j)):
                        draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), white, black)
                elif(self.mapa_objetos[i][j] == Util.M_DESENHO):
                    if(self.isPosicaoVazia(i,j)):
                        draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), orange, black)                
                elif(self.mapa_objetos[i][j] == Util.M_PORTA or self.mapa_objetos[i][j] == Util.M_JANELA):
                    draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), red, black)
                #if(self.mapa_individuo[i][j] == Util.M_INDIVIDUO):
                #    draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), blue, black)
                elif(self.mapa_objetos[i][j] == Util.M_TELEPORTE):
                    draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), green, black)
                        
        nomeImg = diretorio+"Mapa"+str(self.id)+"_Iter"+str(iteracao)+".png"
        
        image1.save(nomeImg)

    def desenhaMapaTracing(self, iteracao, diretorio):        
        image1 = Image.new("RGB", (self.dados.TAM_BLOCO*self.tam_colunas, self.dados.TAM_BLOCO*self.tam_linhas), (255,255,255))
        draw = ImageDraw.Draw(image1)

        for i in range(self.tam_linhas):
            for j in range(self.tam_colunas):
                if(self.mapa_objetos[i][j] == Util.M_PAREDE):
                    cor = (0,0,0)
                elif (self.mapa_objetos[i][j] == Util.M_PORTA or self.mapa_objetos[i][j] == Util.M_JANELA):
                    cor = (255,0,0)
                elif(self.mapa_objetos[i][j] == Util.M_VOID):
                    cor = (192,192,192)
                else:
                    cor = (255, 255-20*int(self.mapa_dinamico1[i][j]), 255)

                draw.rectangle((j*self.dados.TAM_BLOCO, i*self.dados.TAM_BLOCO, 
                               (j+1)*self.dados.TAM_BLOCO, (i+1)*self.dados.TAM_BLOCO), 
                                cor, (0,0,0))
        nomeImg = diretorio+"Tracing"+str(self.id)+"_Iter"+str(iteracao)+".png"
        
        image1.save(nomeImg)

    def desenhaMapaFogo(self, iteracao, diretorio):
        image1 = Image.new("RGB", (self.dados.TAM_BLOCO * self.tam_colunas, self.dados.TAM_BLOCO * self.tam_linhas),
                           (255, 255, 255))
        draw = ImageDraw.Draw(image1)
        for i in range(self.tam_linhas):
            for j in range(self.tam_colunas):
                if(self.mapa_objetos[i][j] == Util.M_PAREDE):
                    cor = (0,0,0)
                elif (self.mapa_objetos[i][j] == Util.M_PORTA or self.mapa_objetos[i][j] == Util.M_JANELA):
                    cor = (255,0,0)
                elif(self.mapa_objetos[i][j] == Util.M_VOID):
                    cor = (192, 192, 192)
                elif(self.mapa_fogo[i][j][Util.FS_STATE] == Util.FIRE_EMPTY):
                    cor = (255, 255, 255)
                elif(self.mapa_fogo[i][j][Util.FS_STATE] == Util.FIRE_BURNING):
                    cor = (255, 165, 0)
                else:
                    #Cor orquidia
                    cor = (147, 112, 219)

                draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO,
                                (j + 1) * self.dados.TAM_BLOCO, (i + 1) * self.dados.TAM_BLOCO),
                               cor, (0,0,0))
        nomeImg = diretorio + "Fire" + str(self.id) + "_Iter" + str(iteracao) + ".png"

        image1.save(nomeImg)

    def desenhaMapaCalor(self, iteracao, diretorio):
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        #blue = (0, 0, 255) 
        gray = (192, 192, 192)
        image1 = Image.new("RGB", (self.dados.TAM_BLOCO * self.tam_colunas, self.dados.TAM_BLOCO * self.tam_linhas),
                           white)
        draw = ImageDraw.Draw(image1)

        maior = 0
        for i in range(self.tam_linhas):
            for j in range(self.tam_colunas):
                if (self.mapa_objetos[i][j] != Util.M_PAREDE and self.mapa_objetos[i][j] != Util.M_JANELA and 
                self.mapa_objetos[i][j] != Util.M_VOID and self.mapa_calor[i][j] > maior):
                    maior = self.mapa_calor[i][j]
        maior = int(maior) + 1
        red_color = Color("red")
        blue_color = Color("blue")
        cores = list(red_color.range_to(blue_color, maior))

        for i in range(self.tam_linhas):
            for j in range(self.tam_colunas):
                if (self.mapa_objetos[i][j] == Util.M_PAREDE):
                    # posicao inicial horizontal | posicao inicial vertical | posicao final horizontal | posicao final vertical
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), black, black)
                elif (self.mapa_objetos[i][j] == Util.M_PORTA or self.mapa_objetos[i][j] == Util.M_JANELA):
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), red, black)
                elif (self.mapa_objetos[i][j] == Util.M_VOID):
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), gray, black)

                elif (self.mapa_objetos[i][j] == Util.M_VAZIO or self.mapa_objetos[i][j] == Util.M_DESENHO):
                    cor = str(cores[int(self.mapa_calor[i][j])].hex)
                    cor = re.sub('[#]', '', cor)
                    if (cor.__len__() == 3):
                        cor = cor[0] + cor[0] + cor[1] + cor[1] + cor[2] + cor[2]
                    cor = tuple(int(cor[i:i + 2], 16) for i in (0, 2, 4))
                    if cor == (255,0,0):
                        cor = (0,0,255)
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), cor, black)
        nomeImg = diretorio + "Heat" + str(self.id) + "_Iter" + str(iteracao) + ".png"

        image1.save(nomeImg)
        # print(maior)
        # exit(0);

    def desenhaDistribuicaoMapaBanner(self, diretorio,iteracao):
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        gray = (192, 192, 192)
        image1 = Image.new("RGB", (self.dados.TAM_BLOCO * self.tam_colunas, self.dados.TAM_BLOCO * self.tam_linhas),
                           white)
        draw = ImageDraw.Draw(image1)

        maior = 0
        for i in range(self.tam_linhas):
            for j in range(self.tam_colunas):
                if (self.mapa_objetos_static[i][j] != Util.M_PAREDE and 
                self.mapa_objetos[i][j] != Util.M_VOID and self.mapa_estatico[i][j] > maior):
                    maior = self.mapa_estatico[i][j]
        maior = int(maior) + 1
        red_color = Color("red")
        blue_color = Color("blue")
        cores = list(red_color.range_to(blue_color, maior))

        for i in range(self.tam_linhas):
            for j in range(self.tam_colunas):
                if (self.mapa_objetos_static[i][j] == Util.M_PAREDE):
                    # posicao inicial horizontal | posicao inicial vertical | posicao final horizontal | posicao final vertical
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), black, black)
                elif (self.mapa_objetos_static[i][j] == Util.M_PORTA or self.mapa_objetos_static[i][j] == Util.M_JANELA):
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), red, black)
                elif (self.mapa_objetos_static[i][j] == Util.M_VOID):
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), gray, black)
                elif (self.mapa_objetos_static[i][j] == Util.M_VAZIO or self.mapa_objetos_static[i][j] == Util.M_DESENHO):
                    cor = str(cores[int(self.mapa_estatico[i][j])].hex)
                    cor = re.sub('[#]', '', cor)
                    if (cor.__len__() == 3):
                        cor = cor[0] + cor[0] + cor[1] + cor[1] + cor[2] + cor[2]
                    cor = tuple(int(cor[i:i + 2], 16) for i in (0, 2, 4))
                    if cor == (255,0,0):
                        cor = (0,0,255)
                    draw.rectangle((j * self.dados.TAM_BLOCO, i * self.dados.TAM_BLOCO, (j + 1) * self.dados.TAM_BLOCO,
                                    (i + 1) * self.dados.TAM_BLOCO), cor, black)
        nomeImg = diretorio + "static-field" + "_Iter" + str(iteracao) + ".png"

        image1.save(nomeImg)
        # print(maior)
        # exit(0);

    def calculaValorMovimentoBruto(self, linha, coluna, direcao, ind):
        D = self.calculaValorDinamico(linha, coluna, ind)
        E = self.calculaValorEstatico(linha, coluna, ind)
        I = self.calculaValorEfeitoInercia(direcao, ind)
        P = self.calculaValorEfeitoParedes(linha, coluna, ind)
        C = 1
        c = 1
        if self.dados.FLAG_ATIVACAO_FOGO:
            C = self.calculaValorEfeitoCalor(linha, coluna, ind)
            if(self.verificaMovimentoValido(linha, coluna) and not self.mapa_fogo[linha][coluna] == Util.FIRE_BURNING):
            #if(self.verificaMovimentoValido(linha, coluna)):
                c = 1
            else:
                c = 0
        return D * E * I * P * c * C
    
    def calculaValorEfeitoCalor(self, linha, coluna, ind):
        if self.mapa_calor[linha][coluna] == 0:
            return 20**5
        else :
            #return max([0, math.log(Util.KC*self.mapa_calor[linha][coluna])])
            return ind.KC * ((self.mapa_calor[linha][coluna])**2 - 1)

    def calculaValorDinamico(self, linha, coluna, ind):
        #print(str(self.id) +' '+ str(linha) +' '+ str(coluna))
        return math.exp(ind.KD * self.mapa_dinamico1[linha][coluna])
    
    def calculaValorEstatico(self, linha, coluna, ind):
        return math.exp(ind.KS * -self.mapa_estatico[linha][coluna])
    
    def calculaValorEfeitoInercia(self, direcao, ind):
        if(direcao == ind.ultimaDirecao):
            return math.exp(ind.KI)
        return 1
        
    def calculaValorEfeitoParedes(self, linha, coluna, ind):
        return math.exp(ind.KW * numpy.min([Util.DMax, self.mapa_parede[linha][coluna]]))
