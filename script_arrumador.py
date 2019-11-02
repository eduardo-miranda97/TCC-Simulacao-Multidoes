import sys

if len(sys.argv) != 3:
    print("\nERRO Sintaxe: python3 script_arrumador.py <arq-entrada> <arq-saida> \n")
    exit()

arquivo_entrada = sys.argv[1]
arquivo_saida = sys.argv[2]	

arquivo = open(arquivo_entrada, 'r')
arquivo2 = open(arquivo_saida, 'w')

for linha in arquivo:
    escrita = ''
    cont = linha.split('\t')
    cont[7] = cont[7].replace('\n','')
    escrita = 'i ' + cont[1] + ' ' + cont[9].strip() + ' 80 ' + cont[7]+ ' ' + cont[1] + ' 70 40 5,'+cont[3]+ ','+cont[4]+','+cont[5]+','+cont[6]
    arquivo2.write(escrita+'\n')


arquivo2.close()
arquivo.close()
