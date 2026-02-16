from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
COOKIE_FILE = "cookies.txt"

# Create folders
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# ===============================
# COMMON YT-DLP OPTIONS
# ===============================
def get_ydl_opts(quality):

    filename = f"{DOWNLOAD_FOLDER}/{uuid.uuid4()}.%(ext)s"

    ydl_opts = {

        "outtmpl": filename,

        "quiet": True,

        "noplaylist": True,

        "nocheckcertificate": True,

        "ignoreerrors": False,

        "no_warnings": True,

        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    # Use cookies if exists
    if os.path.exists(COOKIE_FILE):

        ydl_opts["cookiefile"] = COOKIE_FILE


    # MP3
    if quality == "mp3":

        ydl_opts["format"] = "bestaudio/best"

        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]

    else:

        ydl_opts["format"] = quality


    return ydl_opts


# ===============================
# GET INFO
# ===============================
@app.route("/get_info", methods=["POST"])
def get_info():

    url = request.form.get("url")

    if not url:

        return jsonify({"error": "Enter URL"}), 400

    try:

        ydl_opts = get_ydl_opts("best")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            return jsonify({

                "title": info.get("title"),

                "thumbnail": info.get("thumbnail"),

                "duration": info.get("duration")

            })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# ===============================
# DOWNLOAD
# ===============================
@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")

    quality = request.form.get("quality", "best")

    if not url:

        return "URL required", 400

    try:

        ydl_opts = get_ydl_opts(quality)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filename = ydl.prepare_filename(info)

            if quality == "mp3":

                filename = filename.rsplit(".", 1)[0] + ".mp3"


        return send_file(filename, as_attachment=True)


    except Exception as e:

        return f"Download failed: {str(e)}", 500


# ===============================
# HOME
# ===============================
@app.route("/")
def home():

    return render_template("index.html")


# ===============================
# RUN
# ===============================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)

