# app.py

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from pydub import AudioSegment
from pydub.utils import which
import whisper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite データベースのパス
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Whisper モデルのロード
model = whisper.load_model("base")

# Pydub の設定
AudioSegment.converter = which("ffmpeg")

# データベースのモデル定義
class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_file = db.Column(db.String(200), nullable=False)
    transcription = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Transcription {self.id}>'

# データベースの初期化
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join("static", file.filename)
        file.save(file_path)
        
        # 音声ファイルの文字起こし
        result = model.transcribe(file_path)
        transcription_text = result["text"]
        
        # データベースに保存
        transcription_entry = Transcription(audio_file=file_path, transcription=transcription_text)
        db.session.add(transcription_entry)
        db.session.commit()
        
        return render_template('index.html', transcription=transcription_text, audio_file=file_path)
    
@app.route('/history')
def history():
    transcriptions = Transcription.query.all()
    return render_template('history.html', transcriptions=transcriptions)

if __name__ == '__main__':
    app.run(debug=True)
