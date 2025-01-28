from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Text-to-Speech Generator</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 0;
          background-color: #121212;
          color: white;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }

        .container {
          text-align: center;
          max-width: 500px;
          width: 100%;
          padding: 20px;
          background-color: #1e1e1e;
          border-radius: 10px;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }

        textarea {
          width: 100%;
          margin: 10px 0;
          padding: 10px;
          border: none;
          border-radius: 5px;
          resize: none;
          font-size: 16px;
        }

        select, button {
          margin: 5px;
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          font-size: 16px;
          cursor: pointer;
        }

        button {
          background-color: #6200ee;
          color: white;
          transition: background-color 0.3s;
        }

        button:hover {
          background-color: #3700b3;
        }

        select {
          background-color: #292929;
          color: white;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Text-to-Speech Generator</h1>
        <textarea id="text-input" placeholder="Type your text here..." rows="5"></textarea>
        <select id="voice-speed">
          <option value="fast">Fast</option>
          <option value="medium">Medium</option>
          <option value="slow">Slow</option>
        </select>
        <button id="speak-btn">Speak</button>
        <button id="download-btn">Download</button>
      </div>
      <script>
        const textInput = document.getElementById('text-input');
        const voiceSpeed = document.getElementById('voice-speed');
        const speakBtn = document.getElementById('speak-btn');
        const downloadBtn = document.getElementById('download-btn');
        
        speakBtn.addEventListener('click', () => {
          const text = textInput.value;
          const speed = voiceSpeed.value;
          const data = { text, speed };
          
          fetch('/speak', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          })
          .then(response => response.json())
          .then(data => {
            const audio = new Audio(data.url);
            audio.play();
          });
        });

        downloadBtn.addEventListener('click', () => {
          const text = textInput.value;
          const speed = voiceSpeed.value;
          const data = { text, speed };
          
          fetch('/download', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          })
          .then(response => response.json())
          .then(data => {
            const a = document.createElement('a');
            a.href = data.url;
            a.download = 'output.mp3';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
          });
        });
      </script>
    </body>
    </html>
    '''

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