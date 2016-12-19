import os

class DBConfig(object):
    DB_ON = True
    DB_DRIVER = 'mysql'
    DB_ORM = False

class DevelopmentDBConfig(DBConfig):
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    DB_DATABASE_NAME = 'red_ribbon'
    DB_HOST = 'localhost'
    DB_PORT = 3306
    # """ unix_socket is used for connecting with MAMP. Take this out if you aren't using MAMP """
    # DB_OPTIONS = {
    #     'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock'
    # }

class StagingDBConfig(DBConfig):
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    DB_DATABASE_NAME = 'mydb'
    DB_HOST = 'localhost'

class ProductionDBConfig(DBConfig):
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    DB_DATABASE_NAME = 'mydb'
    DB_HOST = 'localhost'
