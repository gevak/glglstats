import dataclasses
from typing import List

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import analysis
import self_correlation
from common import SongId

ARTISTS_DATA = pd.read_csv(analysis.ARTISTS_DATA_PATH).round(2)
CHART_DATA = pd.read_csv(analysis.CHART_DATA_PATH).round(2)

LABELS = {
    "artist_name": "Artist",
    "song_name": "Song",
    "score": "Compressed size",
    "year": "Year",
    "chart_index": "Chart Index",
}

CORRELATION_HOVER_TEMPLATE = "<b>%{x}</b>" \
                             "<extra>%{z}</extra>"

TEMPLATE = 'plotly'


def plot_self_correlation(sid: SongId, theme: str):
    """
    Based on: https://colinmorris.github.io/SongSim/#/about
    https://colinmorris.github.io/SongSim/#/12daysofxmas
    https://colinmorris.github.io/SongSim/#/gallery
    https://github.com/AllenThomasDev/LyricVisualizer/blob/master/app.py
    """
    pass
    lyrics = analysis.get_song_result(sid, analysis.SOURCES, save_to_cache=True).lyrics
    df = self_correlation.generate_heatmap(lyrics)
    fig = go.Figure(layout=go.Layout(
        hovermode='closest',
        template='plotly_dark',
        showlegend=False,
        xaxis={
            'ticks': '',
            'zeroline': False,
            'showticklabels': False,
            'showline': False,
            'showgrid': False,
            'tickmode': "array",
            'ticktext': df['words'],
            'tickvals': [x for x in range(len(df['words']))],
        },
        yaxis={
            'ticks': '',
            'zeroline': False,
            'showticklabels': False,
            'showline': False,
            'showgrid': False,
            'tickmode': "array",
            'ticktext': df['words'],
            'tickvals': [x for x in range(len(df['words']))],

        },
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=0  # top margin
        )
    ))
    fig.add_trace(
        go.Heatmap(
            z=df['z'],
            colorscale=theme,
            hoverongaps=False,
            hoverinfo="x+y+z",
            hovertemplate=CORRELATION_HOVER_TEMPLATE,
        ))

    fig.update_traces(showlegend=False, showscale=False)
    # TODO: Add lyrics on the side and illuminate the selected word?
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_layout(margin=go.layout.Margin(
        l=0,  # left margin
        r=0,  # right margin
        b=0,  # bottom margin
        t=0,  # top margin
    ))
    return fig


def hit_song_repetitiveness_by_year(years: List[int] = None):
    df = CHART_DATA
    groups = df.groupby("year")
    max_df = df.loc[groups['score'].idxmax()].reset_index(drop=True)
    max_df['type'] = 'max'
    min_df = df.loc[groups['score'].idxmin()].reset_index(drop=True)
    min_df['type'] = 'min'
    mean_df = groups['score'].mean().to_frame().reset_index()
    mean_df['song_name'] = ''
    mean_df['artist_name'] = ''
    mean_df['chart_index'] = ''
    mean_df['type'] = 'avg'
    summary_df = pd.concat([min_df, mean_df, max_df], ignore_index=True, sort=True)
    fig = px.line(summary_df, x='year', y='score', color='type',
                  color_discrete_map={"min":"red", "avg":"orange", "max":"green"},
                  hover_data={"song_name": True, "artist_name": True, 'type': False, 'chart_index': True},
                  labels=LABELS, template=TEMPLATE)
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_layout(
        title_font_family="sans-serif",
        title={
            'text': "כמה מגוונים היו שירי המצעד לאורך השנים",
            'y': 0.92,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
    )
    return fig


def repetitiveness_by_chart_index(years: List[int] = None):
    df = CHART_DATA
    if years:
        df = df[df['year'].isin(years)]
    groups = df.groupby("chart_index")
    mean_df = groups['score'].mean().to_frame().reset_index()
    mean_df["score"] = mean_df["score"].astype(float)
    fig = px.bar(mean_df, x='chart_index', y='score', color='score',
                 color_continuous_scale=["red", "yellow", "green"], range_color=[0.3, 0.9], range_x=[0, 26],
                 range_y=[0, 1],
                 template=TEMPLATE, labels=LABELS)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_layout(margin=go.layout.Margin(
        l=0,  # left margin
        r=0,  # right margin
        b=0,  # bottom margin
        t=0,  # top margin
    ))
    return fig


def repetitiveness_by_artist(artist_names=None):
    df = ARTISTS_DATA
    df['median'] = df.groupby('artist_name')['score'].transform('median')
    df = df.sort_values(by='median', ascending=False)
    if artist_names:
        df = df[df['artist_name'].isin(artist_names)]
    groups = df.groupby("artist_name")
    mean_df = groups['score'].mean().to_frame().reset_index()
    mean_df = mean_df.sort_values('score', ascending=True)
    # fig = px.bar(mean_df, x='artist_name', y='score', title="Song repetitiveness by artist name", color='score',
    #             color_continuous_scale=["red", "yellow", "green"])
    fig = px.box(df, y='artist_name', x='score', points="all",
                 hover_data={"song_name": True, "artist_name": False}, height=200 + len(mean_df) * 100,
                 labels=LABELS, template=TEMPLATE)
    fig.update_xaxes(side='top', range=[0, 1], title="")
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True, title="")
    fig.update_layout(margin=go.layout.Margin(
        l=0,  # left margin
        r=0,  # right margin
        b=0,  # bottom margin
        t=0,  # top margin
    ))
    return fig


def most_repetitive_songs(df = CHART_DATA, years: List[int] = None, artist_names: List[str] = None):
    if years:
        df = df[df['year'].isin(years)]
    if artist_names:
        df = df[df['artist_name'].isin(artist_names)]
    df = df.sort_values(by='score', ascending=False)
    df = pd.concat([df.head(1), df.tail(25)])
    df['song_name'] = df['artist_name'] + ' - ' + df['song_name']
    fig = px.bar(df, y='song_name', x='score',
                 hover_data={"song_name": False, "score": True}, height=725, range_y=[-1, 26],
                 labels=LABELS, template=TEMPLATE, color='score', color_continuous_scale=["red", "yellow", "green"],
                 range_color=[0.3, 0.9])
    fig.update_xaxes(side='top', title="", range=[0, 1])
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True, title="")
    fig.update_layout(margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0, #top margin
    ))
    return fig


def main():
    repetitiveness_by_artist(["אלה לי"]).show()


if __name__ == "__main__":
    main()
