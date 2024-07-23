from pathlib import Path

basedir = Path(__file__).parent.parent

# SQLをコンソールログに出力する設定
SQLALCHEMY_ECHO=True

# BaseConfigクラスを作成する
class BaseConfig:
    SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
    WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"

# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

# BaseConfigクラスを継承してTestConfigクラスを作成する
class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

# config辞書にマッチングする
config = {
    "testing": TestConfig,
    "local": LocalConfig,
}
