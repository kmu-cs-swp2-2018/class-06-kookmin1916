usonic_data = []

# usonic_data 초기값
for i in range(10):
    usonic_data.append(40)

def callback(data):
    global usonic_data
    usonic_data.append(data.data)
    usonic_data.pop(0)

def sensorFilter():
    sorted_usonic_data = sorted(usonic_data)
    result = 0
    for i in range(3, 7):
        result += sorted_usonic_data[i]
    return result / 4
