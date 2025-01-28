from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data['text']
    speed = data['speed']
    lang = 'en'

    slow_speed = speed == 'slow'
    tts = gTTS(text=text, lang=lang, slow=slow_speed)
    filename = 'output.mp3'
    tts.save(filename)
    file_url = f'/audio/{filename}'
    return jsonify({'url': file_url})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    text = data['text']
    speed = data['speed']
    lang = 'en'

    slow_speed = speed == 'slow'
    tts = gTTS(text=text, lang=lang, slow=slow_speed)
    filename = 'output.mp3'
    tts.save(filename)
    file_url = f'/audio/{filename}'
    return jsonify({'url': file_url})

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_file(os.path.join(os.getcwd(), filename), as_attachment=True, mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(debug=True)