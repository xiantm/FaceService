from app import app,db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

#使用migrate绑定app和db
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001)
