from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# ======================
# HOME
# ======================

@app.route("/")
def home():
    return render_template("index.html")


# ======================
# GET INFO
# ======================

@app.route("/get_info", methods=["POST"])
def get_info():

    url = request.form.get("url")

    if not url:
        return jsonify({"error": "No URL"}), 400

    try:

        ydl_opts = {

            'quiet': True,

            'cookiefile': 'cookies.txt',

            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            return jsonify({

                "title": info.get("title"),

                "thumbnail": info.get("thumbnail")

            })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# ======================
# DOWNLOAD
# ======================

@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")

    quality = request.form.get("quality")

    if not url:
        return "URL missing"


    filename = f"{DOWNLOAD_FOLDER}/{uuid.uuid4()}.%(ext)s"


    # FORMAT FIX

    if quality == "mp3":

        format_code = "bestaudio/best"

    elif quality == "720p":

        format_code = "bestvideo[height<=720]+bestaudio/best"

    elif quality == "1080p":

        format_code = "bestvideo[height<=1080]+bestaudio/best"

    else:

        format_code = "best"


    ydl_opts = {

        'format': format_code,

        'outtmpl': filename,

        'cookiefile': 'cookies.txt',

        'merge_output_format': 'mp4',

        'quiet': True,

        'noplaylist': True
    }


    if quality == "mp3":

        ydl_opts['postprocessors'] = [{

            'key': 'FFmpegExtractAudio',

            'preferredcodec': 'mp3'

        }]


    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filepath = ydl.prepare_filename(info)

            if quality == "mp3":

                filepath = filepath.rsplit(".", 1)[0] + ".mp3"


        return send_file(filepath, as_attachment=True)

    except Exception as e:

        return f"Download failed: {str(e)}"


# ======================
# RUN
# ======================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)

  
       
