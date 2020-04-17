from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from wlmooe import create_app
from exts import db
from apps.cms import models as cms_models


CMSUser = cms_models.Teacher



app = create_app()
manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)



if __name__ == '__main__':
    manager.run()