from flask import Flask, request, render_template, redirect, url_for
import whisper
from pydub import AudioSegment
from pydub.utils import which
import os

from apps.crud.forms import UserForm
from flask import Blueprint
# dbをimportする
from apps.app import db
# Userクラスをimportする
from apps.crud.models import User
from flask_login import login_required

# Whisper モデルのロード
model = whisper.load_model("base")

# Pydub の設定
AudioSegment.converter = which("ffmpeg")

# データベースのモデル定義
class Transcription(db.Model):
    __tablename__ = "transcription"
    id = db.Column(db.Integer, primary_key=True)
    audio_file = db.Column(db.String(200), nullable=False)
    transcription = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Transcription {self.id}>'

# データベースの初期化
# with mojiokoshi.app_context():
#     db.create_all()

# Blueprintでmojiokoshiアプリを生成する
mojiokoshi = Blueprint(
    "mojiokoshi",
    __name__,
    template_folder="templates",
    static_folder="static",
)
# データベースの初期化
# with mojiokoshi.app_context():
#     db.create_all()

@login_required
def index():
    return render_template("crud/index.html")

# indexエンドポイントを作成しindex.htmlを返す
@mojiokoshi.route("/")
@login_required
def index():
    form = UserForm()
    return render_template("mojiokoshi/index.html", form=form)


@mojiokoshi.route('/transcribe', methods=['POST'])
@login_required
def transcribe_audio():
    # UserFormをインスタンス化する
    form = UserForm()
    
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join("apps/mojiokoshi/static", file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
        # Transcribe the audio file
        result = model.transcribe(file_path)
        transcription_text = result["text"]

        # データベースに保存
        transcription_entry = Transcription(audio_file=file_path, transcription=transcription_text)
        db.session.add(transcription_entry)
        db.session.commit()
        
        return render_template('mojiokoshi/index.html', transcription=transcription_text, audio_file=file_path, form=form)

@mojiokoshi.route('/history')
@login_required
def history():
    transcriptions = Transcription.query.all()
    return render_template('mojiokoshi/history.html', transcriptions=transcriptions)

if __name__ == '__main__':
    app.run(debug=True)