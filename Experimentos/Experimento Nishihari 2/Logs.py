# -*- coding:utf-8 -*-
'''
Created on 13 de out de 2017

@author: Guilherme C.
@author: Eduardo Miranda
'''

from Util import Util
import statistics

class Logs(object):

    def __init__(self, diretorio, iteracao):
        '''Constructor'''
        self.diretorio = diretorio +'/'+str(iteracao)

        self.dirOut = diretorio

        # Cria cabecalho do arquivo de resultados das replicacoes
        # arquivo = open(self.dirOut + '/replicacoes.dat', 'a+')
        # arquivo.write('REPLICACAO\tRESULTADO\n')
        # arquivo.close()

        self.dirArq = diretorio+'/Log.txt'
        self.abreArquivoEscrita()
        
        self.NameMovsPerIter = self.diretorio + "/movs.per.iter.txt"
        self.ArqMovsPerIter  = None        

    def abreArquivoLeitura(self):
        self.arq = open(self.dirArq, 'r')
        
    def abreArquivoEscrita(self):
        self.arq = open(self.dirArq, 'w')
    
    def fechaArquivo(self):
        self.arq.close()
    
    def gravaNumReplicacao(self, ite):
        self.abreArquivoLeitura()
        conteudo = self.arq.readlines()
        conteudo.append("#REPLICACAO "+str(ite)+"\n")
        
        self.abreArquivoEscrita()
        self.arq.writelines(conteudo)
        self.arq.close()
    
    def gravaCabecalho(self, qtdIndividuos):
        self.abreArquivoLeitura()
        conteudo = self.arq.readlines()
        string = "Iter\t"
        for ind in range(qtdIndividuos):
            string+="M"+str(ind)+"\t"   #Id do Mapa
            string+="Y"+str(ind)+"\t"   #Posicao Linha
            string+="X"+str(ind)+"\t"   #Posicao Coluna
        conteudo.append(string+"\n")
        
        self.abreArquivoEscrita()
        self.arq.writelines(conteudo)
        self.arq.close()
    
    def gravaIteracao(self, ite, listaIndividuos):
        self.abreArquivoLeitura()
        conteudo = self.arq.readlines()
        
        string = str(ite)+"\t"
        for ind in range(listaIndividuos.__len__()):
            aux = self.pesquisaNaLista(ind, listaIndividuos)
            string+=str(listaIndividuos[aux].idMapa)+"\t"
            string+=str(listaIndividuos[aux].linha)+"\t"
            string+=str(listaIndividuos[aux].coluna)+"\t"
        conteudo.append(string+"\n")
        self.abreArquivoEscrita()
        self.arq.writelines(conteudo)
        self.arq.close()
        #self.arq.write(string+"\n")
        
    def pesquisaNaLista(self, idInd, listaIndividuos):
        for i in range(listaIndividuos.__len__()):
            if(listaIndividuos[i].idNum == idInd):
                return i;
        return 0

    def geraResultado(self, Replicacao, Resultado):
        arquivo = open(self.dirOut + '/replicacoes.dat', 'a+')
        arquivo.write(str(Replicacao) + '\t' + str(Resultado) + '\n')
        arquivo.close()

    def abreMovsPerIter(self):
        self.ArqMovsPerIter = open(self.NameMovsPerIter, "a+")

    def fechaMovsPerIter(self):
        self.ArqMovsPerIter.close()

    def gravaMovsPerIter(self, iteracao, movimentos, multidao):
        if multidao != 0:
            self.ArqMovsPerIter.write(str(iteracao) + '\t' + str(movimentos) + '\t' + str(multidao) + '\t' + str(movimentos/multidao) + '\n')
        else:
            self.ArqMovsPerIter.write(str(iteracao) + '\t' + str(movimentos) + '\t' + str(multidao) + '\t' + 'sem mudancas no mapa' + '\n')
    
    def printaKPIs(self, individuos, FLAG_ATIVACAO_FOGO):
        listMovsFeitos = []
        listMovsWaiting = []
        porcentagem_morte = 0
        porcentagem_feridos = 0
        for ind in individuos:
            listMovsFeitos.append(ind.movimentosFeitos)
            listMovsWaiting.append(ind.movimentosWaiting)
            if(ind.vitalidade <= 0):
                porcentagem_morte += 1
            elif(ind.vitalidade != Util.VITALIDADE_INICIAL_INDIVIDUO):
                porcentagem_feridos += 1

        mediana_moving = statistics.median(listMovsFeitos)
        mediana_waiting = statistics.median(listMovsWaiting)
        porcentagem_morte = 100 / len(individuos) * porcentagem_morte
        porcentagem_feridos = 100 / len(individuos) * porcentagem_feridos

        porcentagem_morte = round(porcentagem_morte,2)
        porcentagem_feridos = round(porcentagem_feridos,2)

        print("Media movimentos = " + str(mediana_moving))
        print("Media espera = " + str(mediana_waiting))
        if FLAG_ATIVACAO_FOGO:
            print("Porcentagem de individuos que morreram = " + str(porcentagem_morte) + "%")
            print("Porcentagem de individuos que se feriram = " + str(porcentagem_feridos) + "%")
        
        KPIs = []
        KPIs.append(mediana_moving)
        KPIs.append(mediana_waiting)
        if FLAG_ATIVACAO_FOGO:
            KPIs.append(porcentagem_morte)
            KPIs.append(porcentagem_feridos)
        
        return KPIs


    def geraHTML(self, data, tempoGasto, qtdIndividuos, qtdMapas, KPIs, FLAG_ATIVACAO_FOGO):
        #os.mkdir(diretorio)
        
        #arquivo = open('re_simulacao'+data.strftime('%a_%b_%d_%H_%M_%S_%Y')+'.html', 'w')
        arquivo = open(self.diretorio+'/index.html', 'w')
        arquivo.write('<!DOCTYPE HTML>\n')
        arquivo.write('<html lang="pt-br">\n')
        arquivo.write('    <head>\n')
        arquivo.write('        <meta charset="UTF-8">\n')
        arquivo.write('        <title>Relatorio Simulacao</title>\n')
        arquivo.write('        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">\n')
        arquivo.write('    </head>\n')
        arquivo.write('    <body>\n')
        arquivo.write('        <div class="container">\n')
#        arquivo.write('            <div class="jumbotron">\n')
#        arquivo.write('                <center>\n')
#        arquivo.write('                    <h2>Relatorio de Simulacao de Evacuacao</h2>\n')
#        arquivo.write('                    <h3>'+data.strftime('%a %b %d %T %Y')+'</h3>\n')
#        arquivo.write('                </center>\n')
#        arquivo.write('            </div>\n')
#        arquivo.write('            <hr/>\n')
        arquivo.write('            <div class="row">\n')
        arquivo.write('                <div class="col-md-2"></div>\n')
        arquivo.write('                    <div class="col-md-8">\n')
        arquivo.write('                        <table class="table table-striped table-hover table-condensed table-bordered table-sm">\n')
        arquivo.write('                            <thead>\n')
        arquivo.write('                                <tr>\n')
        arquivo.write('                                    <th>Indiv.</th>\n')
        arquivo.write('                                    <th>Iteracoes</th>\n')
        arquivo.write('                                    <th>#Andares</th>\n')

        arquivo.write('                                    <th>Med. movs</th>\n')
        arquivo.write('                                    <th>Med. espera</th>\n')
        if FLAG_ATIVACAO_FOGO:
            arquivo.write('                                    <th>% mortos</th>\n')
            arquivo.write('                                    <th>% feridos</th>\n')

        arquivo.write('                                </tr>\n')
        arquivo.write('                            </thead>\n')
        arquivo.write('                        <tbody>\n')
        arquivo.write('                            <tr>\n')
        arquivo.write('                                <td>'+str(qtdIndividuos)+'</td>\n')
        arquivo.write('                                <td>'+str(tempoGasto)+'</td>\n')
        arquivo.write('                                <td>'+str(qtdMapas)+'</td>\n')

        arquivo.write('                                <td>'+str(KPIs[0])+'</td>\n')
        arquivo.write('                                <td>'+str(KPIs[1])+'</td>\n')
        if FLAG_ATIVACAO_FOGO:
            arquivo.write('                                <td>'+str(KPIs[2])+'</td>\n')
            arquivo.write('                                <td>'+str(KPIs[3])+'</td>\n')
       
        arquivo.write('                            </tr>\n')
        arquivo.write('                        </tbody>\n')
        arquivo.write('                    </table>\n')
        arquivo.write('                </div>\n')
        arquivo.write('                <div class="col-md-2"></div>\n')
        arquivo.write('            </div>\n')

        #Parte para controle de javascript dos botoes
        arquivo.write('		    <div class="timers" align="center">\n')
        arquivo.write('				<button onclick="SetaMs(1)">1 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(3)">3 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(5)">5 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(10)">10 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(30)">30 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(50)">50 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(100)">100 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(300)">300 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(1000)">1000 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(3000)">3000 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(5000)">5000 ms</button>\n')
        arquivo.write('			</div>\n')
        
        arquivo.write('			<p></p>\n')
        arquivo.write('		    <div class="controls" align="center">\n')
        arquivo.write('				<button onclick="Retrocede()"> << </button>\n')
        arquivo.write('				<button onclick="Recomeca()"> PLAY </button>\n')
        arquivo.write('		    	<button onclick="Congela()"> STOP </button>\n')
        arquivo.write('		    	<button onclick="Avanca()"> >> </button>\n')
        arquivo.write('			</div>\n')




        arquivo.write('            <hr/>\n')
        arquivo.write('            <div class="row">\n')
        for i in range(qtdMapas):
            arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
            arquivo.write('                    <div id="banner_img" style="display:block">\n')
            for j in range(tempoGasto):
                arquivo.write('                        <img src="imagens/Mapa'+str(i)+'_Iter'+str(j)+'.png" class="img-fluid" style="display:none" id="mapa'+str(i)+"_"+str(j)+'">\n')
            arquivo.write('                    </div>\n')
            arquivo.write('                </div>\n')

        if FLAG_ATIVACAO_FOGO:
            for i in range(qtdMapas):
                arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
                arquivo.write('                    <div id="banner_img" style="display:block">\n')
                for j in range(tempoGasto):
                    arquivo.write('                        <img src="imagens/Heat'+str(i)+'_Iter'+str(j)+'.png" class="img-fluid" style="display:none" id="heat'+str(i)+"_"+str(j)+'">\n')
                arquivo.write('                    </div>\n')
                arquivo.write('                </div>\n')

        for i in range(qtdMapas):
            arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
            arquivo.write('                    <div id="banner_img" style="display:block">\n')
            for j in range(tempoGasto):
                arquivo.write('                        <img src="imagens/Tracing'+str(i)+'_Iter'+str(j)+'.png" class="img-fluid" style="display:none" id="tracing'+str(i)+"_"+str(j)+'">\n')
            arquivo.write('                    </div>\n')
            arquivo.write('                </div>\n')

        if FLAG_ATIVACAO_FOGO:
            for i in range(qtdMapas):
                arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
                arquivo.write('                    <div id="banner_img" style="display:block">\n')
                for j in range(tempoGasto):
                    arquivo.write('                        <img src="imagens/Fire'+str(i)+'_Iter'+str(j)+'.png" class="img-fluid" style="display:none" id="fire'+str(i)+"_"+str(j)+'">\n')
                arquivo.write('                    </div>\n')
                arquivo.write('                </div>\n')

        for i in range(qtdMapas):
            arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
            arquivo.write('                    <div id="banner_img" style="display:block">\n')
            #static-field_Iter0
            for j in range(tempoGasto):
                if Util.QTD_ITER_CALC_CAMPO_STATICO == 0:
                    iteracao = 0
                else:
                    iteracao = Util.QTD_ITER_CALC_CAMPO_STATICO * (j // Util.QTD_ITER_CALC_CAMPO_STATICO)
                arquivo.write('                        <img src="imagens/static-field_Iter'+str(iteracao)+'.png" class="img-fluid" style="display:none" id="static-field'+str(i)+"_"+str(j)+'">\n')
            arquivo.write('                    </div>\n')
            arquivo.write('                </div>\n')
        arquivo.write('            </div>\n')
        arquivo.write('            <hr/>\n')
        arquivo.write('            <div class="jumbotron" style="margin-bottom:0px">\n')
        arquivo.write('            </div>\n')
        arquivo.write('        </div>\n')
        arquivo.write('        <script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>\n')
        arquivo.write('        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
        arquivo.write('        <script>\n')

        arquivo.write('''
            function SetaMs(Timer)
            {
                clearInterval(TimeHandler)
                TimeHandler = setInterval("mudaImg()", Timer);
            }

            function Congela()
            {
                ultimoinc  = incremento
                incremento = 0
            }

            function Recomeca()
            {
                incremento = ultimoinc
            }

            function Avanca()
            {
                ultimoinc  = +1
                incremento = +1
            }

            function Retrocede()
            {
                ultimoinc  = -1
                incremento = -1
            }

            function mudaImg() {
                $('#mapa0_'+indice).css("display", "none");\n''')

        if FLAG_ATIVACAO_FOGO:
            arquivo.write("""                $('#heat0_'+indice).css("display", "none");\n""")

        arquivo.write('''                $('#tracing0_'+indice).css("display", "none");\n''')
        if FLAG_ATIVACAO_FOGO:
            arquivo.write('''                $('#fire0_'+indice).css("display", "none");\n''')
                
        arquivo.write('''                $('#static-field0_'+indice).css("display", "none");\n''')

        arquivo.write('''
                if (incremento > 0)
                {
                    if(indice == '''+str(tempoGasto)+''') 
                    {
                        indice = -1;
                    }
                }
                else
                {
                    if(indice == 0)
                    {
                        indice = '''+str(tempoGasto)+'''
                    }					
                }

                if(incremento != 0)
                {
                       indice = indice + incremento;
                }\n''')

        arquivo.write('''                $('#mapa0_'+indice).removeAttr("style");\n''')
        if FLAG_ATIVACAO_FOGO:
            arquivo.write('''                $('#heat0_'+indice).removeAttr("style");\n''')
        arquivo.write('''                $('#tracing0_'+indice).removeAttr("style");\n''')
        if FLAG_ATIVACAO_FOGO:
            arquivo.write('''                $('#fire0_'+indice).removeAttr("style");''')

        arquivo.write('''
                $('#static-field0_'+indice).removeAttr("style");
            }\n''')

        arquivo.write('''
            $(document).ready(function() {
                indice = 0;
                incremento = 1
                ultimoinc = 1
                TimeHandler = setInterval("mudaImg()", 100);
            })\n''')

        arquivo.write('        </script>\n')
        arquivo.write('    </body>\n')
        arquivo.write('</html>\n')
        arquivo.close()
