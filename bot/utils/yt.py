# bot/utils/yt.py

from yt_dlp import YoutubeDL

def extract_playlist_audio_urls(query: str):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,
        'format': 'bestaudio/best',
        'noplaylist': False,
    }

    if not query.startswith('http'):
        ydl_opts['default_search'] = 'ytsearch'

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)

        # Se não for uma playlist, trata como vídeo único
        if 'entries' not in info:
            return [(info['url'], info.get('title', 'Unknown'))]

        result = []
        for entry in info['entries']:
            result.append((entry['url'], entry.get('title', 'Unknown')))
        return result