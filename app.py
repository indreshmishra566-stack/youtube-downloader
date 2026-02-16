from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")
    quality = request.form.get("quality")

    filename = f"{DOWNLOAD_FOLDER}/{uuid.uuid4()}.%(ext)s"


    if quality == "mp3":

        format_code = "bestaudio/best"

    elif quality == "720p":

        format_code = "bestvideo[height<=720]+bestaudio/best"

    elif quality == "1080p":

        format_code = "bestvideo+bestaudio/best"

    else:

        format_code = "best"


    ydl_opts = {

        "format": format_code,

        "outtmpl": filename,

        "quiet": True,

        "merge_output_format": "mp4",


        # ✅ THIS IS THE REAL FIX
        "extractor_args": {

            "youtube": {

                "player_client": ["android_creator"]

            }

        },


        # ✅ ADD THIS
        "http_headers": {

            "User-Agent":
            "com.google.android.youtube/17.31.35 (Linux; U; Android 11)"

        }

    }


    if quality == "mp3":

        ydl_opts["postprocessors"] = [{

            "key": "FFmpegExtractAudio",

            "preferredcodec": "mp3"
        }]


    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filepath = ydl.prepare_filename(info)

            if quali
