import pymysql
def showDevice():
    output = ''
    try:
        sql = 'select * from deviceinfo'
        conn = pymysql.connect(host='127.0.0.1', port=12306, user='root', passwd='Vudo3423', db='HiDockerwifi', charset='utf8')
        cur = conn.cursor()
        cur.execute(sql)
        output = cur.fetchall()
        #print(output)
    except pymysql.Error as err_msg:
        print(err_msg)
    except Exception as err_msg:
        print(err_msg)
    finally:
        cur.close()
        conn.close()
        return output

if __name__ == "__main__":
    device_data = showDevice()
    print(format("deviceID", "<20"), format("IP", "<20"), format("status", "<20"), format("network status"))
    for device in device_data:
        if device[3] == 1:
            status = 'on-line'
        else:
            status = 'off-line'
        #print("%s\t\t%s\t%s\t%s" % (device[1], device[2], status, device[4]))
        print(format(device[1], "<20"), format(device[2], "<20"), format(status, "<20"), format(device[4]))
