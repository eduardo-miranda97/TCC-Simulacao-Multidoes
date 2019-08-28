from PIL import Image
import numpy as np

im = Image.open('imagem2.png')
# R, G, B, A
im2arr = np.array(im)

colors = {
    'wall': [[0, 0, 0, 255], 1],
    'door': [[255, 0, 0, 255], 2],
    'none': [[255, 255, 255, 255], 0],
    'none': [[0, 0, 0, 0], 0]
}

for r in range(0, im2arr.shape[0]):
    for c in range(0, im2arr.shape[1]):
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


arr2im = Image.fromarray(im2arr)
#https://www.pixilart.com