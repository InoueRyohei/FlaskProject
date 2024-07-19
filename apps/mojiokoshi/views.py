from flask import Flask, request, render_template, redirect, url_for
import whisper
from pydub import AudioSegment
import os

from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for
# dbをimportする
from apps.app import db
# Userクラスをimportする
from apps.crud.models import User
from flask_login import login_required

# Blueprintでmojiokoshiアプリを生成する
mojiokoshi = Blueprint(
    "mojiokoshi",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# indexエンドポイントを作成しindex.htmlを返す
@mojiokoshi.route("/")
def index():
    return render_template("mojiokoshi/index.html")


@mojiokoshi.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # UserFormをインスタンス化する
    form = UserForm()
    
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join("static", file.filename)
        file.save(file_path)
        
        # Transcribe the audio file
        result = model.transcribe(file_path)
        transcription = result["text"]
        
        return render_template('mojiokoshi/index.html', transcription=transcription, audio_file=file_path, form=form)

if __name__ == '__main__':
    app.run(debug=True)