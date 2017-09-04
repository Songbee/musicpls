import itertools
from flask import Flask, Response, render_template
from mutagen.easyid3 import EasyID3

from .client import YandexMusic
from .util import SeekableBuffer


app = Flask(__name__)
ym = YandexMusic()


@app.route("/stream/<int:id>")
def stream(id):
    track = ym.get_track(id).json()
    src_url = ym.get_download_link(track)

    r = ym.head(src_url, headers={})
    headers = {
        "Content-Type": r.headers["Content-Type"],
        "Content-Length": r.headers["Content-Length"],
    }

    tags = EasyID3()
    tags["length"] = [track["track"]["durationMs"]]
    tags["artist"] = [a["name"] for a in track["artists"]]
    tags["title"] = [track["track"]["title"]]
    tags["album"] = [track["track"]["albums"][0]["title"]]


    def streaming_fn():
        r = ym.get(src_url, headers={}, stream=True)
        sb = SeekableBuffer(r.raw)
        tags.save(sb)
        sb.seek(0)
        return sb.read()  # XXX performance ???

    return Response(streaming_fn(), headers=headers)


@app.route("/users/<owner>/playlists/<int:playlist_id>.m3u")
def playlist(owner, playlist_id):
    """
    Grabs a playlist and converts it to M3U playlist file with correct tags
    and localhost links.
    """

    r = ym.get_playlist(owner, playlist_id)
    pls = r.json()["playlist"]

    return Response(
        render_template("playlist.m3u", tracks=pls["tracks"]),
        mimetype="audio/x-mpegurl")
