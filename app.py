from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

# Create downloads folder
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# =========================
# GET VIDEO INFO
# =========================
@app.route("/get_info", methods=["POST"])
def get_info():

    url = request.form.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:

        ydl_opts = {

            'quiet': True,

            'noplaylist': True,

            # ✅ VERY IMPORTANT LINE (BOT FIX)
            'cookiefile': 'cookies.txt',

            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web']
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            return jsonify({

                "title": info.get("title"),

                "thumbnail": info.get("thumbnail")

            })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# =========================
# DOWNLOAD VIDEO / MP3
# =========================
@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")

    quality = request.form.get("quality", "best")

    if not url:

        return "URL required", 400

    try:

        filename = f"{DOWNLOAD_FOLDER}/{uuid.uuid4()}.%(ext)s"

        ydl_opts = {

            'format': 'bestaudio/best' if quality == "mp3" else quality,

            'outtmpl': filename,

            # ✅ VERY IMPORTANT LINE (BOT FIX)
            'cookiefile': 'cookies.txt',

            'noplaylist': True,

            'quiet': True,

            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web']
                }
            }
        }


        # Convert to MP3
        if quality == "mp3":

            ydl_opts['postprocessors'] = [{

                'key': 'FFmpegExtractAudio',

                'preferredcodec': 'mp3',

                'preferredquality': '192'

            }]


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filepath = ydl.prepare_filename(info)

            if quality == "mp3":

                filepath = filepath.rsplit(".", 1)[0] + ".mp3"


        return send_file(filepath, as_attachment=True)


    except Exception as e:

        return f"Download failed: {str(e)}", 500


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():

    return render_template("index.html")


# =========================
# RUN FOR RENDER
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)


          



