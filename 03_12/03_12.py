import matplotlib.pyplot as plt
import numpy as np
from skimage.morphology import label, binary_dilation
from skimage.measure import regionprops


def has_vline(arr):
    return 1. in arr.mean(0)


def recognize(prop):
    euler_number = prop.euler_number
    if euler_number == -1:
        if has_vline(prop.image):
            return "B"
        else:
            return "8"
    elif euler_number == 0:
        tmp = prop.image.copy()
        tmp[-1, :] = 1
        tmp_props = regionprops(label(binary_dilation(tmp)))
        tmp_euler = tmp_props[0].euler_number
        if tmp_euler == -1:
            return "A"
        else:
            if has_vline(prop.image):
                tmp = prop.image.copy()
                tmp_cent = tmp.shape[0] // 2
                tmp[tmp_cent, :] = 1
                tmp_props = regionprops(label(binary_dilation(tmp)))
                tmp_euler = tmp_props[0].euler_number
                if tmp_euler == -1:
                    return "D"
                else:
                    return "P"
            else:
                return "0"
    else:
        if prop.image.mean() == 1:
            return "-"
        else:
            if has_vline(prop.image) and has_vline(prop.image.T):
                return "1"
            else:
                tmp = prop.image.copy()
                tmp[[0, -1], :] = 1
                tmp[:, [0, -1]] = 1
                tmp_props = regionprops(label(tmp))
                tmp_euler = tmp_props[0].euler_number
                if tmp_euler == -3:
                    return "X"
                elif tmp_euler == -1:
                    return "/"
                else:
                    if prop.eccentricity > 0.5:
                        return "W"
                    else:
                        return "*"
    return "_"


image = plt.imread("images/symbols.png")
labeled = label(image.mean(2) > 0)

props = regionprops(labeled)
result = {}
for prop in props:
    symbol = recognize(prop)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1

print(result, f'\n\r{(1 - result.get("_", 0) / np.max(labeled)) * 100}%')
