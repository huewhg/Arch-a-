import os

basedir = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_FOLDER = "../frontend/templates/"
STATIC_FOLDER = "../frontend/static/dest/"
TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'project.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
