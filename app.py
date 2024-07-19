from flask import Flask, request, render_template, redirect, url_for
import whisper
from pydub import AudioSegment
import os


from pydub.utils import which

AudioSegment.converter = which("ffmpeg")


app = Flask(__name__)
model = whisper.load_model("base")

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
        
        # Transcribe the audio file
        result = model.transcribe(file_path)
        transcription = result["text"]
        
        return render_template('index.html', transcription=transcription, audio_file=file_path)

if __name__ == '__main__':
    app.run(debug=True)
