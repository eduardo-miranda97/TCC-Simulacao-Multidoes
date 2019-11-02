# -*- coding:utf-8 -*-
'''
Created on 15 de set de 2017

@author: Guilherme C.
@author: Eduardo Miranda
'''

from Dados import Dados
from Simulacao import Simulacao
import sys
import cProfile as profile
import pstats

def main(arq=None):
    #p = profile.Profile()
    #p.enable()
    dados = Dados()
    dados.carregaDados('d_dadosIF.ini', arq)
    qtdIter = Simulacao(dados)

    #p.disable()
    #pstats.Stats(p).sort_stats('cumulative').print_stats(30)
    return qtdIter


def monteCarlo():

    kc = '5'
    qtdVezes = 100
    nomeClasse = 'classeMediadora '
    qtdInd = '406 '
    rgb = '144,238,144 '
    vital = '100 '
    deslocamento = '1 '
    ferido1 = '70 '
    ferido2 = '40 '

    lista = [1]
    for kd in lista:
        for ks in lista:
            for kw in lista:
                for ki in lista:
                    for it in range(qtdVezes):
                        #arqSaida = 'arqOut_'+str(kc)+'_'+str(kd)+'_'+str(ks)+'_'+str(kw)+'_'+str(ki)+'_'+str(it)+'.ind'

                        #fileOut = open(arqSaida,'w')
                        #linha = 'i '+qtdInd+rgb+vital+deslocamento+nomeClasse+ferido1+ferido2+kc+','
                        #linha += str(kd)+','+str(ks)+','+str(kw)+','+str(ki)
                        #fileOut.write(linha)
                        #fileOut.close()
                        main()

                        #arqSaida = 'result_'+str(kc)+'_'+str(kd)+'_'+str(ks)+'_'+str(kw)+'_'+str(ki)+'.txt'
                        #fileOut = open(arqSaida,'a')
                        #fileOut.write(str(resultados.tempo)+'\n')
                        #fileOut.close()



if len(sys.argv)<2:
    main()
else:
    monteCarlo()
