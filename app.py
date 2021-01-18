import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly as px
from dash.dependencies import Input, Output, State

import plot
import pop_charts
from common import SongId

chart_repetitiveness_fig = plot.hit_song_repetitiveness_by_year()
DECADE_OPTIONS = [year for year in pop_charts.YEARS if year % 10 == 0] + ["נקה בחירה", "כל הזמנים"]

external_stylesheets = [
    dbc.themes.PULSE,
    {
        'href': 'https://use.fontawesome.com/releases/v5.15.1/css/all.css',
        'rel': 'stylesheet',
    },
]

PURPLE = "#593196"

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                    {"name": "og:title", "content": "GlglStats - ניתוח שירים רפטטיביים במצעד הפזמונים"},
                    {"name":"og:description", "content": "איזה אמנים יותר מבולבלים מיובל המבולבל? יצאנו לבדוק את הסטטיסטיקה"},
                    {"name": "og:image", "content": "/static/images/logo.png"}
                ],
                )
app.title = "GlglStats"
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "height": "100%",
    # 'display': 'inline-block',
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "textAlign": "right",
    "dir": "rtl",
    "backgroundColor": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "paddingRight": "2rem",
    "max-width": "max(76rem, 100vw - 20rem)",
    #"width": "max(76rem, 100vw - 20rem)",
    "padding": "1.5rem 0rem 0.5rem",
    "textAlign": "right",
    "dir": "rtl",
    "overflow-x": "hidden",
}

sidebar = html.Div(children=
[
    html.A(
        html.H2(
            "GlglStats", className="display-4",
            style={
                "font-weight": "bold",
                "-webkit-text-fill-color": "yellow",
                "-webkit-text-stroke-width": "3px",
                "-webkit-text-stroke-color": PURPLE}
        ),
        href="/", style={"text-decoration": "none"},
    ),
    html.Hr(),
    html.P(
        "זיהוי וניתוח סטטיסטי של שירים חזרתיים בעברית", className="lead"
    ),
    dbc.Nav(
        [
            dbc.NavLink("אודות", href="/", active="exact"),
            dbc.NavLink("מצעד הפזמונים", href="/charts", active="exact"),
            dbc.NavLink("נתונים בחלוקה לאמנים", href="/artists", active="exact"),
            dbc.NavLink("דפוסי חזרות אומנותיים", href="/autocorrelation", active="exact"),
            dbc.NavLink("איך זה עובד", href="/curious", active="exact"),
        ],
        vertical=True,
        pills=True,
    ),
],
    className="sidebar-wrapper d-none d-md-block",
    style=SIDEBAR_STYLE,
)

mobile_navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("אודות", href="/"), style={"dir": "rtl", "textAlign": "right"}),
        # TODO: Collapse on click?
        dbc.NavItem(dbc.NavLink("מצעד הפזמונים", href="/charts"), style={"dir": "rtl", "textAlign": "right"}),
        dbc.NavItem(dbc.NavLink("נתונים בחלוקה לאמנים", href="/artists"), style={"dir": "rtl", "textAlign": "right"}),
        dbc.NavItem(dbc.NavLink("דפוסי חזרות אומנותיים", href="/autocorrelation"),
                    style={"dir": "rtl", "textAlign": "right"}),
        dbc.NavItem(dbc.NavLink("איך זה עובד", href="/curious"), style={"dir": "rtl", "textAlign": "right"}),
    ],
    brand="GlglStats",
    brand_href="/",
    brand_style={
        "font-weight": "bold",
        "color": "yellow",
    },
    color="primary",
    dark=True,
    className="d-md-none",
    style={'top': '0px',
           'left': '0px',
           'right': '0px',
           "position": "fixed",  # TODO: Comment?
           "display": "block",
           "z-index": "1",
           }
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

footer2 = html.Footer(children=[
    dcc.Markdown("Made by Geva Kipper and Guy Shalev, 2021",
                 style={"textAlign": "center", "margin-bottom": "0px", "padding-bottom": "0px"}),
], style={"textAlign": "center", "margin-bottom": "0px"})

app.layout = dbc.Container([
    dcc.Location(id="url"),
    dbc.Row([], className="d-md-none",
            style={"height": "4rem"}
            ),
    dbc.Row([
        dbc.Col([
            content,
            footer2,
        ], style={"dir": "rtl"}),
        dbc.Col([
            sidebar,
        ], className="d-none d-md-block", width=2.5,
            style={"width": "16rem"}
        ),
    ]),
    mobile_navbar,
], fluid=True)

about_page = html.Div(children=[
    dbc.Container(style={"margin-right": "0rem", 'padding-right': "0rem"}, children=[
        dcc.Markdown(
            """
            #### ניתוח חזרות במוזיקה ישראלית
            קמנו בבוקר ויצאנו לעשות ניתוח סטטיסטי לשירים בעברית.
            בהשראת [מאמר שעשה ניתוח דומה באנגלית,](https://pudding.cool/2017/05/song-repetition/) בחרנו להתמקד בגישה פשוטה - 
            למדוד עד כמה אורך הטקסט מתקצר אם אנחנו מצמצמים חזרות. זה אותו הדבר שעושות תוכנות כיווץ כמו WinZip.
            באתר תוכלו לראות מה השירים הכי חזרתיים, ואיפה עומדים האמנים האהובים עליכם.  
             כדי ללמוד איך זה עובד, או איך שרים את השיר "אין (1-3)2x חגיגה, בלי (20-22)3x עוגה, איפה (42-45)12x ה(36-39)", פנו לדף ["איך זה עובד"](/curious).
            """, style={'textAlign': 'right', 'direction': 'rtl'}
        ),
        dbc.Row(className="flex-wrap-reverse", children=[
            dbc.Col(width=12, md=6,
                    style={"margin-bottom": "1rem", "flex": 1, 'textAlign': 'right', 'direction': 'rtl'}, children=[
                    dbc.Card(className="border-primary",
                             style={'textAlign': 'right', 'direction': 'rtl', "max-width": "64rem",
                                    "min-width": "16rem"}, children=[
                            dbc.CardHeader(style={"padding": "7px"}, children=[
                                html.I(className="fa fa-music", style={"paddingLeft": "0.5rem", "color": PURPLE}),
                                html.H5(
                                    html.A("פילוח לפי אמנים", href="/artists", style={"text-decoration":"none"}),
                                    className="card-title", style={"display": "inline-block"}),
                            ]),
                            dbc.CardBody(style={"padding": "7px"}, children=[
                                dcc.Markdown('''      
                                    רצינו לבדוק אם **אמנים מסוימים (לא חשוב שמות) כותבים שירים חזרתיים במיוחד**. 
                                     לקחנו את כל השירים, לא רק מהמצעדים, ועשינו פילוח לפי אמנים, והשוואה בין ז'אנרים מוזיקליים שונים. 
                                    בתור דוגמא, נספר לכם שהשירים של **דודו פארוק** מתכווצים בממוצע ל-55% מאורכם המקורי! לא מפתיע, למישהו שאפילו בשם הפרטי שלו יש חזרות.  
                                    * מי חוזר על עצמו הכי הרבה?  
                                    * השוואה בין ז'אנרים מוזיקליים
                                    * מה השירים הכי רפטטיביים של כל אמן, בכל הזמנים?  
                                    *  איזה אמנים מבולבלים יותר מיובל המבולבל?  
                                            ''',
                                             style={'textAlign': 'right', 'direction': 'rtl'})
                            ]),
                        ])
                ]),

            dbc.Col(width=12, md=6, style={"margin-bottom": "1rem", 'textAlign': 'right', 'direction': 'rtl'},
                    children=[
                        dbc.Card(className="border-primary",
                                 style={'textAlign': 'right', 'direction': 'rtl', "max-width": "64rem",
                                        "height": "100%",
                                        "min-width": "16rem"}, children=[
                                dbc.CardHeader(style={"padding": "7px"}, children=[
                                    html.I(className="fa fa-chart-line",
                                           style={"paddingLeft": "0.5rem", "color": PURPLE}),
                                    html.H5(
                                        html.A("מצעד הפזמונים", href="/charts", style={"text-decoration":"none"}),
                                        className="card-title",
                                        style={"display": "inline-block"}),
                                ]),
                                dbc.CardBody(style={"padding": "7px"}, children=[
                                    dcc.Markdown('''
                                        הדבר הראשון שעשינו זה **לנתח את השירים החזרתיים במצעד הפזמונים לאורך השנים.** 
                                        השיר הכי חזרתי מהמצעד האחרון, אגב, הוא **יש לי חור בלב בצורה שלך (ג'ירפות)**. נראה אתכם נזכרים ב-10 מילים שונות שנאמרות בשיר. 

                                        * האם השירים במצעד נהיים יותר חזרתיים עם השנים?
                                        * מה השירים הכי רפטטיביים שנבחרו ע"י גלגלצ בכל שנה? 
                                        * האם אפשר לזכות באירוויזיון עם שירים ממש שבלוניים? (רמז: כן)
                                        * יהודה יתן לו בעניבה או לא יתן?
                                    ''', style={'textAlign': 'right', 'direction': 'rtl'})
                                ])
                            ])
                    ])

        ]),

        dbc.Row(className="flex-wrap-reverse", children=[
            dbc.Col(width=12, md=6,
                    style={'textAlign': 'right', 'direction': 'rtl', "margin-bottom": "1rem", "flex": 1}, children=[
                    dbc.Card(className="border-primary",
                             style={'textAlign': 'right', 'direction': 'rtl', "max-width": "64rem",
                                    "min-width": "16rem", "height": "100%"}, children=[
                            dbc.CardHeader(style={"padding": "7px"}, children=[
                                html.I(className="fa fa-envelope-open-text",
                                       style={"paddingLeft": "0.5rem", "color": PURPLE}),
                                html.H5("צרו קשר", className="card-title", style={"display": "inline-block"}),
                            ]),
                            dbc.CardBody(style={"padding": "7px"}, children=[
                                dcc.Markdown('''
                                          אם אהבתם את האתר ואתם רוצים לספר למישהו, או שיש לכם שאלות, אתם מוזמנים ליצור קשר:
                                        ''', style={'textAlign': 'right', 'direction': 'rtl',
                                                    'margin-bottom': "-1rem"}),
                                dbc.Container(
                                    className="justify-content-center align-items-center",
                                    style={"width": "100%", "display": "flex", "padding-bottom": "0.5rem"}, children=[
                                        dbc.Col(
                                            html.Blockquote([
                                                html.H5("גבע קיפר"),
                                                html.Footer("מתכנת", className="blockquota-footer")
                                            ], className="m-0"),
                                            width=4, className="p-1", style={"max-width": "7rem"},
                                        ),
                                        html.A(
                                            html.I(className="fab fa-facebook-square fa-3x",
                                                   style={"padding": "1rem", "color": PURPLE}),
                                            href="https://www.facebook.com/geva.kipper/"
                                        ),
                                        html.A(
                                            html.I(className="fa fa-envelope-square fa-3x",
                                                   style={"padding": "1rem", "color": PURPLE}),
                                            href="mailto:gevakip@gmail.com"
                                        ),
                                        html.A(
                                            html.I(className="fab fa-linkedin fa-3x",
                                                   style={"padding": "1rem", "color": PURPLE}),
                                            href="https://www.linkedin.com/in/gevakip/"
                                        ),
                                    ]),
                                html.P(style={'textAlign': 'right', 'direction': 'rtl', "margin-bottom": "0.5rem"},
                                       children=[
                                           "אם אתם בכלל כאן בשביל אלגוריתמים וסטטיסטיקה, לכו לעמוד 'איך זה עובד'. תוכלו גם ",
                                           html.Strong(
                                               html.A("למצוא את הקוד ב-GitHub.",
                                                      href="https://github.com/gevak/glglstats"),
                                           )
                                       ]),
                            ])
                        ])
                ]),

            dbc.Col(width=12, md=6,
                    style={'textAlign': 'right', 'direction': 'rtl', "margin-bottom": "1rem", "flex": 1}, children=[
                    dbc.Card(className="border-primary",
                             style={'textAlign': 'right', 'direction': 'rtl', "max-width": "64rem", "width": "100%",
                                    "min-width": "16rem", "height": "100%"}, children=[
                            dbc.CardHeader(style={"padding": "7px"}, children=[
                                html.I(className="fa fa-palette", style={"paddingLeft": "0.5rem", "color": PURPLE}),
                                html.H5(
                                    html.A("דפוסי חזרות אומנותיים", href="/autocorrelation", style={"text-decoration":"none"}),
                                    className="card-title",
                                        style={"display": "inline-block"}),
                            ]),
                            dbc.CardBody(style={"padding": "7px"}, children=[
                                dcc.Markdown('''                               
                                        **חזרתיות היא לא בהכרח דבר רע**, ואנחנו אוהבים שירים חזרתיים! אז לסיום הוספנו **ויזואליזציה של השימוש האומנותי בחזרות**. תוכלו לראות את הדפוסים הנוצרים על ידי שירים שונים.
                                        הרעיון הגיע מהפרויקט [SongSim](https://colinmorris.github.io/SongSim/#/about), בו עשו ניתוח דומה לשירים באנגלית.
                                    ''', style={'textAlign': 'right', 'direction': 'rtl', "clear": "none"}),
                                dbc.Container(
                                    fluid=True,
                                    className="align-items-top",
                                    style={"width": "100%", "display": "flex", "padding": 0},
                                    children=[
                                        dbc.Col(width=7, style={"padding": "0"}, children=[
                                            dcc.Markdown("""
                                                * איזה דפוסים החזרות יוצרות?
                                                * איך מציירים את 'אחד מי יודע'?
                                                * איזה שיר מייצגת התמונה?
                                                * למה שרה שרה שיר שמח?
                                            """, style={"margin-bottom": "0rem", "margin-right": "-1.5rem"}),
                                        ]),
                                        dbc.Col(width=5, style={"padding": 0, "flex-shrink": "2"}, children=[
                                            html.Img(src="/static/images/plot1.png",
                                                     style={"max-width": "100%", "float": "left", "max-height": "6rem"})
                                        ]),
                                    ])
                            ]),
                            # dbc.CardImg(src="/static/images/plot1.png",),
                        ])
                ])

        ])
    ])
])

how_it_works_page = html.Div(children=[
    dcc.Markdown(
        open("HOW_IT_WORKS.md", "r", encoding="utf8").read(), style={'textAlign': 'right', 'direction': 'rtl'}),

])

charts_page = html.Div(style={'textAlign': 'right', 'direction': 'rtl'}, children=[
    html.Div(style={"padding-bottom": "0rem", "display": "inline-block", "max-width": "32rem"}, children=[
        dcc.Markdown("""
        #### מצעד הפזמונים
        מקום אחד שבו אפשר לצפות להתקל בהרבה שירים חזרתיים הוא מצעד הפזמונים השנתי. ומתברר ש[יש באינטרנט נתונים על המצעדים מאז שנות ה-70](http://pizmonet.co.il/wiki/%D7%A2%D7%9E%D7%95%D7%93_%D7%A8%D7%90%D7%A9%D7%99).  
         בחרו עשור או שנה שמעניינים אתכם, ותוכלו לראות את השירים הכי חזרתיים במצעדים המתאימים, בהשוואה לשיר הכי מגוון.

         גרף נוסף מציג לכם את החזרתיות בשירי המצעד לאורך השנים. שימו לב למגמת הירידה משנת 2012.   
        """),
        dcc.Dropdown(
            id="year-selection-list",
            options=[{
                'label': str(i),
                'value': i
            } for i in pop_charts.YEARS],
            value=[2020],
            multi=True,
            style={'textAlign': 'right', 'direction': 'rtl'},
        ),
        html.Div(
            children=
            ([html.Button(str(year) + "s", id=f'decade-button:{year}', n_clicks=0, className="btn-secondary")
              for year in pop_charts.YEARS if year % 10 == 0] +
             [html.Button("כל הזמנים", id=f'decade-button:כל הזמנים', n_clicks=0, className='btn-primary')] +
             [html.Button("נקה בחירה", id=f'decade-button:נקה בחירה', n_clicks=0, className='btn-primary')]),
            style={'text-align': 'center'}
        ),
    ]),
    dcc.Graph(
        id='most-repetitive-graph',
        style={"float": "left", "display": "inline-box", "max-width": "100%"},
        config={'displayModeBar': False},
    ),
    dbc.Container(fluid=True, children=[
        dbc.Row([
            # dbc.Col(width=12, md=12, children=[
            #    dcc.Graph(
            #        id='repetitiveness-by-index-graph',
            #        config={'displayModeBar': False},
            #    ),
            # ]),
            dbc.Col(width=12, md=12, children=[
                dcc.Graph(
                    id='chart-repetitiveness-graph',
                    figure=chart_repetitiveness_fig,
                    config={'displayModeBar': False},
                ),
            ]),
        ])
    ]),
])

artists_page = html.Div(style={'textAlign': 'right', 'direction': 'rtl'}, children=[
    html.Div(style={"padding-bottom": "0rem"}, children=[
        dcc.Markdown("""
        #### נתונים בחלוקה לאמנים
        יש אמונה רווחת שאמנים מסוימים (לא חשוב שמות) כותבים שירים חזרתיים במיוחד. אנחנו רוצים להעמיד את הטענה הזו למבחן.  
        הכניסו את שמות האמנים שמעניינים אתכם (או היעזרו בכפתורים) ותוכלו לראות את השירים הכי חזרתיים שלהם, ואת הנתונים הממוצעים של כל אמן על מנת להשוות.  
        האמנים הכי חזרתיים נוטים להיות אמני פופ צעירים, ואמני רוק וראפ נוטים להיות המגוונים ביותר במילים, אבל יש גם הפתעות.
        """),
        dbc.Container([
            dcc.Dropdown(
                id="artist-selection-list",
                options=[{
                    'label': i,
                    'value': i
                } for i in pop_charts.ALL_ARTISTS],
                value=pop_charts.DEFAULT_ARTISTS,
                multi=True,
                style={'textAlign': 'right', 'direction': 'rtl'}
            ),
            html.Div(
                children=
                ([html.Button(category, className="btn-secondary", id=f'category-button:{category}', n_clicks=0)
                  for category in pop_charts.ARTISTS] +
                 [html.Button("כולם", id=f'category-button:כולם', n_clicks=0, className='btn-primary')] +
                 [html.Button("נקה בחירה", id=f'category-button:נקה בחירה', n_clicks=0, className='btn-primary')]),
                style={'text-align': 'center'}
            ),
        ], style={"margin": "auto"})
    ]),

    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(width=12, md=6, children=[
                dcc.Graph(
                    id='artist-graph',
                    config={'displayModeBar': False},
                )
            ]),
            dbc.Col(width=12, md=6, children=[
                dcc.Graph(
                    id='most-repetitive-artists-graph',
                    config={'displayModeBar': False},
                ),
            ]),
        ])
    ]),
])

autocorrelation_page = html.Div(style={'textAlign': 'right', 'direction': 'rtl'}, children=[
    html.Div(style={"padding-bottom": "0rem", "display": "inline-block"}, children=[
        dcc.Markdown("""
                #### דפוסי חזרות אומנותיים
                הגרף מראה כל רגע בשיר בו חוזרת מילה שהופיעה קודם, והצבע נקבע על פי כמות ההופעות הכוללת של המילה.  
                אם תצביעו על נקודה בגרף עם העכבר, תוצג לכם המילה המתאימה. בחרו שיר:
                """),
        dcc.Dropdown(id='song-dropdown',
                     options=[{'label': x,
                               'value': x} for x in pop_charts.SELF_CORRELATION_SONGS],
                     clearable=False,
                     value="ג'ירפות - יש לי חור בלב בצורה שלך",
                     style={"width": '250px', 'textAlign': 'right', 'direction': 'rtl', 'display': 'inline-block', "border-color":PURPLE}),
        dcc.Dropdown(id='theme',
                     options=[{'label': x, 'value': x} for x in px.colors.named_colorscales()],
                     clearable=False,
                     value='thermal', style={'color': 'black', 'width': '100px',
                                             "margin-right": "5px", 'display': 'inline-block', "border-color":PURPLE}),
    ]),
    html.Div([
        dcc.Loading([
            dcc.Graph(id="correlation-graph", responsive=True, config={'displayModeBar': False}),
        ])
    ], style={"width": "500px", "height": "500px", "margin-right": "1rem", "margin-left": "1rem",
              "overflow": "auto", "vertical-align": "top",
              "float": "left", "display": "block"}),
    dbc.Card(style={'textAlign': 'right', 'direction': 'rtl', "max-width": "32rem",
                    "min-width": "8rem", "marginTop": "1rem"}, children=[
        dbc.CardHeader([
            html.H5("איזה דפוסים יוצרים השירים?", className="card-title"),
        ]),
        dbc.CardBody([
            dcc.Markdown('''                        
                       ##### 
                        * **פזמון חוזר ארוך** - רואים קווים אלכסוניים ארוכים
                        * **משפט קצר שחוזר הרבה פעמים** - רואים הרבה נקודות קטנות מפוזרות
                        * **מילה החוזרת ברצף** - רואים ריבועים מלאים קטנים
                        * **אחרי כל שורה חדשה חוזרים על כל השיר** - רואים קטעים אלכסוניים באורך הולך וקטן
                        * **דפוסים מיוחדים** - אתם תזהו אחד כשתראו אותו

                        נסו למצוא שיר שמתאים לכל אחד מהדפוסים.
                    ''', style={'textAlign': 'right', 'direction': 'rtl'})
        ])
    ]),
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return about_page
    elif pathname == "/charts":
        return charts_page
    elif pathname == "/artists":
        return artists_page
    elif pathname == "/autocorrelation":
        return autocorrelation_page
    elif pathname == "/curious":
        return how_it_works_page
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(Output('most-repetitive-graph', 'figure'),
              [Input('year-selection-list', 'value')])
def update_years_repetitive(selected_years):
    return plot.most_repetitive_songs(df=plot.CHART_DATA, years=selected_years)


@app.callback(Output('repetitiveness-by-index-graph', 'figure'),
              [Input('year-selection-list', 'value')])
def update_years_index(selected_years):
    return plot.repetitiveness_by_chart_index(selected_years)


@app.callback(
    Output('correlation-graph', 'figure'),
    [
        Input(component_id='song-dropdown', component_property='value'),
        Input(component_id='theme', component_property='value')]
)
def update_correlation_graph(song, theme):
    artist_name, song_name = song.split(" - ")
    sid = SongId(artist_name=artist_name, song_name=song_name)
    return plot.plot_self_correlation(sid, theme)


@app.callback(Output('year-selection-list', 'value'),
              [Input(f'decade-button:{decade}', "n_clicks")
               for decade in DECADE_OPTIONS])
def update_years_button(*buttons):
    ctx = dash.callback_context
    if not ctx.triggered:
        # No clicks yet
        return [2020]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        decade_name = button_id.split(":")[1]
    if decade_name == 'כל הזמנים':
        return [year for year in pop_charts.YEARS]
    if decade_name == 'נקה בחירה':
        return []
    decade = int(decade_name)
    return [year for year in pop_charts.YEARS if year - (year % 10) == decade]


@app.callback(Output('artist-graph', 'figure'),
              [Input('artist-selection-list', 'value')])
def update_artists_repetitiveness(selected_artists):
    return plot.repetitiveness_by_artist(selected_artists)


@app.callback(Output('most-repetitive-artists-graph', 'figure'),
              [Input('artist-selection-list', 'value')])
def update_artists_repetitive(selected_artists):
    return plot.most_repetitive_songs(df=plot.ARTISTS_DATA, artist_names=selected_artists)


@app.callback(Output('artist-selection-list', 'value'),
              [Input(f'category-button:{category}', "n_clicks")
               for category in list(pop_charts.ARTISTS.keys()) + ["כולם", "נקה בחירה"]])
def update_artists_button(*buttons):
    ctx = dash.callback_context
    if not ctx.triggered:
        # No clicks yet
        return pop_charts.DEFAULT_ARTISTS
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        category_name = button_id.split(":")[1]
    if category_name == "כולם":
        return pop_charts.ALL_ARTISTS
    elif category_name == "נקה בחירה":
        return pop_charts.DEFAULT_ARTISTS
    return list(set(pop_charts.ARTISTS[category_name]))


if __name__ == "__main__":
    app.run_server(debug=True)
