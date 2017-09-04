# music.pls

**Play any playlist from Yandex.Music in your own player.**

Usage:

1. Clone and run (`FLASK_APP=./musicpls/__index__.py flask run`)
2. Open `http://127.0.0.1:5757/users/[username]/playlists/[id].m3u` as a playlist in your player

## To do

- caching tracks (and possibly playlists) for offline listening
- HTML view w/ search, artist/album pages (and playlists) for lighter browsing experience
- bug? Audacious (and possibly other players) start downloading every single track instead of parsing `#EXTINF` comments
