
    # select format
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

        # bot bypass fix
        "extractor_args": {
            "youtube": {
                "player_client": ["android_creator"]
            }
        },

        "http_headers": {
            "User-Agent":
            "com.google.android.youtube/17.31.35 (Linux; Android 11)"
        }
    }


    # mp3 convert
    if quality == "mp3":

        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3"
        }]


    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filepath = ydl.prepare_filename(info)

            if quality == "mp3":

                filepath = filepath.rsplit(".", 1)[0] + ".mp3"


        return send_file(filepath, as_attachment=True)


    except Exception as e:

        return f"Error: {str(e)}"


# render port fix
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)

  
    
