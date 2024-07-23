from flask import Flask, request, render_template, redirect, url_for
import whisper
from pydub import AudioSegment
from pydub.utils import which
import os

from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for
# dbをimportする
from apps.app import db
# Userクラスをimportする
from apps.crud.models import User
from flask_login import login_required

# Whisper モデルのロード
model = whisper.load_model("base")

# Pydub の設定
AudioSegment.converter = which("ffmpeg")

# Blueprintでmojiokoshiアプリを生成する
mojiokoshi = Blueprint(
    "mojiokoshi",
    __name__,
    template_folder="templates",
    static_folder="static",
)

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
        transcription = result["text"]
        
        return render_template('mojiokoshi/index.html', transcription=transcription, audio_file=file_path, form=form)

if __name__ == '__main__':
    app.run(debug=True)