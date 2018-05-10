from controler import execute
import sys
import pymysql
import json

def findDevicePort(deviceID):
    output = ''
    try:
        sql = 'select port from portdb where equip="%s"' % deviceID
        conn = pymysql.connect(host='127.0.0.1', port=12306, user='root', passwd='Vudo3423', db='HiDockerwifi', charset='utf8')
        cur = conn.cursor()
        cur.execute(sql)
        output = cur.fetchone()
        #print(output)
    except pymysql.Error as err_msg:
        print(err_msg)
    except Exception as err_msg:
        print(err_msg)
    finally:
        cur.close()
        conn.close()
        return output

def Print(data):
    print(format(data, "<20"), end='')

def PrintTitle(title):
    for t in title:
        Print(t)
    print('')

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: nodeID database_name")
        exit(0)
    port = findDevicePort(sys.argv[1])[0]
    cmd = "controller&show&%s" % sys.argv[2]

    (status, output) = execute(port, cmd)
    if status == 0:
        print("can't find this database, please check your input")
    if sys.argv[2] == 'datacach':
        output = json.loads(output)
        title_list = ['DeviceID', 'Data', 'Updata Time', 'Status']
        PrintTitle(title_list)
        if output == []:
            output = None
        else:
            for items in output:
                items.remove(items[0])
                for item in items:
                    Print(item)
                print('')
    elif sys.argv[2] == 'decide':

