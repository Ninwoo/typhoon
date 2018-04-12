
print('''
***********************************************
*         传感器设备检测程序                  *
*      程序说明：                             *
*      1. 使用ping命令检测设备是否在线        * 
*      2. 将检测结果保存在网关数据库中        *
*                                             *
*               author:joliu<joliu@s-an.org>  *
*               date: 2018-4-12               *
*********************************************** 
''')

import subprocess
import os
import pymysql
import time

def sdnToDatabase(sql):
    # 发送sql命令到数据库
    cmd = sql.split(' ')[0]
    try:
        conn = pymysql.connect(host='127.0.0.1', port=12306, user='root', passwd='Vudo3423', db='HiDockerwifi', charset='utf8')
        cursor = conn.cursor()
        cursor.execute(sql)
        if cmd == 'select':
            output = cursor.fetchall()
            status = True
        else:
            conn.commit()
            status = True
            output = ''
    except pymysql.Error as err_msg:
        status = False
        output = err_msg
    except Exception as err_msg:
        status = False
        output = err_msg
    finally:
        cursor.close()
        conn.close()
        return (status, output)


def getDeviceIDByIP(ipaddr):
    # 从数据库查找对应的设备编号
    sql = "select equip from portdb where ipaddress='%s'" % ipaddr
    
    result = sdnToDatabase(sql)
    if result[0]:
        if result[1] == ():
            return False
        print(result[0])
        return result[1][0][0]
    else:
        return False


def updateDeviceInfo(ipaddress, equipid, device_status, delay):
    # 根据ip地址更新设备
    sql = "select * from deviceinfo where ipaddress='%s'" % ipaddress
    (status, result) = sdnToDatabase(sql)
    if status:
        if result == ():
            
            sql = "insert into deviceinfo (equipid, ipaddress, status, \
                  delay) VALUES ('%s', '%s',%d ,'%s')" % (equipid, ipaddress,\
                  device_status, delay)
        else:
            sql = "update deviceinfo set status=%d,delay='%s' where ipaddress='%s'" % \
                  (1, delay, ipaddress)
            
        (status, output) = sdnToDatabase(sql)
        if not status:
            return False
        return True
    else:
        print("connet database error")
        return False
    

def pingTestHost(ip):
    # 使用ping检测host设备的网络通信情况
    cmd = 'ping -c 1 -w 1 ' + ip
    equipid = getDeviceIDByIP(ip)
    if not equipid:
        return False
    # 执行ping命令
    (status, output) = subprocess.getstatusoutput(cmd)
    if status == 0:
        # 如果检测设备正常，获取单次检测的时延
        delayTime = output.split('\n')[1].split(' ')[-2].split('=')[1]
        status = 1
    else:
        delayTime = '-'
        status = 0
    return updateDeviceInfo(ip, equipid, status, delayTime)

if __name__ == "__main__":
    host = os.getenv('HOST')
    while True:
        print(host)
        print(pingTestHost(host))
        time.sleep(1)
