from flask import Flask, request, render_template, redirect, url_for
import whisper
from pydub import AudioSegment
import os

from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from apps.config import config

# SQLAlchemyをインスタンス化する
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

login_manager.login_view = "auth.signup"
login_manager.login_message = ""

# create_app関数を作成する
def create_app(config_key):
    # Flaskインスタンス生成
    app = Flask(__name__)
    # コンフィグを.envから読み込む
    # app.config.from_envvar("APPLICATION_SETTINGS")

    # config_keyにマッチする環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])
    # アプリのコンフィグ設定をする
    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI=
            f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f",
        # SQLをコンソールログに出力する設定
        SQLALCHEMY_ECHO=True
    )

    csrf.init_app(app)

    # SQLAlchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを連携する
    Migrate(app, db)

    login_manager.init_app(app)

    # crudパッケージからviewsをimportする
    from apps.crud import views as crud_views

    # register_blueprintを使いviewsのcrudをアプリへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.mojiokoshi import views as mojiokoshi_views

    app.register_blueprint(mojiokoshi_views.mojiokoshi, url_prefix="/mojiokoshi")

    return app

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'file' not in request.files:
#         return redirect(request.url)
    
#     file = request.files['file']
#     if file.filename == '':
#         return redirect(request.url)
    
#     if file:
#         file_path = os.path.join("static", file.filename)
#         file.save(file_path)
        
#         # Transcribe the audio file
#         result = model.transcribe(file_path)
#         transcription = result["text"]
        
#         return render_template('index.html', transcription=transcription, audio_file=file_path)

# if __name__ == '__main__':
#     app.run(debug=True)
