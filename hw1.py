import numpy as np

def read_file(file):
    with open(file) as f:
        return [line.rstrip() for line in f]

def nominal_resolution(file):
    lst = read_file(file)
    figure = np.loadtxt(lst[1:])
    horizontal_mm = int(lst[0])
    if max(sum(figure)) != 0:
        return horizontal_mm / max(np.sum(figure, axis = 1))
    else:
        return 0

def offset(files):
    img1 = np.loadtxt(read_file(files[0])[1:])
    img2 = np.loadtxt(read_file(files[1])[1:])
    difference = np.argwhere(img2 == 1)[0] - np.argwhere(img1 == 1)[0]
    return difference

figures = ['figure1.txt', 'figure2.txt', 'figure4.txt', 'figure5.txt', 'figure6.txt']
images = ['img1.txt', 'img2.txt']

for figure in figures:
    print(f'{figure}: {nominal_resolution(figure)}')

print(f'Смещение по x: {offset(images)[0]}, смещение по y: {offset(images)[1]}')

   
