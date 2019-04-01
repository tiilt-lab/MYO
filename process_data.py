import csv
import numpy as np


initial_data = np.load("train_set.npz")

x=initial_data['x']
y=initial_data['y']
#x = np.ndarray.tolist(initial_data['x'])
#y = np.ndarray.tolist(initial_data['y'])

for val in y:
    val = np.append(val, 0)

gesture = np.array([[0, 0, 0, 0, 0, 1]])

with open('myo_emg.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    data_group = np.array([])
    for row in csv_reader:
        i = i + 1
        row = row[1:]
        if i == 1:
            data_group = list(map(int, row))
        elif i == 5:
            for j in range(len(data_group)):
                data_group[j] = round(data_group[j]/5)
            x = np.vstack((x, np.array([data_group])))
            y = np.vstack((y, gesture))
            data_group = np.array([])
            i = 0
        else:
            for j in range(len(data_group)):
                data_group[j] = data_group[j] + int(row[j])

print(np.asarray(x))
print(np.asarray(y))

np.savez("train_set2.npz", x=np.asarray(x), y=np.asarray(y))
