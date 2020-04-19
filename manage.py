from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from wlmooe import create_app
from exts import db
from apps import models as common_models
from apps.cms import models as cms_models
from apps.front import models as front_models


Teacher = cms_models.Teacher
Student = front_models.Student


app = create_app()
manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)



if __name__ == '__main__':
    manager.run()