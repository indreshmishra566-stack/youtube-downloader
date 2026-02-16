import os
from flask import Flask, render_template, request, send_file
import yt_dlp
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
COOKIE_FILE = "cookies.txt"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    url = request.form["url"]
    quality = request.form.get("quality", "best")

    try:

        filename = str(uuid.uuid4()) + ".mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {
            'format': quality,
            'outtmpl': filepath,

            # IMPORTANT
            'cookiefile': COOKIE_FILE,

            # EXTRA FIX
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'quiet': False,
            'no_warnings': False,

            # CRITICAL FIX
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web']
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


  
  
