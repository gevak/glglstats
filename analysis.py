import concurrent
import dataclasses
import logging
import traceback
from typing import Iterable, Sequence, List

import pandas as pd
from tqdm import tqdm

import common
import pop_charts
import compress_lib
import lyrics_cache
import re
from common import SongId, SongResult, LyricsSource

log = logging.getLogger("songs")

OFFLINE_CACHE_ONLY: Sequence[LyricsSource] = [lyrics_cache.get_cache(), common.HardcodedSongsSource()]
SOURCES = OFFLINE_CACHE_ONLY

CHART_DATA_PATH = "pop_chart_data.csv"
ARTISTS_DATA_PATH = "artists_data.csv"

def score_song(lyrics):
    cleaned_lyrics = lyrics.encode("cp1255", errors='replace').replace(b'?', b' ')
    new_length = len(compress_lib.compress_2(cleaned_lyrics))
    score = new_length / len(cleaned_lyrics)
    return score


def get_song_result(sid: SongId, prioritized_sources: Sequence[LyricsSource], chart_index: int = -1,
                    save_to_cache=False):
    lyrics = None
    for source in prioritized_sources:
        lyrics = source.get_lyrics(sid)
        if lyrics:
            regex = "|".join([re.escape(s) for s in ["..", "[", "פזמון", "פיזמון"]] + ['[ء-ي]+'])
            if re.search(regex, lyrics):
                # TODO(gevak): Try to handle .. better
                log.debug(f"Found special character in lyrics for {sid} in source {source}, ignoring")
                lyrics = None
                continue
            log.info(f'Found lyrics for song: {sid} in source: {source}')
            break

    if lyrics:
        try:
            result = SongResult(artist_name=sid.artist_name, song_name=sid.song_name,
                                lyrics=lyrics, score=score_song(lyrics), chart_index=chart_index)
            if save_to_cache:
                lyrics_cache.get_cache().update([result])
                lyrics_cache.get_cache().flush()
            return result
        except Exception as e:
            log.error(f"FAILED ENCODE for song {sid}: {e}")
            traceback.print_exc(limit=10)
            return None
    else:
        log.warning(f"Found no lyrics for song: {sid}")
        return None


def analyze_songs_parallel(songs: Iterable[SongId], prioritized_sources: Sequence[LyricsSource]):
    cache = lyrics_cache.get_cache()
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_song_result, prioritized_sources=prioritized_sources, sid=s, chart_index=i+1)
                   for i, s in enumerate(songs)]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as exc:
                log.error('generated an exception: %s' % repr(exc))
                traceback.print_exc(limit=10)

    # Save results to disk cache
    cache.update(results)
    cache.flush()
    return results


def results_for_year(year: int, prioritized_sources: Sequence[LyricsSource]):
    songs = pop_charts.song_chart_for_year(year)
    results = analyze_songs_parallel(songs, prioritized_sources)
    log.info("Found lyrics for %d out of %d songs for %d", len(results), len(songs), year)
    return results


def results_for_artist(artist_name: str, prioritized_sources: Sequence[LyricsSource]):
    songs = set()
    for source in prioritized_sources:
        songs.update(source.get_songs_for_artist(artist_name))
    log.info(f"Songs found for {artist_name}: {songs}")
    results = analyze_songs_parallel(songs, prioritized_sources)
    log.info("Found lyrics for %d out of %d songs for %s", len(results), len(songs), artist_name)
    return results


def export_chart_data(path=None):
    if not path:
        path = CHART_DATA_PATH
    years = pop_charts.YEARS
    df = pd.DataFrame()
    for year in tqdm(years):
        data = results_for_year(year, SOURCES)
        year_df = pd.DataFrame([dataclasses.asdict(d) for d in data])
        year_df['year'] = year
        year_df['decade'] = year - year % 10
        if 'lyrics' in year_df.columns:
            del year_df['lyrics']
        df = pd.concat([df, year_df], ignore_index=True)
    df.to_csv(path)


def export_artists_data(path=None):
    if not path:
        path = ARTISTS_DATA_PATH
    artists = pop_charts.ALL_ARTISTS
    df = pd.DataFrame()
    for artist in tqdm(artists):
        log.info(f"Getting songs for {artist}")
        data = results_for_artist(artist, SOURCES)
        artist_df = pd.DataFrame([dataclasses.asdict(d) for d in data])
        if 'lyrics' in artist_df.columns:
            del artist_df['lyrics']
        df = pd.concat([df, artist_df], ignore_index=True)
    df.to_csv(path)


def main():
    common.setup_logging("INFO")
    export_artists_data()
    export_chart_data()


if __name__ == "__main__":
    main()