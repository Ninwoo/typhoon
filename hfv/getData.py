from controllMatrix import *

import time


print(updateDeviceTask('25', '192.168.12.1', 25))

while True:
    if getDeviceTask()[0] == -1:
        print(output)
        continue
    (id, data, dstIP, ctime) = getDeviceTask()[1]
    print(data)
    if data == 25:
        print('success')
    time.sleep(ctime)
