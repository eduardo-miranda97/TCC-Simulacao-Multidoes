
import matplotlib.pyplot as plt

import sys

indice = int(sys.argv[2])
nome = sys.argv[1]

Arq = open('arquivao.txt','r')

listas = []

for linha in Arq:

    if 'RUNTIME' in linha:
        listas.append([])
        continue
    if '#' in linha:
        continue

    cont = linha.split('\t')
    listas[-1].append(float(cont[indice]))

Arq.close()

plt.figure()

plt.xlabel("Kw")
plt.ylabel(nome)
plt.title("Comparações de "+nome+" com Kw distintos ")

#for i in range(5):
#    plt.boxplot(lst1[i], listas[i])

plt.boxplot(listas,labels=['0','0.1','0.2','0.3','0.4'])

plt.savefig("nishinariBoxplot"+nome+".png")
plt.close()
