import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASK_MAIL_SENDER = 'Flasky Admin <flasky@example.com'
    FLASKY_ADMIN = 'yangz@zzy.com'
    FLASKY_MINDS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 5
    FLASKY_COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_POER = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:joze@localhost:3306/sae'
    APP_KEY = '3669231834'
    APP_SECRET = '7e6bf0606f471415c0c95cdb406142b9'
    CALLBACK_URL = 'http://yangzhuoze.applinzi.com/'
    APIKEY = 'c41a36cd0060dce2f4c88721d7822e22'
    WEATHER_API = 'http://apis.baidu.com/heweather/weather/free?city='
    WEATHER_CITY = 'guangzhou'

class ProductionConfig(Config):
    if 'SERVER_SOFTWARE' in os.environ:
        import sae.const
        SQLALCHEMY_DATABASE_URI = 'mysql://' + sae.const.MYSQL_USER + \
            ':' + sae.const.MYSQL_PASS + '@' + sae.const.MYSQL_HOST  + ':' + \
            sae.const.MYSQL_PORT + '/' + sae.const.MYSQL_DB
        SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        SQLALCHEMY_POOL_RECYCLE = 10
    APP_KEY = '3669231834'
    APP_SECRET = '7e6bf0606f471415c0c95cdb406142b9'
    CALLBACK_URL = 'http://yangzhuoze.applinzi.com/auth/callback'
    APIKEY = 'c41a36cd0060dce2f4c88721d7822e22'
    WEATHER_API = 'http://apis.baidu.com/heweather/weather/free?city='
    WEATHER_CITY = 'guangzhou'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}