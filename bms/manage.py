from flask_migrate import Migrate, MigrateCommand
from app.models import db
from app.app import create_app
from flask_script import Manager


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
