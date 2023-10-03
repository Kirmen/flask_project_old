import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    DB_NAME = os.getenv('DATABASE', 'test.db')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
