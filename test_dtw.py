import numpy as np
import math

from fastdtw import fastdtw

with open("exercises/bicep.txt", "r") as template_file:
    temp_arr =[]
    for line in template_file:
        formatted_line = line.strip()
        formatted_line = formatted_line.split(",")
        formatted_line = [float(i) for i in formatted_line]
        temp_arr.append(formatted_line)
    template_file.close()
#print(temp_arr)
x = np.array(temp_arr)

with open("exercises/bicep_4.txt", "r") as template_file:
    temp_arr =[]
    for line in template_file:
        formatted_line = line.strip()
        formatted_line = formatted_line.split(",")
        formatted_line = [float(i) for i in formatted_line]
        temp_arr.append(formatted_line)
    template_file.close()
#print(temp_arr)
y= np.array(temp_arr)

def dtw_distance_window(s1, s2, window):
    n = len(s1)
    m = len(s2)
    window = max(window, abs(n-m))   # Adjusting the window size
    DTW = np.zeros((n+1, m+1))
    for i in range(1, n+1):
        DTW[i, 0] = np.inf
    for i in range(1, m+1):
        DTW[0, i] = np.inf
    DTW[0,0] = 0
    for i in range(1, n+1):
        for j in range(max(1, i-window), min(m, i+window)+1):
            cost = np.linalg.norm(s1[i-1]-s2[j-1])
            DTW[i,j] = cost + min(DTW[i-1,j], DTW[i,j-1], DTW[i-1,j-1])
    return DTW[n,m]

print(dtw_distance_window(x, y, 1))