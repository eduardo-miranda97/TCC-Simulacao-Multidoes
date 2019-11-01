from PIL import Image
import numpy as np
import sys

def retornaPrctCombust(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if len(sys.argv) == 2:
    if sys.argv[1] =='-h' or sys.argv[1] =='-H' or len(sys.argv) == 1:
        string = "Tabela de cores para representação do mapa:\n"
        string += "Portas - Vermelho : RGB = (255,0,0)\n"
        string += "Espaço vazio - Branco : RGB = (255,255,255)\n"
        string += "Espaço inatingível - Prata : RGB = (192,192,192)\n"
        string += "Janelas - Lima : RGB = (0,255,0)\n"
        string += "Paredes - Preto : RGB = (0,0,0)\n"
        string += "Desenho - Laranja : RGB = (255,165,0)\n"

        string +=  """As porcentagem de combustão dos objetos serão definidas em uma escala de azul onde o R = G = 0 enquanto o
B varia de 1-255 definindo então a combustão do objeto em questão sendo 1 menos inflamável e 255 mais inflamável\n."""

        print(string)

    exit()

if len(sys.argv) != 3:
    print("\nERRO Sintaxe: python3 conversorMapa.py <arq-entrada> <arq-saida> \n")
    exit()

arquivo_entrada = sys.argv[1]
arquivo_saida = sys.argv[2]	

print(arquivo_entrada + ' ' + arquivo_saida)

im = Image.open(arquivo_entrada)
# R, G, B, A
im2arr = np.array(im)

print()

colors = {
    'wall': [[0, 0, 0, 255], 1],
    'door': [[255, 0, 0, 255], 2],
    'none': [[255, 255, 255, 255], 0],
    'none': [[0, 0, 0, 0], 0]
}
#funcao para reconhecer a quantidade de cores

listOfColors = list()
for r in range(0, im2arr.shape[0]):
    for c in range(0, im2arr.shape[1]):

        bu = True
        for cor in listOfColors:
            if im2arr[r][c][0] == cor[0] and im2arr[r][c][1] == cor[1] and im2arr[r][c][2] == cor[2]:
                bu = False
            else:
                pass

        if bu:
            listOfColors.append(im2arr[r][c])

        '''
        diff = {}
        print("======================================")
        for color in colors.keys():
            colorArray = colors[color][0]
            diff[color] = abs(im2arr[r][c][0] - colorArray[0]) + abs(im2arr[r][c][1] - colorArray[1]) + abs(im2arr[r][c][2] - colorArray[2]) + abs(im2arr[r][c][3] - colorArray[3])
            print("=============")
            print(im2arr[r][c])
            print(colorArray)
            print(diff[color])
            print("============")
        a = 1000
        object = "N"
        for dif in diff.keys():
            if diff[dif] < a:
                object = dif
                a = diff[dif]

        print(f"{r} - {c} = {object}")
        '''

#funcao para traduzir o primeiro mapa estatico de distancias
with open(arquivo_saida+".map", "w") as arq_out:

    for r in range(0, im2arr.shape[0]):
        for c in range(0, im2arr.shape[1]):

            if im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                arq_out.write('1')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                arq_out.write('2')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 255:
                arq_out.write('0')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 165 and im2arr[r][c][2] == 0:
                arq_out.write('9')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 166 and im2arr[r][c][2] == 0:
                arq_out.write('9')
            elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 0:
                arq_out.write('7')
            elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0:
                arq_out.write('0')
            else:
                arq_out.write('8')
        arq_out.write('\n')

#funcao para traduzir o segundo mapa de fogo fixo
with open(arquivo_saida+"_fogo.map", "w") as arq_out:

    for r in range(0, im2arr.shape[0]):
        for c in range(0, im2arr.shape[1]):

            if im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                arq_out.write('0')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                arq_out.write('0')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 255:
                arq_out.write('1')
            elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 0:
                arq_out.write('1')
            elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0:
                arq_out.write(retornaPrctCombust(im2arr[r][c][2], 1, 255, 0, 8))
            else:
                arq_out.write('1')
        arq_out.write('\n')

#funcao para traduzir o segundo mapa de vento fixo
with open(arquivo_saida+"_vento.map", "w") as arq_out:

    for r in range(0, im2arr.shape[0]):
        for c in range(0, im2arr.shape[1]):
            
            if im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                arq_out.write('0')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                arq_out.write('1')
            elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 255:
                arq_out.write('1')
            else:
                arq_out.write('1')
        arq_out.write('\n')

print(listOfColors)
arr2im = Image.fromarray(im2arr)
#https://www.pixilart.com