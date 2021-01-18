import os
from dataclasses import dataclass
from typing import Set, Iterable
import logging
from dataclasses_json import dataclass_json


def setup_logging(level):
    logger = logging.getLogger("songs")
    handler = logging.StreamHandler()
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)


@dataclass_json
@dataclass(eq=True, frozen=True)
class SongId:
    artist_name: str
    song_name: str

    def get_dict_key(self):
        return "+".join([self.artist_name, self.song_name])


@dataclass_json
@dataclass
class SongResult:
    artist_name: str
    song_name: str
    lyrics: str
    score: float
    chart_index: int

    def get_dict_key(self):
        return "+".join([self.artist_name, self.song_name])

    def to_sid(self):
        return SongId(artist_name=self.artist_name, song_name=self.song_name)


def dict_key_to_song(dict_key: str):
    artist_name, song_name = dict_key.split("+")
    return SongId(artist_name, song_name)


class LyricsSource:
    def __init__(self):
        pass

    def get_lyrics(self, sid: SongId):
        raise NotImplementedError()

    def get_songs_for_artist(self, artist_name: str) -> Iterable[SongId]:
        return set()


class HardcodedSongsSource(LyricsSource):
    def __init__(self):
        LyricsSource.__init__(self)

    def get_lyrics(self, sid: SongId):
        song = " - ".join([sid.artist_name, sid.song_name])
        if os.path.exists(f"lyrics/{song}.txt"):
            print(f"Found hardcoded lyrics for {sid}")
            return open(f"lyrics/{song}.txt", "r", encoding='utf-8').read()
        return None

    def get_songs_for_artist(self, artist_name: str) -> Iterable[SongId]:
        return set()
