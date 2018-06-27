import pymysql

try:
    pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='face', charset='utf8')
    print(1)
except:
    print(0)