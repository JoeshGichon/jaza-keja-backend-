class Config:
    SECRET_KEY="jwtsecretkey"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:access@localhost/kejadb'


class ProdConfig(Config):
    DEBUG=False

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY="jwtsecretkey"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:access@localhost/kejadb'


config_options = {
'development':DevConfig,
'production':ProdConfig
}