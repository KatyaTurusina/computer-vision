from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu
from skimage.morphology import label
from skimage.measure import regionprops
from skimage.color import rgb2gray

total_max_length_objects = 0
max_length_objects = []

for i in range(1, 12):
    img = plt.imread(f'images/img ({i}).jpg')
    thresh = threshold_otsu(rgb2gray(img))
    binary = img <= thresh * 1.08
    labeled = label(binary)
    props = regionprops(labeled)
    for prop in props:
        max_length_objects.append(prop.major_axis_length)

total_max_length_objects += sum(1 for i in max_length_objects if max(max_length_objects) - i < 300)
print(f'Общая сумма карандашей на всех фотографиях: {total_max_length_objects}')
