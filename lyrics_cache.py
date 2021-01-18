import dataclasses
import json
import logging
from typing import List, Mapping, Set

from common import SongResult, SongId, LyricsSource

log = logging.getLogger("songs")

CACHE_PATH = "lyrics_cache.json"
SINGLETON = None


class LyricsCache:
    def __init__(self, path=None):
        if not path:
            path = CACHE_PATH
        self.path = path
        try:
            self.cache = json.load(open(path, "r", encoding='utf8'))
            # Decode from dict to dataclass
            for song, result in self.cache.items():
                self.cache[song] = SongResult(**result)
        except Exception as e:
            log.warning(f"Got exception reading cache: {e}")
            self.cache = {}

    def update(self, results: List[SongResult]):
        for r in results:
            self.cache[r.get_dict_key()] = r

    def flush(self):
        f = open(self.path, "w", encoding="utf8")
        encoded_cache = {s: dataclasses.asdict(r) for (s, r) in self.cache.items()}
        json.dump(encoded_cache, f, ensure_ascii=False)

    def get_lyrics(self, sid: SongId):
        value = self.cache.get(sid.get_dict_key(), None)
        if value and value.lyrics:
            return value.lyrics
        return None

    def get_songs_for_artist(self, artist_name) -> Set[SongId]:
        return {v.to_sid() for k, v in self.cache.items() if v.artist_name == artist_name}


def get_cache() -> LyricsCache:
    global SINGLETON
    if not SINGLETON:
        SINGLETON = LyricsCache()
    return SINGLETON
