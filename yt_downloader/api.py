import re
from flask import Flask, jsonify, request, send_file, json
import youtube_downloader

app = Flask(import_name = '__main__')

@app.route('/download', methods = ['GET'])
def run():
    video = youtube_downloader.Video(youtube_downloader.__DATA_URL__, youtube_downloader.__VIDEO_ROUTE__, youtube_downloader.__IMAGES_ROUTE__)
    url = request.args.get("url")
    do = video.getInfo(url, youtube_downloader.YouTube(url))
    if do == True:
        video.imgDownload(url)
        video.videoDownload(url, True)
        return jsonify({"TITLE":youtube_downloader.YouTube(url).title, 
                         "DESCRIPTION":youtube_downloader.YouTube(url).description,
                         "THUMBNAIL":youtube_downloader.YouTube(url).thumbnail_url})
    else:
        return jsonify({"Error": "Video is duplicated"})


@app.route('/json_data', methods = ['GET'])
def jsonfile():
    with open(youtube_downloader.__DATA_URL__, "r", encoding="utf-8") as file:
        response = app.response_class(
        response=json.dumps(json.load(file), indent= 4, sort_keys=True, ensure_ascii=False),
        status=200,
        mimetype='application/json')
        return response

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
    run()
    jsonfile()




# Crear otro archivo python que va a leeer la pagina web y va a imprimirla
# O intentarlo en angular