# -*- coding:utf-8 -*-
'''
Created on 15 de jul de 2017

@author: Guilherme C.
@author: Eduardo Miranda
'''
from Individuo import Individuo

class Dados(object):
    '''Variaveis do arquivo de entrada'''
    TAM_BLOCO             = 0
    QTD_PESSOAS           = 0
    TIME_ESPERA           = 0
    GERAR_LOG             = 0
    QTD_CAMADAS           = 0
    DIRETORIO_MAPAS       = []
    DIRETORIO_MAPAS_FOGO  = []
    DIRETORIO_MAPAS_VENTO = []
    QTD_TELETRANSPORTES   = 0
    TELETRANSPORTES       = []
    LISTA_INDIVIDUOS      = []
    COR_MORTE             = 0
    LISTA_FOCOS           = []
    CLASSES               = []
    CORES                 = {}

    def __init__(self):
        '''Constructor'''
    
    def carregaDados(self, dirArquivoConfig, arqIndividuos):

        arquivo = open(dirArquivoConfig, 'r')
        state = 1
        '''Variaveis do arquivo de entrada'''
        self.TAM_BLOCO             = 0
        self.QTD_PESSOAS           = 0
        self.TIME_ESPERA           = 0
        self.GERAR_LOG             = 0
        self.QTD_CAMADAS           = 0
        self.DIRETORIO_MAPAS       = []
        self.DIRETORIO_MAPAS_FOGO  = []
        self.DIRETORIO_MAPAS_VENTO = []
        self.QTD_TELETRANSPORTES   = 0
        self.TELETRANSPORTES       = []
        self.QTD_REPLICACACOES     = 0
        self.QTD_FOCOS_INCENDIO    = 0
        self.LISTA_INDIVIDUOS      = []
        self.FLAG_FOGO_INICIAL     = 0
        self.COR_MORTE             = 0
        self.LISTA_FOCOS           = []
        self.FLAG_ATIVACAO_FOGO    = 0
        self.CLASSES               = []
        self.CORES                 = {}
        for linha in arquivo:
            if(len(linha) > 1):
                if(linha[0] !="#"): #Comentario inicia com #
                    if(state==1):       #Tamanho Bloco
                        self.TAM_BLOCO = int(linha)
                        state=3
                    #elif(state==2):       #Quantidade Pessoas
                    #    self.QTD_PESSOAS = int(linha)
                    #s    state=3
                    elif(state==3):       #Tempo do Gif
                        self.TIME_ESPERA = int(linha)
                        state=4
                    elif(state==4):       #Gerar Logs
                        self.GERAR_LOG = int(linha)
                        state=5
                    elif(state==5):       #Qtd de Camadas
                        self.QTD_CAMADAS = int(linha)
                        state=6
                    elif(state==6):       #Diretorio dos mapas
                        self.DIRETORIO_MAPAS.append(linha.strip('\n'))
                        if(self.DIRETORIO_MAPAS.__len__() == self.QTD_CAMADAS):
                            state = 7
                    elif(state==7):       #Qtd de teletransportes
                        self.QTD_TELETRANSPORTES = int(linha)
                        if(int(linha) == 0):
                            state=9
                        else:
                            state=8
                    elif(state==8):       #Dados dos teletransportes
                        self.TELETRANSPORTES.append(linha.strip('\n'))
                        if(self.TELETRANSPORTES.__len__() == self.QTD_TELETRANSPORTES):
                            state=9
                    elif(state==9):       #Qtd de replicacoes da simulacao
                        self.QTD_REPLICACACOES = int(linha)
                        state=10
                    elif(state==10):      #Qtd de fotos iniciais de incendio na simulacao
                        self.QTD_FOCOS_INCENDIO = int(linha)
                        state=11
                    elif(state==11):
                        if arqIndividuos == None:
                            self.carregaInfoIndividuos(linha.strip('\n'))
                        else:
                            self.carregaInfoIndividuos(arqIndividuos)
                        self.QTD_PESSOAS = len(self.LISTA_INDIVIDUOS)
                        state=12
                    elif(state==12):
                        self.DIRETORIO_MAPAS_FOGO.append(linha.strip('\n'))
                        if(self.DIRETORIO_MAPAS_FOGO.__len__() == self.QTD_CAMADAS):
                            state = 13
                    elif(state==13):
                        self.DIRETORIO_MAPAS_VENTO.append(linha.strip('\n'))
                        if(self.DIRETORIO_MAPAS_VENTO.__len__() == self.QTD_CAMADAS):
                            state = 14
                    elif(state==14):
                        self.FLAG_FOGO_INICIAL = int(linha)
                        if self.FLAG_FOGO_INICIAL == 0:
                            state = 16
                        state = 15
                    elif(state==15):
                        linha = linha.strip('\n')
                        vet = linha.split(';')
                        for el in vet:
                            foco = el.split(',')
                            self.LISTA_FOCOS.append([int(foco[0]), int(foco[1]), int(foco[2])])
                        state = 16
                    elif(state==16):
                        self.FLAG_ATIVACAO_FOGO = int(linha)
                        if self.FLAG_ATIVACAO_FOGO == 1:
                            self.FLAG_ATIVACAO_FOGO = True
                        else:
                            self.FLAG_ATIVACAO_FOGO = False
                        state = 17

        arquivo.close()
    

    def carregaInfoIndividuos(self, diretorio):
        arquivo = open(diretorio, 'r')
        contador = 0 
        for linha in arquivo:
            if len(linha) <= 1 or linha[0] == "#":
                continue
            elif linha[0] == 'i':
                lst = linha.split()
                for _ in range(int(lst[1])):
                    contador += 1
                    lstCor = lst[2].split(",")
                    corIndividuo = (int(lstCor[0]), int(lstCor[1]), int(lstCor[2]))
                    vitalidade = int(lst[3])
                    deslocamento = int(lst[4])
                    classe = lst[5]
                    vit1 = int(lst[6])
                    vit2 = int(lst[7])
                    lstCONST = lst[8].split(',')
                    kc = float(lstCONST[0])
                    kd = float(lstCONST[1])
                    ks = float(lstCONST[2])
                    kw = float(lstCONST[3])
                    ki = float(lstCONST[4])     
                    
                    #(idNum, cor, vitalidade, deslocamento, classeIndividuo, vit1, vit2):
                    self.LISTA_INDIVIDUOS.append(Individuo(contador, corIndividuo, vitalidade, deslocamento, classe, vit1, vit2, kc, kd, ks, kw, ki))
                    if not classe in self.CLASSES:
                        self.CLASSES.append(classe)
                        self.CORES[classe] = corIndividuo

            elif linha[0] == 'd':
                lista = list(map(int,linha.split()[1].split(',')))
                self.COR_MORTE = (lista[0], lista[1], lista[2])
            elif linha[0] == 'f':
                break