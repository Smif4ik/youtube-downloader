import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'cookiefile': 'cookies.txt',
        'extractor_args': {'youtube': {'player_client': ['web']}},
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Произошла ошибка при скачивании: {e}"

if __name__ == '__main__':
    app.run(debug=True)