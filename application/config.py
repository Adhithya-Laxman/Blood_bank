class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Password123@localhost:5432/bloodbank"
    DEBUG = True