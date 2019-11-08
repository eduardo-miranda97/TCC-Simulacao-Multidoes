# -*- coding:utf-8 -*-
'''
Created on 16 de set de 2017

@author: Guilherme C.
@author: Eduardo Miranda
'''

class Util(object):
    '''Constantes'''
    #Constantes do mapa
    M_VAZIO     = 0
    M_PAREDE    = 1
    M_PORTA     = 2
    M_INVISIVEL = 3
    M_TELEPORTE = 4
    M_INDIVIDUO = 5
    M_OBJETO    = 6
    M_JANELA    = 7
    M_VOID      = 8
    M_DESENHO   = 9
    
    M_VALOR_ESTATICO_SAIDA     = 1
    M_VALOR_ESTATICO_TELEPORTE = 3
    
    #Contantes de tipos de mapa
    CALOR_MAPA = 1
    ESTATICO_MAPA = 2

    #Constantes dos valores dos individuos
    I_NAO_MOVIDO = 0
    I_MOVIDO     = 1
    I_PARADO     = 2
    I_ESPERANDO  = 3
    
    I_ESCOLARIDADE_FUNDAMENTAL = 0
    I_ESCOLARIDADE_MEDIO       = 1
    I_ESCOLARIDADE_SUPERIOR    = 2
    
    #Constantes de cores
    COR_INDIVIDUO = "blue"
    COR_PAREDE    = "black"
    COR_CHAO      = "white"
    COR_PORTA     = "red"
    
    #Constantes dos indices na lista de mapas 
    #IDmapa-linha-coluna_IDmapa-linha-coluna
    T_ORIGEM_MAPA    = 0
    T_ORIGEM_LINHA   = 1
    T_ORIGEM_COLUNA  = 2
    T_DESTINO_MAPA   = 3
    T_DESTINO_LINHA  = 4
    T_DESTINO_COLUNA = 5
    
    #Constantes para campo de vis�o para movimentacao
    C_SE = 0
    C_SD = 1
    C_ID = 2
    C_IE = 3
    C_TO = 4
    C_BA = 5
    C_ES = 6
    C_DI = 7
    C_ME = 8
    
    #Difus�o e Decaimento
    DD_ALFA  = 0.6
    DD_SIGMA = 0.1
    
    #Constantes de Movimento
    KC = 5
    KD = 1
    KS = 2
    KW = 0.5
    KI = 1
    DMax = 10

    #Sexo
    S_FEMININO  = 0
    S_MASCULINO = 1
    
    #Idade
    IND_ADOLECENTE = 0
    IND_JOVEM      = 1
    IND_ADULTO     = 2
    IND_IDOSO      = 3

    #Vitalidade do individuo
    VITALIDADE_INICIAL_INDIVIDUO = 100
    
    #fogo e fumaca
    FS_STATE  = 0
    F_PERSIST = 1
    F_STATIC  = 2
    S_STATIC  = 1
    
    FIRE_EMPTY    = 0
    FIRE_UNBURNED = 1
    FIRE_BURNING  = 2
    
    SMOKE_BLANK         = 0
    SMOKE_WITHOUT_SMOKE = 1
    SMOKE_WITH_SMOKE    = 2

    #Controle do expalhamento do fogo
    FIRE_TIMES = 15
    FIRE_RATE = 0.5

    #Controle para ver de quanto em quanto tempo sera recalculado o campo estatico
    QTD_ITER_CALC_CAMPO_STATICO = 20

    #Controle para limite das chamadas recursivas que calculam o mapa de calor e mapa estatico
    LIMITE_RECURSAO_CALOR = 10
    LIMITE_RECURSAO_PORTA = 10000
    LIMITE_RECURSAO_JANELA = 7

    #Controle para fator mutiplicativo que definira a proximidade do campo estatico a partir de uma janela
    MULTIPLICADOR_INCREMENTO_JANELA = 8
    
    def __init__(self, params):
        '''Constructor'''
        pass
