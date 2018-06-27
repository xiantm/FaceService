### 在docker中运行

##### 使用docker-compose
```
$ docker-compose build
$ docker-compose up -d
#关闭
$ docker-compose down
```

##### 不使用docker-compose
```
$ docker run --name mysql -p 3306:3306 -v `pwd`/dbdata:/docker-entrypoint-initdb.d -e MYSQL_DATABASE=face -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -d mysql:5.7.11
```


