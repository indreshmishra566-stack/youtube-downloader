from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# Get video info
@app.route("/get_info", methods=["POST"])
def get_info():

    url = request.form["url"]

    ydl_opts = {
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)

        return jsonify({

            "title": info["title"],
            "thumbnail": info["thumbnail"]
        })


# Download video
@app.route("/download", methods=["POST"])
def download():

    url = request.form["url"]
    quality = request.form["quality"]

    if quality == "mp3":

        ydl_opts = {

            'format': 'bestaudio/best',

            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }

    else:

        ydl_opts = {

            'format': quality,

            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)

        if quality == "mp3":
            filename = filename.replace(".webm", ".mp3")

    return send_file(filename, as_attachment=True)


@app.route("/")
def index():
    return render_template("index.html")


# ✅ IMPORTANT FIX FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)    

     
     
