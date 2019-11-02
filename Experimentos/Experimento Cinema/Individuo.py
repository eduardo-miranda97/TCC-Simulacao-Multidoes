# -*- coding:utf-8 -*-
'''
Created on 14 de set de 2017

@author: Guilherme C.
@author: Eduardo Miranda
'''
from Util import Util;

class Individuo(object):

    #def __init__(self, idNum, cor, vitalidade, deslocamento, classeIndividuo, vit1, vit2):
    def __init__(self, idNum, cor, vitalidade, deslocamento, classeIndividuo, vit1, vit2, KC, KD, KS, KW, KI):
        '''Constructor'''
        #Informacoes basicas do individuo
        self.idNum             = idNum
        self.cor               = cor
        self.ultimaDirecao     = 0
        self.classeIndividuo   = classeIndividuo
        self.vitalidade        = vitalidade
        self.deslocamentoBase  = deslocamento
        self.deslocamento      = deslocamento
        self.qtdPassos         = 0
        self.vit1              = vit1
        self.vit2              = vit2
        self.KC                = KC
        self.KD                = KD
        self.KS                = KS
        self.KW                = KW
        self.KI                = KI
        self.iteracoesGastas   = 0
        
        #Estatisticas
        self.movimentosFeitos  = 0
        self.movimentosWaiting = 0
        
        #Posicionamento do individuo no mapa
        self.coluna            = 0
        self.linha             = 0
        self.idMapa            = 0
        self.saiu              = False
        '''
        self.idade            = idade
        self.escolaridade     = escolaridade
        self.contadorNoRound  = 0
        self.status           = Util.I_NAO_MOVIDO
        '''

    def posicionaIndividuoMapa(self, coluna, linha, idMapa):
        self.coluna            = coluna
        self.linha             = linha
        self.idMapa            = idMapa

    def diminuiVitalidade(self, distancia):

        if (distancia == 0):
            return self.vitalidade
        
        return self.vitalidade - (16-distancia)

    def corrigeDeslocamento(self):
        if self.vitalidade < self.vit1:
            return self.deslocamentoBase + 1
        elif self.vitalidade < self.vit2:
            return self.deslocamentoBase + 2
        return self.deslocamentoBase       
        