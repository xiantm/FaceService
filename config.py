import os
basedir = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(basedir, "app", "static", "image")
if not os.path.exists(image_path):
    os.mkdir(image_path)
ip = "127.0.0.1"
port = "5000"

mysql_url = 'mysql+pymysql://root@localhost:3306/face'
# docker 环境下更改数据库url
in_docker = os.environ.get('IN_DOCKER', None)
print(in_docker)
if in_docker:
    mysql_url = 'mysql+pymysql://root@db:3306/face'

class Config(object):
    SQLALCHEMY_DATABASE_URI = mysql_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# docker exec mysql sh -c 'exec mysqldump --all-databases -uroot -p""' > ./dbdata/init.sql