import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

first_ball_x, first_ball_y = [], []
second_ball_x, second_ball_y = [], []

for i in range(99):
    labeled = label(np.load(f'h_{i}.npy'))
    props = regionprops(labeled)
    sorted_areas = sorted(props, key=lambda x: x.area)

    first_ball_x.append(sorted_areas[0].centroid[0])
    first_ball_y.append(sorted_areas[0].centroid[1])
    
    second_ball_x.append(sorted_areas[1].centroid[0])
    second_ball_y.append(sorted_areas[1].centroid[1])


plt.plot(first_ball_x, first_ball_y)
plt.plot(second_ball_x, second_ball_y)
plt.legend(['First ball', 'Second ball'], loc=2)
plt.show()



