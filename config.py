class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:moringa@localhost/keja'


class ProdConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:moringa@localhost/keja'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:moringa@localhost/keja'


config_options = {
'development':DevConfig,
'production':ProdConfig
}