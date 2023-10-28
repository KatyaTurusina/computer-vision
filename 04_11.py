import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_erosion, binary_dilation,
                                binary_opening, binary_closing)

img = np.load("ps.npy")

masks = {
    'bottom_hole': np.array(
                     [[1,1,1,1,1,1],
                      [1,1,1,1,1,1],
                      [1,1,0,0,1,1],
                      [1,1,0,0,1,1]]),
    'left_hole': np.rot90(
                     [[1,1,1,1,1,1],
                      [1,1,1,1,1,1],
                      [1,1,0,0,1,1],
                      [1,1,0,0,1,1]], 1, axes=(0, 1)),
    'top_hole': np.rot90(
                     [[1,1,1,1,1,1],
                      [1,1,1,1,1,1],
                      [1,1,0,0,1,1],
                      [1,1,0,0,1,1]], 2, axes=(0, 1)),
    'right_hole': np.rot90(
                     [[1,1,1,1,1,1],
                      [1,1,1,1,1,1],
                      [1,1,0,0,1,1],
                      [1,1,0,0,1,1]], 3, axes=(0, 1)),
    'rectangle': np.ones((4, 6), dtype = int)}

num_of_objects = {}

for mask in masks:
    num_of_objects[mask] = np.max(label(binary_opening(img, masks[mask])))

num_of_objects['bottom_hole'] -= num_of_objects['rectangle']
num_of_objects['top_hole'] -= num_of_objects['rectangle']

for key,value in num_of_objects.items():
    print(key, ':', value)
print(f"In total: {sum(num_of_objects.values())}")

