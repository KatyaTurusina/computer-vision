import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv

image = plt.imread("images/balls_and_rects.png")
hsv = rgb2hsv(image)
labeled = label(image.mean(2) > 0)
h = hsv[:, :, 0]
rectangles_count = {}
circles_count = {}

for region in regionprops(labeled):
    if region.area == region.area_bbox:
        color = round(np.mean(h[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]]), 3)
        if color in rectangles_count:
            rectangles_count[color] += 1
        else:
            rectangles_count[color] = 1
    else:
        color = round(np.mean(h[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]]), 3)
        if color in circles_count:
            circles_count[color] += 1
        else:
            circles_count[color] = 1


def group_shades(data):
    grouped_data = {}
    for color, count in data.items():
        rounded_color = round(color, 1)
        if rounded_color in grouped_data:
            grouped_data[rounded_color] += count
        else:
            grouped_data[rounded_color] = count
    return grouped_data


print(f"Всего фигур: {sum(group_shades(rectangles_count).values()) + sum(group_shades(circles_count).values())}")
print(f"Всего прямоугольников: {sum(group_shades(rectangles_count).values())}")
print(f"Всего кругов: {sum(group_shades(circles_count).values())}")

print("Количество прямоугольников каждого оттенка:")
for color, count in sorted(group_shades(rectangles_count).items()):
    print(f"Оттенок: {color:.2f}, Количество прямоугольников: {count}")

print("Количество кругов каждого оттенка:")
for color, count in sorted(group_shades(circles_count).items()):
    print(f"Оттенок: {color:.2f}, Количество кругов: {count}")
